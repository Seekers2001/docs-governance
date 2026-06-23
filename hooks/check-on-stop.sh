#!/usr/bin/env bash
# docs-governance · Stop hook
# 会话结束时检查四件套是否在腐烂，只提醒不阻塞（exit 0）。
# 想改成"强制 Claude 先修复再停"，把结尾的 exit 0 改成 exit 2。
set -uo pipefail

quad=(CLAUDE.md CLAUDE_MAP.md PROJECT_STATUS.md PROJECT_LOG.md)
present=()
for f in "${quad[@]}"; do [ -f "$f" ] && present+=("$f"); done
# 没用四件套的项目，直接放行
[ ${#present[@]} -eq 0 ] && exit 0

warned=0

# 检查1：相对时间残留（LOG/STATUS 重灾区，必须绝对日期）
rot=$(grep -nE "今天|昨天|刚刚|最近|上周|本周|recently|yesterday" "${present[@]}" 2>/dev/null || true)
if [ -n "$rot" ]; then
  echo "⚠️ docs-governance: 四件套里有相对时间，应改绝对日期（如 $(date +%Y-%m-%d)）：" >&2
  echo "$rot" >&2
  warned=1
fi

# 检查2：PROJECT_LOG 今天有没有追加（本会话有进展就该补一行）
if [ -f PROJECT_LOG.md ]; then
  today=$(date +%Y-%m-%d)
  if ! grep -q "$today" PROJECT_LOG.md 2>/dev/null; then
    echo "⚠️ docs-governance: PROJECT_LOG.md 今天（$today）还没有条目，这次会话有进展记得追加一行 [日期] 类型 | 摘要。" >&2
    warned=1
  fi
fi

[ "$warned" -eq 1 ] && echo "（以上为 docs-governance 治理提醒，不阻塞；要强制可把 hook 脚本结尾改 exit 2）" >&2
exit 0
