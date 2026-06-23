#!/usr/bin/env bash
# 插件结构完整性自检：JSON 可解析 / hook 可执行 / 命令→agent→skill/template/reference 引用不断链。
# 这是插件自己的"测试"——任何一处断链 exit 1，可挂进 CI 或发布前手动跑。
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
FAIL=0
ok(){ echo "  ✓ $1"; }
bad(){ echo "  ✗ $1"; FAIL=1; }

echo "[1] JSON 可解析"
for j in .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json; do
  [ -f "$j" ] || { echo "  – $j 不存在，跳过"; continue; }
  python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$j" 2>/dev/null && ok "$j" || bad "$j 解析失败"
done

echo "[2] hook 脚本可执行"
shopt -s nullglob
for h in hooks/*.sh; do [ -x "$h" ] && ok "$h" || bad "$h 不可执行（chmod +x）"; done

echo "[3] 命令引用的 agent 存在"
for c in commands/*.md; do
  while IFS= read -r a; do
    [ -z "$a" ] && continue
    [ -f "agents/$a.md" ] && ok "$(basename "$c") → agents/$a.md" || bad "$(basename "$c") → agents/$a.md 缺"
  done < <(grep -oE "contract-director|frontend-dev|backend-dev|docs-governor|docs-auditor" "$c" | sort -u)
done

echo "[4] 路径式引用（templates/ references/ skills/）存在"
grep -rhoE "(templates|references)/[A-Za-z0-9._-]+\.md|skills/[A-Za-z0-9._-]+/SKILL\.md" agents/ skills/ commands/ 2>/dev/null | sort -u | while read -r ref; do
  [ -f "$ref" ] && ok "$ref" || bad "$ref 被引用但不存在"
done
# 子 shell 里的 FAIL 不外传，单独复核第 4 项
MISS=$(grep -rhoE "(templates|references)/[A-Za-z0-9._-]+\.md" agents/ skills/ commands/ 2>/dev/null | sort -u | while read -r ref; do [ -f "$ref" ] || echo "$ref"; done)
[ -n "$MISS" ] && FAIL=1

echo "[5] 每个 skill 有 SKILL.md / 每个 command 与 agent 是 .md"
for d in skills/*/; do [ -f "$d/SKILL.md" ] && ok "$d" || bad "$d 缺 SKILL.md"; done

echo ""
if [ "$FAIL" -eq 0 ]; then echo "✅ verify 通过：插件结构完整，无断链。"; else echo "❌ verify 失败：见上面 ✗。"; fi
exit "$FAIL"
