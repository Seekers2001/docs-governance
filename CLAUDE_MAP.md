# CLAUDE_MAP.md — 插件地图（只记 `ls` 看不出来的）

> 目录里有啥直接 `ls`；这里只记依赖方向、非显然定位、易误读区。

## 依赖方向（改动的因果链）

```
command → agent → skill（方法论唯一源）
                → templates/（给用户项目套的空白模板）
                → references/（收尾同步矩阵）
```

- 改**方法论** → 只动 `skills/*/SKILL.md`，agent / command 自动继承（它们只指向、不复制）
- 改**模板** → `templates/*.example.md`
- 加**体检项** → `scripts/verify.sh`

## 找 X 去哪

| 要找 | 去 |
|---|---|
| 活文档方法论 | `skills/living-docs-governance/SKILL.md` |
| 契约方法论（含两种模式） | `skills/contract-first/SKILL.md` |
| 收尾同步矩阵 | `references/governance-sync-matrix.md` |
| 结构完整性自检 | `scripts/verify.sh` |

## 易误读（别混）

- `templates/*.example.md` 是给**用户项目**套用的空白模板，**不是本插件自己的治理文件**。本插件自己的治理文件是根目录的 `CLAUDE.md` / `CLAUDE_MAP.md` / `PROJECT_STATUS.md` / `PROJECT_LOG.md`（无 `.example` 后缀）。
