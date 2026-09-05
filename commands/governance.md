---
description: 对当前项目做活文档治理——扫描真实结构，生成或增量更新四件套治理文档（CLAUDE.md / CLAUDE_MAP.md / PROJECT_STATUS.md / PROJECT_LOG.md），并按需生成 Codex 的 AGENTS.md 薄桥接，全中文。
---

读取 `skills/living-docs-governance/SKILL.md`，执行“已有项目治理”模式。

用户参数：`$ARGUMENTS`。将参数作为该模式定义的项目信息、范围或阶段说明传入；规则与读写边界以 Skill 为唯一来源。

Claude Code 可由 **docs-governor** 承担该模式；传入目标项目根目录、参数与已有验证证据，不复制流程。
