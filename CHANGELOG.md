# Changelog

本插件的版本变更记录。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [未发布]

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
