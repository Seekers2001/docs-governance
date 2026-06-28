# docs-governance

> 一个 Claude Code 插件，用「文档驱动开发」治理 AI 协作项目：把项目拆成各司其职的小文档，AI 照文档干活，并持续防止文档随代码腐烂。

## 为什么需要它

AI 让代码变得**便宜、可丢弃、可再生**。当写代码不再是瓶颈，承重的东西就上移到**意图（文档）**和**验证（测试）**——人维护的是规格和验收，代码只是规格的一次投影。

但这套范式有个最容易塌的地方：**文档会腐烂**。README 撒谎、架构图描述一次没上线的重构、AI 每次进会话都在重新摸索本该一读就懂的结构。**docs-governance 专门治这个腐烂。**

它和 Claude 生态里的 onboarding 类工具是**互补**的：`codebase-onboarding` 解决"第一次进场"，**本插件解决"几个月后那张图还为不为真"**——维护期的持续治理。

## 它怎么治

把项目文档当成一个**小系统**：四份各司其职、互不重叠的「脊柱」文档，加一套**分级读取协议**（不每次全读，省上下文），再把脊柱之外的所有文档按角色分层、按需读。

| 脊柱文档 | 唯一职责 | 进会话怎么读 |
|---|---|---|
| `CLAUDE.md` | 宪法：永久硬规则 + 指路牌 | 全文常驻 |
| `CLAUDE_MAP.md` | 地图：只记**文件树看不出来**的（依赖方向 / 误导清单 / 别动区） | 默认不读，改文件前必读 |
| `PROJECT_STATUS.md` | 健康仪表盘：指标 + 删除区 + P0 | 只有红线块常驻 |
| `PROJECT_LOG.md` | 流水账：只追加的历史 | 按需 grep |

> 关键纪律：**每个事实只活在一份文档里**（非重叠）；脊柱只放索引和指路牌，细节下沉到对应层；"不读会悄悄出事"的红线常驻，其余按需。

另配一条**契约式前后端协作**线（`contract-first`）：一份 `CONTRACT.md` 当前后端唯一真相源，防字段漂移导致集成白屏——本质是轻量的**消费者驱动契约（CDC）/ 契约测试**，支持单会话多 agent 和多终端异步两种模式。

## 治理常见错误（dogfood 里反复撞到的）

| 错误 | 正确做法 |
|---|---|
| STATUS 撒谎（指标停在旧快照、说"无 git"其实早建了） | STATUS 只写量过的当前真相，旧事实移进 LOG |
| 血肉上浮：脊柱里混进目录树镜像 / 逐条历史 / 整篇产物 | 脊柱只留索引和指路牌，细节下沉到对应层 |
| CLAUDE_MAP 抄文件树（`ls` 就有、还会过期） | MAP 只记树看不出来的：依赖方向 / 误导清单 / 别动区 |
| 孤儿文档：有 `.md` 没人从脊柱指向它 | 挂上指路牌，否则没人读必烂 |
| 每次进会话全读四份，白占上下文 | 分级读：红线常驻，其余按需 |
| 一上来铺满四件套（小项目过度治理） | 渐进式采用，按预警信号上下一级 |
| 个人偏好塞进团队 `CLAUDE.md` | 放 `CLAUDE.local.md` / `~/.claude/` |

## 真实使用案例（dogfood，非演示）

| 项目 | 跑了什么 | 抓到什么 |
|---|---|---|
| 经营报表加工（324 个 .py） | `/governance-audit` | CLAUDE_MAP 长到 143 行、抄目录树、跟 STATUS 抢职责 |
| 礼仪课程 demo（59 个 .js，Node） | 审计 + 修复 | STATUS 三项指标漂移（style.css 标 443 实为 605）、6 个误导备份目录未标注、CLAUDE.md 指路牌指向废弃文件——全部修正，留有 git diff |
| 本插件自身 | 套自己的四件套 + `scripts/verify.sh` | 用自己的方法论治自己，结构自检全绿 |

## 安装

把本目录作为本地插件加载（已注册为 directory 来源即可），或把 `skills/` `agents/` `commands/` 软链到 `~/.claude/` 对应目录。

## 用法

```
# 活文档治理
/governance              # 扫项目，生成/更新四件套
/governance-audit        # 只读审计：哪儿漂移了，不动文件
/governance-sync         # 阶段收尾：按矩阵查漏补缺该同步哪份文档

# 契约式前后端协作
/contract 做订单详情页    # 先判模式，再定契约 → 各端开发 → 集成对账
```

## 结构

```
docs-governance/
├── CLAUDE.md / CLAUDE_MAP.md / PROJECT_STATUS.md / PROJECT_LOG.md  # 插件自治理（dogfood）
├── .claude-plugin/{plugin,marketplace}.json
├── skills/{living-docs-governance,contract-first,loop-design-check}/SKILL.md         # 方法论唯一源
├── agents/{docs-governor,docs-auditor,contract-director,frontend-dev,backend-dev}.md
├── commands/{governance,governance-audit,governance-sync,contract}.md
├── templates/*.example.md                                          # 给用户项目套的空白模板
├── references/governance-sync-matrix.md
├── hooks/{check-on-stop.sh,hooks.json}                             # 会话结束治理提醒
└── scripts/verify.sh                                               # 结构完整性自检
```

> skill = 方法论（唯一源），agent = 照方法论干活的人，command = 按钮，template = 空白表格。方法论只写在 skill 里，agent 不复制——**一个防文档漂移的插件，自己内部先不漂移。**

## 开发

改任何文件后、提交前跑 `bash scripts/verify.sh`（检查 JSON 可解析、hook 可执行、命令→agent→skill/template/reference 不断链）。

---
MIT · Seekers2001（小磊）· jiaxinleifm@outlook.com
