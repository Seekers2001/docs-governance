# CLAUDE_MAP.md — 插件地图（只记 `ls` 看不出来的）

> 目录里有啥直接 `ls`；这里只记依赖方向、非显然定位、易误读区。

## 依赖方向（改动的因果链）

```
command → agent → skill（方法论唯一源）
                → templates/（给用户项目套的空白模板）
                → references/（收尾同步矩阵）

自然语言触发 → test-collaboration skill → templates/TESTS.example.md

Codex / ChatGPT → .codex-plugin/plugin.json → skills/*
Codex 项目入口 → AGENTS.md（薄桥接）→ CLAUDE.md（共享章程唯一源）
```

- 改**方法论** → 只动 `skills/*/SKILL.md`，agent / command 自动继承（它们只指向、不复制）
- 改**模板** → `templates/*.example.md`
- 加**体检项** → `scripts/verify.sh`

## 找 X 去哪

| 要找 | 去 |
|---|---|
| 活文档方法论 | `skills/living-docs-governance/SKILL.md` |
| 契约方法论（含两种模式） | `skills/contract-first/SKILL.md` |
| 测试资产与必要测试点治理 | `skills/test-collaboration/SKILL.md` |
| 模块联动回归方法论 | `skills/module-regression/SKILL.md` |
| TESTS.md 空白模板 | `templates/TESTS.example.md` |
| Codex 项目入口模板 | `templates/AGENTS.example.md` |
| 收尾同步矩阵 | `references/governance-sync-matrix.md` |
| 结构完整性自检 | `scripts/verify.sh` |

## 易误读（别混）

- `templates/*.example.md` 是给**用户项目**套用的空白模板，**不是本插件自己的治理文件**。本插件自己的治理文件是根目录的 `CLAUDE.md` / `CLAUDE_MAP.md` / `PROJECT_STATUS.md` / `PROJECT_LOG.md`（无 `.example` 后缀）。
- `.codex-plugin/plugin.json` 与 `.claude-plugin/plugin.json` 是不同宿主的安装入口，名称和版本必须一致；方法论仍只在 `skills/` 维护。
- 根目录 `AGENTS.md` 只负责让 Codex 进入共享 `CLAUDE.md` 章程，不是第五份治理文档。
