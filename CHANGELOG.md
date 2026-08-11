# Changelog

本插件的版本变更记录。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [0.7.0] - 2026-08-02

### 新增
- 新增 `docs-governance` 总路由、`context-and-decisions` 与 `change-impact` 三个 Skill；Codex 可从一个入口按需进入 CONTEXT、ADR、契约、测试、回归和治理同步。
- 新增 CONTEXT / ADR 模板，并用 `docs/adr/` 记录本插件的 PROJECT_LOG SQLite 索引决策。
- 新增 `scripts/project-log-index.py`：按事件计数，超过 200 条后经确认归档旧事件，并从 Markdown 原文重建本地 SQLite 索引。
- 新增 `scripts/audit-docs.py` 及 spine/context/adr/artifacts/full 审计范围，检查断链、ADR 索引、LOG 完整性、TEST-ID 和孤儿文档。

### 变更
- 文档架构明确为“根脊柱 = 当前导航、可选文档 = 持久知识、Issue Tracker = 任务排期、SQLite = 机器投影”，所有目录按需懒创建。
- 成功标准留在 Spec/Issue 唯一来源；TESTS 关联证据，变更影响在实施前后核对迁移、回滚、实际 diff 和文档同步。
- `verify.sh` 新增总路由/README/使用说明一致性、派生数据库忽略、Python 编译和单元测试检查。

## [0.6.0] - 2026-08-02

### 新增
- 新增 `.codex-plugin/plugin.json`，将现有 skills 打包为 Codex / ChatGPT 可安装插件。
- 新增根目录 `AGENTS.md` 与 `templates/AGENTS.example.md` 薄桥接，让 Codex 读取共享 `CLAUDE.md` 章程而不复制规则。

### 变更
- 活文档、契约协作与模块回归 skills 增加 Codex 直接执行和宿主 agent 降级说明。
- README、使用说明与 day-0 初始化流程补充 Codex 安装、调用和 AGENTS 生成方式。
- 结构自检增加 Claude / Codex manifest 名称、版本和 skills 路径一致性检查。

## [0.5.0] - 2026-07-12

### 新增
- **第四条线·测试协作治理**（`test-collaboration` skill + `templates/TESTS.example.md`）：盘点项目现有测试资产，把需求、规则、风险和 Bug 转成 TEST-ID，维护必要、缺失、疑似重复、疑似废弃及可执行证据。v1 由当前会话直接使用 skill，不新增专用 agent、slash command 或执法脚本。

### 变更
- `module-regression` 和 `REGRESSION.example.md` 不再重复维护业务规则清单，改为引用 `TESTS.md` 的 TEST-ID；`/regression-audit` 继续只负责按台账运行本模块和下游命令并报告退出码。
- `/governance-retro` 的重复错误下沉候选改为登记到 `TESTS.md`。

## [0.4.0] - 2026-07-03

### 新增
- **第三条线·模块回归审计**（`module-regression` skill + `regression-auditor` agent + `/regression-audit` 命令 + `templates/REGRESSION.example.md`）：REGRESSION.md 台账登记每个模块的下游消费者（脚本从 import 生成、勿手改）与可执行回归验收命令（对账型优先），改完照单跑"本模块+全部下游"，退出码终审——防大项目"改一个模块悄悄弄坏其他模块"。铁律：判决=退出码 / 审计员只报不修 / 红着不准交付。

### 新增
- `templates/pre-commit.example`：pre-commit 护栏——固化"含代码改动的 commit 必须同批 staged 一行 PROJECT_LOG.md"（测试/文档/治理文件豁免，`--no-verify` 应急后门）；`/governance-init` 自动装，`/governance` 对已有 git 项目询问安装。（backlog #2）

## [0.3.0] - 2026-07-02

### 新增
- `/governance-init` 命令 + `templates/governance.example.md`：全新空项目的 day-0 治理骨架——精简 CLAUDE.md（含 Git 自动执行+硬禁单 / 失败自检三问 / references 触发规则）+ docs/governance.md（4 步检查流程 + 三层验收）+ PROJECT_LOG.md + 目录骨架。刻意不生成 MAP/STATUS（防空壳占位符出生即漂移），项目长起来后用 `/governance` 升级；与 `/governance` 双向指路。
- `loop-design-check` skill：写 loop（该不该建 → 可判定目标 → 回路类型 → plan/build/judge 骨架）+ 体检 loop（五个崩法防呆 + 判断留人红线）。英文版已被 ECC 上游合并（affaan-m/ECC #2381）。

## [0.2.0] - 2026-06-23

### 新增
- **活文档治理**（`living-docs-governance` skill + `docs-governor` / `docs-auditor` agent + `/governance` `/governance-audit` `/governance-sync` 命令）：四件套（CLAUDE.md / CLAUDE_MAP.md / PROJECT_STATUS.md / PROJECT_LOG.md）+ 分级读取协议 + 文档角色分层。
- **契约式前后端协作**（`contract-first` skill + `contract-director` / `frontend-dev` / `backend-dev` agent + `/contract` 命令）：一份 CONTRACT.md 当唯一真相源，支持单会话多 agent 与多终端异步两种模式（CDC / 契约测试）。
- `templates/`：四件套 + CONTRACT 空白模板。
- `references/governance-sync-matrix.md`：阶段收尾的查漏补缺矩阵。
- `hooks/check-on-stop.sh`：会话结束治理提醒（提醒型，未强制阻断）。
- `scripts/verify.sh`：插件结构完整性自检（JSON 可解析 / hook 可执行 / 命令→agent→skill/template/reference 不断链）。

### 改进
- `CLAUDE_MAP.md` 模板瘦身：删掉目录树镜像，只留"树看不出来"的四类（依赖方向 / 非显然定位 / 误导清单 / 别动区）。
- 分级读取协议：CLAUDE 全文常驻、STATUS 仅红线块常驻、MAP 默认按需、LOG 按需 + 改文件前必读护栏。

### 已验证
- 在真实项目「经营报表加工」「礼仪课程 demo」上跑通审计（读）与修复（写），捕获并校正 STATUS 指标漂移、脊柱职责越界、误导目录未标注等问题。
