# Matt Skills：交付物契约缺口核对

## 结论

值得记录为 Issue 候选，但应把问题收窄为：**进入 idea-to-ship 工作流前，先确认并在后续阶段保持交付物契约**。

这不是“埋点分析 Skill”缺失，也不应把 `to-spec` 扩成通用商业方案生成器。真实缺口是：现有路由能决定进入原型、工程规格或实现，却没有先固定交付物类型、目标受众、代表性案例、必须包含项和明确排除项。

## 一手源码证据

核对基准：GitHub `mattpocock/skills` 当前 `main`，提交 `84fdeffd12f2ee307994d1eb6feb48173b6e0502`（2026-08-06）。

### `ask-matt`

- [`skills/engineering/ask-matt/SKILL.md` 第 13–26 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering/ask-matt/SKILL.md#L13-L26) 以“能否通过对话解决问题”“是否是多会话构建”决定进入 `prototype`、`to-spec` 或 `implement`。
- 它没有先区分最终要的是企业方案、产品 brief、工程 spec、原型还是实现，也没有要求锁定目标受众。
- [第 77–83 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering/ask-matt/SKILL.md#L77-L83) 中只有 `to-questionnaire` 会围绕“发给谁、要收回什么”提问，但这是发送问卷的专用边界，不是通用交付物契约。

### `grilling` / `grill-me`

- [`skills/productivity/grilling/SKILL.md` 第 6–22 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/productivity/grilling/SKILL.md#L6-L22) 定义了设计树、frontier、事实与决策分工，以及“共享理解后才行动”。
- [`grill-me`](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/productivity/grill-me/SKILL.md) 只是调用该访谈原语。
- 两者均未把以下内容列为共享理解的必要组成：交付物类型、目标读者、代表性案例、必须包含项、明确排除项。

### `to-spec`

- [`skills/engineering/to-spec/SKILL.md` 第 7–19 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering/to-spec/SKILL.md#L7-L19) 明确把已讨论内容合成为工程 spec，并发布到 issue tracker。
- [模板第 23–69 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering/to-spec/SKILL.md#L23-L69) 已有 Problem、Solution、User Stories、Implementation Decisions、Testing Decisions 和 Out of Scope，因此“排除项”已有部分覆盖。
- 但模板没有目标受众，也没有要求给出代表性交付案例。第 37–39 行只是用户故事句式示例，不是本项目的业务案例。
- 官方说明也明确 spec 主要给 agent 阅读，见 [`docs/engineering/to-spec.md` 第 50–54 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/docs/engineering/to-spec.md#L50-L54)。它不适合作为企业对外方案的默认容器。

### `prototype`

- [`skills/engineering/prototype/SKILL.md` 第 8–17 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering/prototype/SKILL.md#L8-L17) 会先锁定要回答的问题，并区分 Logic 与 UI 两种产物。
- [`LOGIC.md` 第 18–20、41–48 行](https://github.com/mattpocock/skills/blob/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering/prototype/LOGIC.md#L18-L48) 已要求写明问题，并提供 happy path、edge case、非法操作等 guided scenarios。
- 因此“Logic Prototype 缺案例”并不成立。缺的是进入 prototype 之前，没有确认“用户最终只要企业方案，而非原型或工程实现”。

## 本次会话案例

最终交付物 外部项目的 `saas-web/.scratch/product-usage-analytics/spec.md`（不随本插件分发，以下保留当时的案例结论） 已收敛为企业方案：

- 第 3–4 行明确受众是企业管理者与产品负责人，只说明评估框架和呈现结果，排除菜单调整、技术实现和数据采集方式。
- 第 54–61 行给出管理者会看到的信号案例。
- 第 71–83 行给出功能地图和其他功能使用情况的具体成品示例。
- 第 109–113 行再次明确方案边界。

这个结果说明**案例应该有**：它让“最终成品长什么样、读者如何使用”变得可判断。但案例应属于前置交付物契约，不应成为强迫每个工程 spec 写大量案例的新规则。

本次会话在收敛前曾进入原型、事件、阈值、路由和伪代码，直到用户明确“我们只给方案”才删除。这是可复现的返工证据，而不是纯理论设想。

## 重叠判断

| 能力 | 当前覆盖 | 判断 |
|---|---|---|
| 路由到 prototype / spec / implement | `ask-matt` 已有 | 有能力，但路由前提不完整 |
| 消除设计假设 | `grilling` 已有 | 有机制，但未规定交付物边界必须被确认 |
| 工程 spec 的排除项 | `to-spec` 已有 `Out of Scope` | 部分重叠 |
| Logic Prototype 场景案例 | `prototype/LOGIC.md` 已有 | 不应重复贡献 |
| 目标受众 | 无通用要求 | 真实缺口 |
| 代表性成品/使用案例 | 无通用要求 | 真实缺口 |
| 必须包含项 | 无通用要求 | 真实缺口 |
| 跨阶段保持交付物契约 | 无明确要求 | 真实缺口 |

## 是否值得提 Issue

**值得先提 Issue，不建议直接 PR。** 它改变的是 `ask-matt` 进入主工作流的判断语义，并涉及 `grilling` 的完成条件，需要维护者先确认边界。

建议标题：

> Ask Matt: confirm the deliverable contract before entering the idea-to-ship flow

建议用本次企业功能使用评估作为具体案例，说明没有契约时，流程会把“给管理者看的方案”误路由成 prototype / engineering spec，并产生可删除的技术内容。

## 最小修改建议

不要新增 Skill，不要新增数据库或 metadata 系统，也不要扩大 `to-spec` 的职责。

仅在请求存在歧义时，先确认并在后续 handoff 保留一个轻量块：

```text
Deliverable: 企业功能使用评估方案
Audience: 企业管理者 / 产品负责人
Representative example(s): 一个核心功能如何用五项指标判断真实使用效果
Include: 评估范围、指标、看板呈现、结论解释、企业成果
Exclude: 埋点事件、技术路由、阈值规则、伪代码、实现方案
```

若 Issue 获认可，最小 PR 优先：

1. 在 `ask-matt` 的 idea-to-ship 入口增加歧义判断：未明确交付物时，先确认契约再路由。
2. 在 `grilling` 的共享理解退出条件中加入：存在对后续行动有影响时，交付物、受众、代表性案例、包含与排除项已经明确。
3. `to-spec` 只继承已确认的契约，并继续保留现有 `Out of Scope`；不要让它承担通用商业提案写作。
