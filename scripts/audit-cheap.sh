#!/usr/bin/env bash
# 治理审计·便宜层（层 9-4）：全部确定性检查，退出码判决，LLM 一个字不用说。
# 用法：在被审计项目根目录跑 `bash <插件>/scripts/audit-cheap.sh`
# 铁律：永远从最便宜的层开始判——本脚本红了直接短路，别唤醒 docs-auditor（层 2 大模型裁判）。
set -uo pipefail
export LC_ALL=en_US.UTF-8
FAIL=0
ok(){ echo "  ✓ $1"; }
bad(){ echo "  ✗ $1"; FAIL=1; }
warn(){ echo "  ⚠ $1"; }

echo "[1] 四件套存在性"
for f in CLAUDE.md CLAUDE_MAP.md PROJECT_STATUS.md PROJECT_LOG.md; do
  [ -f "$f" ] && ok "$f" || warn "$f 缺失（若项目处于渐进采用低阶段属正常，报告即可）"
done

echo "[2] CLAUDE_MAP.md 路径真实性（治虚构路径）"
if [ -f CLAUDE_MAP.md ]; then
  # 提取形如 src/xxx、scripts/xxx.py、docs/xxx.md 的路径引用，逐条验存在
  grep -hoE '\`[A-Za-z0-9_./一-龥-]+/[A-Za-z0-9_./一-龥-]+\`' CLAUDE_MAP.md 2>/dev/null \
    | tr -d '\`' | sort -u | while read -r p; do
      [ -e "$p" ] || echo "$p"
    done > /tmp/.map_dead_paths
  if [ -s /tmp/.map_dead_paths ]; then
    bad "MAP 引用了不存在的路径："; sed 's/^/      - /' /tmp/.map_dead_paths
  else
    ok "MAP 路径抽查全部存在"
  fi
fi

echo "[3] STATUS 删除区复活检查（故意删掉的文件不许回来）"
if [ -f PROJECT_STATUS.md ]; then
  # 删除区表格里的路径若重新出现在磁盘上 = 复活，红
  awk '/删除区/,/^## /' PROJECT_STATUS.md | grep -oE '\| *[A-Za-z0-9_./-]+ *\|' \
    | tr -d '| ' | grep -E '/' | sort -u | while read -r p; do
      [ -e "$p" ] && echo "$p"
    done > /tmp/.status_resurrected
  if [ -s /tmp/.status_resurrected ]; then
    bad "删除区文件已复活（该删的又回来了）："; sed 's/^/      - /' /tmp/.status_resurrected
  else
    ok "删除区无复活"
  fi
fi

echo "[4] PROJECT_LOG.md 只追加检查（历史不许被改）"
if [ -f PROJECT_LOG.md ] && git rev-parse --git-dir >/dev/null 2>&1; then
  DELETED=$(git diff HEAD -- PROJECT_LOG.md 2>/dev/null | grep -c '^-[^-]' || true)
  if [ "${DELETED:-0}" -gt 0 ]; then
    bad "LOG 有 $DELETED 行被删改（工作区 diff）——流水账只许追加"
  else
    ok "LOG 工作区无删改"
  fi
fi

echo "[5] CLAUDE.md 指路牌死链"
if [ -f CLAUDE.md ]; then
  grep -hoE '\`?(docs|scripts|src|templates|references|skills|tests|config)/[A-Za-z0-9_./一-龥-]+\`?' CLAUDE.md 2>/dev/null \
    | tr -d '\`' | sort -u | while read -r p; do
      [ -e "$p" ] || echo "$p"
    done > /tmp/.claude_dead_refs
  if [ -s /tmp/.claude_dead_refs ]; then
    bad "CLAUDE.md 指路牌指向不存在的路径："; sed 's/^/      - /' /tmp/.claude_dead_refs
  else
    ok "指路牌无死链"
  fi
fi

echo "[6] 审计保鲜度（反馈频率必须跟上变更频率）"
if [ -f PROJECT_LOG.md ] && git rev-parse --git-dir >/dev/null 2>&1; then
  LAST_AUDIT_LINE=$(grep -E '^\#\# \[[0-9]{4}-[0-9]{2}-[0-9]{2}\].*(audit|审计)' PROJECT_LOG.md | tail -1)
  if [ -n "$LAST_AUDIT_LINE" ]; then
    LAST_DATE=$(echo "$LAST_AUDIT_LINE" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
    COMMITS_SINCE=$(git rev-list --count --since="$LAST_DATE" HEAD 2>/dev/null || echo "?")
    if [ "$COMMITS_SINCE" != "?" ] && [ "$COMMITS_SINCE" -gt 30 ]; then
      bad "上次审计 ${LAST_DATE}，之后已 $COMMITS_SINCE 个 commit（>30）——腐烂在审计间隙里发生，该审了"
    else
      ok "上次审计 ${LAST_DATE}，之后 $COMMITS_SINCE 个 commit"
    fi
  else
    warn "LOG 里没有审计记录——从未审计过或未按格式登记"
  fi
fi

echo
if [ "$FAIL" -eq 1 ]; then
  echo "✗ 便宜层未通过 —— 先修上面的确定性问题，不必唤醒 docs-auditor（层 2）。"
  exit 1
else
  echo "✓ 便宜层全绿 —— 可以唤醒 docs-auditor 判模糊问题（职责重叠 / STATUS 撒谎语气 / 指路牌合理性）。"
  exit 0
fi
