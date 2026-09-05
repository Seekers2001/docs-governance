# ARCHITECTURE.md — docs-governance 当前架构

> 本文是插件**当前架构**的唯一说明入口。设计选择及其理由在 `docs/adr/README.md`；文件定位与误导清单在 `CLAUDE_MAP.md`；方法论唯一源仍在 `skills/*/SKILL.md`。

## 架构摘要

插件以 `skills/` 为窄腰：Claude Code、Codex 与 ChatGPT 各自通过宿主 Adapter 进入同一套方法论，命令和 agent 不复制方法论。模板、参考和确定性脚本位于边缘，目标项目的 Markdown 始终是事实源。

## Module 权责与状态归属

| Module | 唯一职责 | 状态归属 | 对外 Interface | 允许依赖 | 禁止依赖 |
|---|---|---|---|---|---|
| 宿主 Adapter | 把 Claude Code、Codex、ChatGPT 的入口转换为统一 Skill 调用 | 无持久状态 | manifest、command、agent 调用约定 | 总路由与专项 Skill | 持有或复制方法论 |
| 总路由 | 根据用户意图选择专项 Skill 和执行顺序 | 无持久状态 | `skills/docs-governance/SKILL.md` | 专项 Skill | 复制专项方法论 |
| 专项 Skill | 保存治理方法论唯一真相 | 无运行时状态 | 各 `skills/*/SKILL.md` | 模板、参考与确定性脚本 | 宿主专用实现 |
| 模板与参考 | 提供空白载体和同步矩阵 | 无运行时状态 | `templates/`、`references/` | 无 | 反向依赖 agent 或 command |
| 确定性执行 | 处理断链、日志索引、结构自检、提醒和 CI | `.governance/` 只保存可重建派生状态 | `scripts/`、`hooks/`、`.github/workflows/verify.yml` | Markdown 事实源 | 把 SQLite 当事实源 |

## 代码依赖图

```mermaid
flowchart LR
    CODEX["Codex manifest"] --> ROUTER["docs-governance router"]
    CLAUDE["Claude command / agent"] --> SKILL["专项 Skill"]
    ROUTER --> SKILL
    SKILL --> TEMPLATE["templates"]
    SKILL --> REFERENCE["references"]
    SKILL --> SCRIPT["deterministic scripts"]
    SCRIPT --> FACTS["Markdown facts"]
    HOOK["Stop hook"] --> FACTS
    CI["GitHub Actions"] --> VERIFY["scripts/verify.sh"]
    VERIFY --> SCRIPT
```

> 箭头表示左侧实现依赖右侧 Interface。方法论依赖只能从宿主入口指向 Skill，不能把方法论复制回 command 或 agent。

## 运行时核心流转图

```mermaid
flowchart LR
    USER["用户意图"] --> HOST["宿主 Adapter"]
    HOST --> ROUTE["总路由或专项入口"]
    ROUTE --> METHOD["读取专项 Skill"]
    METHOD --> SCAN["扫描目标项目真实证据"]
    SCAN --> MODE{"只读还是写入"}
    MODE -->|只读| AUDIT["确定性检查 → 语义审计"]
    MODE -->|已授权写入| DOCS["生成或更新治理文档"]
    DOCS --> VERIFY["验证与阶段同步"]
    AUDIT --> REPORT["证据报告"]
    VERIFY --> REPORT
    REPORT --> USER
```

> 这张图表示运行时工作流，不代表代码依赖。审计默认只读；写入必须来自用户授权。

## Interface 与 Adapter 证据

| Interface / Seam | 定义位置 | Adapter / 调用方 | 约束唯一来源 |
|---|---|---|---|
| 插件发现 | `.claude-plugin/plugin.json`、`.codex-plugin/plugin.json` | Claude Code、Codex / ChatGPT | 双端 manifest |
| 方法论执行 | `skills/*/SKILL.md` | commands、agents、当前 Codex agent | 对应 Skill |
| 项目文档生成 | `templates/*.example.md` | docs-governor 或当前 agent | 模板 + 对应 Skill |
| 机器契约模板 | `templates/openapi.example.json` | CONTRACT 模板、消费方/提供方校验器 | 单一 OpenAPI 文档 |
| 确定性审计 | `scripts/audit-cheap.sh`、`scripts/audit-docs.py` | governance-audit | 脚本退出码 |
| 测试与发布前验证 | `TESTS.md`、`scripts/verify.sh` | 本地开发、GitHub Actions | TEST-ID + 命令退出码 |

现有展示版架构图在 `diagram/architecture.svg`，渲染预览为 `diagram/architecture.png`；若它与本文冲突，以本文和真实代码为准，并在同次结构变更中同步展示图。

## 更新规则

- 宿主入口、路由、专项 Skill、模板/参考或确定性脚本的职责及依赖变化 → 同次更新本文。
- 难回退的架构选择及理由 → 一项一份 ADR；本文只反映 accepted 决策后的当前结构。
- Interface 字段、测试证据和下游命令分别留在 CONTRACT、TESTS、REGRESSION 对应载体，不复制进本文。
