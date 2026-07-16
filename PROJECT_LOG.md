# PROJECT_LOG.md — 只追加（永不改旧行）

## [2026-06-23] init | 建立插件可发布底座：git 初始化 + LICENSE(MIT) + CHANGELOG + .gitignore(排 .DS_Store) + scripts/verify.sh（结构完整性自检，实跑通过）
## [2026-06-23] init | 给插件自身套精简版四件套（dogfood，用自己的方法论治自己）
## [2026-06-23] audit | verify.sh 首跑全绿：JSON 合法 / hook 可执行 / 命令→agent→skill/template/reference 无断链
## [2026-06-24] feat | 借鉴 @vincemask《.claude/ 组织指南》补 4 处：skill 加「渐进式采用路径（带下一级预警信号）」+「团队 vs 个人分层」；README 加「治理常见错误」表；docs-auditor 扩到也审 .claude/ 配置目录本身（死配置/CLAUDE.md过载/模糊命名/个人混团队）
## [2026-06-24] audit | audit-blog 真项目治理审计跑通（可信度低，揪出 STATUS 自相矛盾/旧快照、MAP 导航6→7、README 描述已删架构等 ~14 条）——第 4 个 dogfood
## [2026-06-28] feat | 新增 skill `loop-design-check`：把任务写成目标导向 loop（该不该建→可判定目标→回路类型→plan/build/judge 骨架）+ 体检 loop（五个崩法防呆+判断留人红线），防空转/作弊/跑飞。源自 vault《控制论×Loop×Goal》；机制层引用 ECC autonomous-loops/continuous-agent-loop 不重写
## [2026-07-02] feat | /governance-init day-0 骨架命令 + governance.example.md 模板（模板单源、瘦身三件、hook 交给插件 Stop、去悬空引用/去 Python 写死/去私有约定）；plugin 0.3.0，CHANGELOG 补 loop-design-check
## [2026-07-02] fix | verify.sh 修两伤：skills 断链漏检（MISS 正则 + 扫描范围扩到 README/使用说明/CLAUDE_MAP，三段测试证伪→证真）+ agent 白名单硬编码改动态"孤儿/未登记"检查；README 补市场安装命令+验收命令+真实审计样例；发布 v0.3.0
## [2026-07-02] governance | 方法论优化 backlog 五条立项（审计脚本化/pre-commit 固化/LOG 消费端/并发约定/文档复利三动作），方案细节见 STATUS Backlog
## [2026-07-02] feat | backlog #2 落地：templates/pre-commit.example 护栏（代码改动必须同批一行流水账；测试/文档豁免；--no-verify 后门）+ /governance-init 自动装 + /governance 询问装；临时仓四段测试全过（拦/带账过/豁免过/后门过）
## [2026-07-03] feat | 第三条线·模块回归审计首版：module-regression skill（台账三要素/审计五步/三铁律）+ regression-auditor agent（只跑只报不修）+ /regression-audit 命令（init 建台账草稿）+ REGRESSION.example 模板；plugin 0.4.0；未真项目实测，待经营报表试点

## [2026-07-03] feat | 吸收「熵与法典」九层判定思想：module-regression 加判定点清单+铁律4坑必下沉；governance-audit 改两段流水线（新增 scripts/audit-cheap.sh 便宜层先跑红了短路）；living-docs 加标准变更留痕+LOG蒸馏升级为蒸馏+复盘；新增 /governance-retro（LOG复盘统计→下沉候选）；STATUS 模板加审计保鲜度。修 audit-cheap.sh bash3 多字节变量名吞并 bug（$VAR后紧跟中文标点须${VAR}）。

## [2026-07-12] feat | 测试协作治理 v1：新增 test-collaboration skill + TESTS.example 模板，盘点现有测试并把需求/Bug 转成 TEST-ID；REGRESSION.md 改为只管下游与回归命令并引用 TEST-ID；plugin 0.5.0，待真实项目试点
