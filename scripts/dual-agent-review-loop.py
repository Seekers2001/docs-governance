#!/usr/bin/env python3
"""Bounded Claude/Codex review loop for one Markdown document."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime


START_MARKER = "<!-- dual-agent-review:start -->"
END_MARKER = "<!-- dual-agent-review:end -->"
VERDICT_RE = re.compile(r"^VERDICT:\s*(PASS|CHANGES_NEEDED)\s*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="文档变化后，让 Claude 与 Codex 做有限轮次的只读交叉评审。"
    )
    parser.add_argument("document", type=Path, help="需要监测和评审的 Markdown 文件")
    parser.add_argument("--max-rounds", type=int, default=2, help="最多讨论轮数，默认 2")
    parser.add_argument("--timeout", type=int, default=300, help="每次 Agent 调用超时秒数")
    parser.add_argument(
        "--watch-interval",
        type=int,
        default=0,
        help="大于 0 时常驻监测，每隔指定秒数检查一次；默认只检查一次",
    )
    parser.add_argument("--force", action="store_true", help="忽略文件哈希，强制评审一次")
    parser.add_argument(
        "--claude-budget-usd", type=float, default=0.50, help="单次 Claude 调用预算上限"
    )
    return parser.parse_args()


def source_without_review(text: str) -> str:
    pattern = re.compile(
        rf"\n?{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}\n?",
        re.DOTALL,
    )
    return pattern.sub("\n", text).rstrip() + "\n"


def source_hash(text: str) -> str:
    return hashlib.sha256(source_without_review(text).encode("utf-8")).hexdigest()


def state_path(document: Path) -> Path:
    current = document.parent.resolve()
    for directory in (current, *current.parents):
        git_dir = directory / ".git"
        if git_dir.is_dir():
            return git_dir / f"dual-agent-review-{document.stem}.json"
    return document.with_suffix(document.suffix + ".review-state.json")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_agent(command: list[str], prompt: str, cwd: Path, timeout: int) -> str:
    try:
        result = subprocess.run(
            [*command, prompt],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"找不到命令：{command[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{command[0]} 调用超过 {timeout} 秒") from exc

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "无错误输出"
        raise RuntimeError(f"{command[0]} 退出码 {result.returncode}：{detail}")
    return result.stdout.strip()


def verdict(output: str) -> str:
    match = VERDICT_RE.search(output)
    return match.group(1) if match else "INVALID"


def common_prompt(document: Path, round_number: int, transcript: str) -> str:
    return f"""你正在参与一场有上限的双 Agent 方案评审。

项目根目录：{document.parent}
主要文档：{document}
当前轮次：{round_number}

请先读取主要文档，并按其中“需要 Claude 重点评审的问题”以及项目现有规则进行审查。
你只能评审，不得修改任何文件，不得调用另一个 Agent。

输出必须满足：
1. 第一行只能是 `VERDICT: PASS` 或 `VERDICT: CHANGES_NEEDED`。
2. PASS 表示方案已可进入实现，没有阻塞问题；非阻塞建议可以保留。
3. CHANGES_NEEDED 必须列出具体阻塞问题和建议修改。
4. 区分事实、推断和建议，避免仅表示赞同。
5. 使用中文，控制在 800 字以内。

此前讨论记录：
{transcript or '（这是第一位发言者，暂无此前记录）'}
"""


def build_review_block(document_hash: str, rounds: list[dict], status: str) -> str:
    lines = [
        START_MARKER,
        "## 双 Agent 自动评审",
        "",
        "> 此区域由 `scripts/dual-agent-review-loop.py` 管理；修改正文会触发新评审。",
        f"> 正文版本：`{document_hash[:12]}`",
        f"> 评审时间：{datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"> 最终状态：**{status}**",
        "",
    ]
    for item in rounds:
        lines.extend(
            [
                f"### 第 {item['round']} 轮 · Claude",
                "",
                item["claude"],
                "",
                f"### 第 {item['round']} 轮 · Codex",
                "",
                item["codex"],
                "",
            ]
        )
    lines.extend([END_MARKER, ""])
    return "\n".join(lines)


def write_review(document: Path, original: str, block: str) -> None:
    clean = source_without_review(original).rstrip()
    document.write_text(f"{clean}\n\n{block}", encoding="utf-8")


def review_once(args: argparse.Namespace) -> bool:
    document = args.document.resolve()
    if not document.is_file():
        raise RuntimeError(f"文档不存在：{document}")
    if args.max_rounds < 1:
        raise RuntimeError("--max-rounds 必须大于 0")

    original = document.read_text(encoding="utf-8")
    digest = source_hash(original)
    state_file = state_path(document)
    state = load_state(state_file)
    if not args.force and state.get("last_source_hash") == digest:
        print(f"无正文变化，跳过：{document.name}")
        return False

    root = document.parent
    claude_command = [
        os.environ.get("CLAUDE_BIN", "claude"),
        "-p",
        "--permission-mode",
        "plan",
        "--allowedTools",
        "Read,Grep,Glob",
        "--no-session-persistence",
        "--max-budget-usd",
        str(args.claude_budget_usd),
    ]
    codex_command = [
        os.environ.get("CODEX_BIN", "codex"),
        "exec",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--cd",
        str(root),
    ]

    rounds: list[dict] = []
    transcript = ""
    final_status = "达到最大轮数，仍需人工判断"

    for round_number in range(1, args.max_rounds + 1):
        claude_output = run_agent(
            claude_command,
            common_prompt(document, round_number, transcript),
            root,
            args.timeout,
        )
        claude_record = f"Claude：\n{claude_output}"
        codex_output = run_agent(
            codex_command,
            common_prompt(document, round_number, f"{transcript}\n\n{claude_record}"),
            root,
            args.timeout,
        )
        rounds.append({"round": round_number, "claude": claude_output, "codex": codex_output})
        transcript += f"\n\n第 {round_number} 轮\n{claude_record}\nCodex：\n{codex_output}"

        if verdict(claude_output) == "PASS" and verdict(codex_output) == "PASS":
            final_status = "双方通过"
            break

    block = build_review_block(digest, rounds, final_status)
    write_review(document, original, block)
    save_state(
        state_file,
        {
            "document": str(document),
            "last_source_hash": digest,
            "reviewed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "rounds": len(rounds),
            "status": final_status,
        },
    )
    print(f"评审完成：{document.name}；{len(rounds)} 轮；{final_status}")
    return True


def main() -> int:
    args = parse_args()
    try:
        if args.watch_interval <= 0:
            review_once(args)
            return 0

        print(f"开始监测：{args.document}；间隔 {args.watch_interval} 秒。Ctrl-C 停止。")
        while True:
            review_once(args)
            args.force = False
            time.sleep(args.watch_interval)
    except KeyboardInterrupt:
        print("监测已停止。")
        return 0
    except RuntimeError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
