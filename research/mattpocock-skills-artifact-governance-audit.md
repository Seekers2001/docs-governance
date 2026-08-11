# `mattpocock/skills` 项目产物落盘、关联与生命周期审计

研究日期：2026-08-02
本地源码：`/Users/daoer/Desktop/0-GitHub/skills-library/mattpocock-skills`
本地快照：[`2ab9580`](https://github.com/mattpocock/skills/commit/2ab958093e83e0ec752e6c1c5932da465bf23e0c)
上游仓库：[`mattpocock/skills`](https://github.com/mattpocock/skills)

## 结论先行

Matt Skills **已经规定多数产物各自放在哪里**，但没有要求把它们都复制到一个统一文档或统一目录：

- Wayfinder Map、decision tickets、spec、implementation tickets 默认进入项目配置的 Issue Tracker；
- 本地 Markdown tracker 才会统一落到 `.scratch/<effort-or-feature>/`；
- 领域词汇进入 `CONTEXT.md` / `CONTEXT-MAP.md`；
- ADR 进入 `docs/adr/`，多 context 项目也可在各 context 下放 `docs/adr/`；
- research、prototype 和 handoff 各自还有独立的临时/throwaway 生命周期。

这不是“完全没有治理”，而是 **按产物职责分散治理**。项目已有单一真相、context pointer、tracker 配置、ADR 冲突提示等局部规则；缺少的是跨这些载体的 **artifact graph integrity**：没有一个流程定期核对 Map → decision ticket → spec → implementation ticket → ADR/current docs 之间的链接是否存在、是否断裂、是否产生孤儿、历史计划是否被误当成当前真相。

因此：

1. **不建议新增一个固定的 `DOCS.md`、`PROJECT_INDEX.md` 或把全部卡片复制进同一文件。** 这会制造第二份真相，并违背 Wayfinder “map is an index, not a store” 的设计。
2. **最小且有价值的贡献，是 review-only 的 artifact-link integrity 检查。** 它发现已有载体、分类当前真相/历史记录/临时证据、检查必要指针与断链，只报告，不自动重组文档。
3. 该能力不应新开 Issue。它直接落在现有 [#307 Documentation Review & Alignment Skill](https://github.com/mattpocock/skills/issues/307) 的范围内；Wayfinder 并行分支中 durable docs 丢失的问题又已由 [#579](https://github.com/mattpocock/skills/issues/579) 精确覆盖。

## 一、产物当前放在哪里

| 产物 | 当前权威位置 | 已有关系规则 | 生命周期判断 |
|---|---|---|---|
| Wayfinder Map | 配置的 Issue Tracker；GitHub 上是带 `wayfinder:map` 的 Issue；本地是 `.scratch/<effort>/map.md` | Map 是 canonical **index**；每个 decision 的完整答案只在对应 ticket，Map 仅留一行 gist + 链接 | **部分具备**：有 open/claimed/resolved、fog/out-of-scope；没有完成后 archive、final-spec 回链或长期保鲜规则 |
| Wayfinder decision ticket | Map 的 child issue；本地是 `.scratch/<effort>/issues/NN-<slug>.md` | resolution comment/`## Answer` 是答案；关闭/标记 resolved 后回链 Map | **已具备基本关闭生命周期**；但 durable repo docs 如何合并到共享基线未解决 |
| Spec / PRD | 配置的 Issue Tracker；本地是 `.scratch/<feature>/spec.md` | `to-spec` 读取领域词汇与 ADR，发布后打 `ready-for-agent` | **部分具备**：定义了创建与消费，没有通用 close/archive/supersede 规则；现有讨论把 spec 视作历史交付记录，而不是长期当前真相 |
| Implementation tickets / task cards | 配置的 Issue Tracker；本地是 `.scratch/<feature>/issues/<NN>-<slug>.md` | 可带 Parent、blocking edges、acceptance criteria；每 ticket 一文件/Issue | **部分具备**：有依赖和状态，没有对已实现 ticket 与最终 PR/commit/current docs 的统一回链检查 |
| Domain glossary | 单 context：根 `CONTEXT.md`；多 context：根 `CONTEXT-MAP.md` 指向各 context 的 `CONTEXT.md` | `CONTEXT-MAP.md` 只表达领域 context 的位置与关系 | **部分具备**：有固定入口与按需创建；无 repository-wide freshness/audit |
| ADR | 单 context：`docs/adr/NNNN-slug.md`；多 context 另可用 `src/<context>/docs/adr/` | 三项门槛；可选 `proposed / accepted / deprecated / superseded by ADR-NNNN` | **部分具备**：有位置、编号、可选 supersede；无强制状态、索引或断链审计 |
| Research | `/research` 写 cited Markdown；Wayfinder research 另放 throwaway `research/<name>` branch，并由 ticket 指针引用 | 研究文件是 primary source，ticket 保存 pointer | **部分具备**：有保存和引用规则；无统一纳入最终 spec/current docs 的检查 |
| Prototype | 代码靠近使用点但明确标为 prototype；完成后保存在 throwaway branch，implementation issue 留 pointer | validated decision 进入 real code，原型作为 primary source 留在支线 | **部分具备**：有 capture 规则；与同一 worktree 产生的 ADR/CONTEXT 如何拆分已被 #579 指出 |
| Handoff | 操作系统临时目录，不进入 workspace | 不复制 spec、ADR、Issue、commit、diff，只引用路径/URL | **已具备明确临时生命周期** |

### 一手源码证据

- Wayfinder 明确规定 Map 是 tracker 上的 canonical artifact，同时强调它是 “index, not a store”，decision 只存于 ticket；ticket resolve 后把 resolution 留在 ticket，再向 Map 追加 pointer：[`wayfinder/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/wayfinder/SKILL.md#L19-L25)、[`L118-L128`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/wayfinder/SKILL.md#L118-L128)。
- 本地 tracker 把 spec、tickets、Wayfinder Map 固定到 `.scratch/` 的不同文件：[`issue-tracker-local.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md#L1-L30)。
- GitHub tracker 则把 specs/PRDs、Map 和 child tickets 都放在 GitHub Issues：[`issue-tracker-github.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md#L1-L45)。
- `to-spec` 只要求发布到配置的 tracker，并要求使用 glossary、尊重 ADR：[`to-spec/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/to-spec/SKILL.md#L7-L20)。
- `to-tickets` 定义了本地每 ticket 一文件、真实 tracker 每 ticket 一 Issue，以及 parent/blocking/acceptance criteria：[`to-tickets/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/to-tickets/SKILL.md#L58-L105)。
- Domain docs 固定为 `CONTEXT.md` / `CONTEXT-MAP.md` 与 `docs/adr/`，并按需创建：[`domain-modeling/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/domain-modeling/SKILL.md#L10-L40)。
- ADR 的状态与 supersede 关系只是可选字段：[`ADR-FORMAT.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/domain-modeling/ADR-FORMAT.md#L17-L27)。
- Prototype 保存在 throwaway branch，Issue 留 pointer；主干只保留 validated decision：[`prototype/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/prototype/SKILL.md#L19-L26)。
- Handoff 明确保存到 OS 临时目录，并引用而不复制其他 artifacts：[`handoff/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/productivity/handoff/SKILL.md#L8-L16)。

## 二、它已经具备哪些治理

### 已具备

1. **产物分职**：Map 是索引、ticket 是 decision store、`CONTEXT.md` 是 glossary、ADR 是难以逆转决定的 why；没有把所有内容混成一份长文档。
2. **tracker 可配置**：`setup-matt-pocock-skills` 会生成 `docs/agents/issue-tracker.md` 与 `docs/agents/domain.md`，并在 `AGENTS.md` 或 `CLAUDE.md` 留消费入口。证据：[`setup-matt-pocock-skills/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/setup-matt-pocock-skills/SKILL.md#L63-L112)。
3. **局部关联**：Map → ticket、ticket → Map；implementation ticket 可指向 parent spec；ticket 之间有 blocking edges。
4. **ADR 冲突提示**：domain consumer guidance 要求发现输出与 ADR 冲突时显式报告，而不是静默覆盖：[`domain.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/setup-matt-pocock-skills/domain.md#L41-L51)。
5. **避免重复**：handoff 和 Wayfinder 都通过 context pointer 引用既有 artifact，不把全文复制到新的文档。

### 部分具备

1. **统一入口只有配置层，没有工作产物总索引**：`docs/agents/issue-tracker.md` 说明 tracker 怎么用，`docs/agents/domain.md` 说明 glossary/ADR 怎么读，但没有列出某个项目的所有 Map、spec、ticket set、ADR 和最终实现。
2. **关系多数是单向、局部的**：Map 会指向 decision ticket；ticket 可以指向 parent；但没有要求 final spec 回链 Map、ADR 回链源 decision、implementation ticket 回链 PR/commit/current docs。
3. **生命周期只覆盖各自局部状态**：ticket 能 close，ADR 可选 supersede，Map 有 fog/out-of-scope；没有统一的 historical/current/superseded/archived 分类纪律。
4. **主流程会消费 ADR，但不保证回写**：`to-spec`、`to-tickets`、`tdd` 会读取 glossary/ADR，`implement` 结束只要求 test、code-review、commit，没有 durable-doc closeout。证据：[`implement/SKILL.md`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/implement/SKILL.md#L7-L15)。

## 三、当前真正缺失的能力

### 1. 没有统一的 artifact registry

没有一份当前项目级文件回答：

- 哪个 Wayfinder Map 对应哪个 final spec；
- 哪组 implementation tickets 从哪个 spec 产生；
- 哪些 ADR/CONTEXT 变更来自哪些 decision；
- 哪个 PR/commit 实现了哪张卡；
- 哪些 artifact 是当前真相，哪些只是历史计划，哪些是 throwaway evidence。

这不等于一定要新增 registry；Issue Tracker 的关系能力本来就可以承担很多索引责任。缺口是系统没有验证这些关系是否被完整建立。

### 2. 没有跨文档/跨 tracker 的关联性审计

当前仓库没有 `/review-docs` 或等价 shipped skill，也没有脚本去检查：

- 指针目标是否还存在；
- Map 的 closed-decision 指针是否完整；
- spec → tickets 的 parent 关系是否完整；
- ADR 是否有明确来源 decision，或是否已被 supersede 却仍被当作 active；
- 同一长期事实是否同时存在于 historical spec 与 current docs 且互相冲突；
- research/prototype pointer 是否可达；
- artifact 是否成为孤儿。

仓库自己的 `package.json` 只有 changeset/version 脚本，`scripts/` 只有 skill 链接/列举工具；这不是下游项目的 artifact audit 机制。现有 [#307](https://github.com/mattpocock/skills/issues/307) 已准确提出 repository-wide docs/code/ADR alignment review，且仍然开放。

### 3. Wayfinder Map 没有完成后的治理

Wayfinder 明确“map clears 后交给 `to-spec`”，但没有要求：

- 在 Map 上留下 final spec pointer；
- 标记 Map 已 handed off / archived；
- 把 Map 的历史 decision 与最终 durable docs 做 reconciliation；
- 定期验证 Map 的链接和已关闭 ticket 仍可访问。

尤其是并行 branch/worktree 中，ticket resolver 产生的 `CONTEXT.md`、ADR 等可能没有进入共享基线。[#579](https://github.com/mattpocock/skills/issues/579) 已经逐条描述这个问题，因此不能再开同义 Issue。

## 四、为什么不应把所有卡片塞进一个统一长文档

一个固定“大总表”看起来方便，但会带来三类新问题：

1. **重复权威**：Issue Tracker 已经保存 Map/ticket/spec 状态，统一文档再复制一份就需要双写。
2. **破坏 artifact 边界**：`CONTEXT-MAP.md` 只管理 bounded contexts，不是任务/ADR/项目导航总表；Wayfinder Map 也只管理一次 effort 的 decision index。
3. **跨 tracker 不可移植**：GitHub、GitLab、Linear、本地 Markdown 的关系能力不同，强制一个目录会削弱现有 tracker abstraction。

更符合 Matt 设计哲学的形式不是“把内容集中”，而是：

```text
Configured artifact locations
        ↓ discover
Artifact roles and links
        ↓ verify
Dangling / orphaned / conflicting authority report
```

也就是 **统一检查关系，不统一复制内容**。

## 五、最小可贡献点

### 推荐：给 #307 增加一个 bounded 的 artifact-link integrity pass

建议将其作为 `/review-docs` 第一版中的一个可选检查分支，而不是独立大型框架：

1. 读取项目已有的 `docs/agents/issue-tracker.md`、`docs/agents/domain.md`、`AGENTS.md` / `CLAUDE.md`，发现真实 artifact 位置；
2. 将 artifact 分类为：
   - current authority（如 glossary、accepted ADR、用户文档）；
   - historical delivery record（spec、closed tickets）；
   - effort index（Wayfinder Map）；
   - temporary evidence（research/prototype branch、handoff）；
3. 只检查项目流程本来就声称存在的关系：pointer 是否可达、parent 是否存在、Map decision link 是否指向 closed/resolved ticket、superseded ADR 是否指向替代者；
4. 报告 dangling link、orphaned artifact、conflicting authority、unclassified artifact；
5. review-only：不自动移动、合并、归档或改写文档。

这比新增 `PROJECT_ARTIFACTS.md` 更小，也能兼容 Issue Tracker 作为主索引的项目。只有在真实项目缺少可发现入口、且用户明确需要人类可读导航时，才应建议一份轻量 index；它仍只放链接与角色，不复制内容。

### 若维护者认可，候选 PR 范围

在 #307 得到方向确认后，最小实现应围绕未来的 review skill，而不是修改所有生产 skill：

- 新增/修改 review-only skill 的 `SKILL.md`：加入 artifact discovery、role classification、link integrity、findings format；
- 同步对应 human-facing docs；
- 增加 changeset；
- 不新增固定文件名，不改变 Wayfinder、`to-spec`、`to-tickets` 的现有权威位置；
- Wayfinder worktree reconciliation 继续由 #579 单独解决。

## 六、与现有 Issues 的重复关系

| Issue | 重复程度 | 边界 |
|---|---:|---|
| [#560 documentation impact gate](https://github.com/mattpocock/skills/issues/560) | **部分重叠** | #560 解决“一次实现 closeout 时，durable changes 是否已回写长期真相”；本研究解决“多个既有 artifacts 的指针和角色是否长期保持一致”。前者是写入 gate，后者是 review/audit。不要把 audit 塞进 `/implement`。 |
| [#653 lightweight repository map](https://github.com/mattpocock/skills/issues/653) | **部分重叠** | #653 记录文件树看不出的代码结构、canonical editing surface、generated/deprecated paths；不是 delivery artifact registry。可共享“只放非显然关系、链接权威源”原则，但不要把任务、spec、ADR 全塞进 repository map。 |
| [#654 review-only test inventory](https://github.com/mattpocock/skills/issues/654) | **不重复** | #654 审计 requirement/risk/bug → executable test evidence；只可能把 spec/ADR 当作 test obligation 来源。 |
| [#656 downstream change-impact verification](https://github.com/mattpocock/skills/issues/656) | **不重复** | #656 是 changed module → downstream consumers → verification commands，不审计文档关系。 |
| [#657 loop completion boundary](https://github.com/mattpocock/skills/issues/657) | **不重复** | #657 定义 workflow 单次运行的 success signal/failure policy。 |
| [#660 executable contracts](https://github.com/mattpocock/skills/issues/660) | **不重复** | #660 管理跨团队单一可执行接口契约与兼容性测试。 |

另外三个更直接的上游入口：

- [#307 Documentation Review & Alignment Skill](https://github.com/mattpocock/skills/issues/307)：**直接覆盖** repository-wide docs/ADR/code drift 与结构审计；最小贡献应归入这里。
- [#579 Wayfinder durable context reconciliation](https://github.com/mattpocock/skills/issues/579)：**直接覆盖** ticket branch/worktree 产生的 ADR/CONTEXT 如何进入共享基线。
- [#212 PRD lifecycle](https://github.com/mattpocock/skills/issues/212)：已关闭，但记录了 spec 是历史计划还是 current truth 的产品问题；#560 已在其基础上明确“spec 作为历史交付记录，长期真相另有载体”。

## 最终判断

- **有没有固定放置规范？有，但按产物类型分散，不是统一放在 `docs/`。** 只有选择 local Markdown tracker 时，Map/spec/tickets 才集中到 `.scratch/`；使用 GitHub 时它们就在 Issues。
- **有没有统一关联管理？部分有。** Map/ticket、parent/blocker、glossary/ADR 消费路径有局部关系，但没有完整 artifact graph。
- **有没有关联性审计？没有 shipped 的通用能力。** #307 正是最接近的现有入口。
- **最值得贡献什么？** 在 #307 下提出并实现小型、review-only 的 artifact-link integrity pass；不新建同义 Issue，不创建固定四件套，不把所有卡片复制到一个总文档。
