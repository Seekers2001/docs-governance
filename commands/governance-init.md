---
description: 给全新（还没代码的）项目搭 day-0 治理骨架：精简 CLAUDE.md + docs/governance.md 检查流程 + PROJECT_LOG.md + 目录骨架，并 git init 首提。已有代码的项目请用 /governance。
argument-hint: "[项目名 技术栈 模块划分]"
---

给**当前工作目录的全新项目**搭 day-0 治理骨架。

**分工（别用错命令）**：项目已有代码 → 用 `/governance`（扫描真实结构生成/更新四件套）；**空项目从零起步 → 用本命令**。本命令刻意只生成"三件 + 骨架"，不铺满四件套——渐进式采用，见 living-docs-governance skill。

用户参数：`$ARGUMENTS`（项目名 / 技术栈 / 模块划分）。缺什么就逐项问，**不要猜技术栈**。

## 生成什么

### 1. `CLAUDE.md`（宪法，≤60 行）

以 `templates/CLAUDE.example.md` 为骨架（读取时机分级 / 硬规则少而精 / 路标），按本项目填充，并加入以下 day-0 段落：

- **治理硬约束**（放最前）：更新任何文件 / 新建文件 / 改业务规则前，必须读取并执行 `docs/governance.md`；无视 = 违反章程，必须重做。
- **验证**（按技术栈生成，禁止照抄别的语言）：如 Python 项目 `python -m py_compile` + `ruff check`；Node 项目 `npx tsc --noEmit` + `npm test`；改主程序后跑最小启动命令。
- **Git 规则（自动执行 + 硬禁单）**：
  - 自动执行：初始化后 `git init` + 首提；文档生成后、模块验证通过后、修 bug 后按型提交；commit message 用英文。
  - 硬禁单（绝对禁止自动执行）：`git add -A` / `git add .`（只 add 具体文件）、`git push`（人工触发）、`git reset --hard`、`git push -f`、`git branch -D`、`git checkout -- .`、`git commit --amend`、`git rebase -i`。
- **代码完成后检查（强制）**：跑本项目验证命令 → 精简一遍再验证 → 有审查手段就审查（CRITICAL 必须修）→ 对照 `docs/{模块}-spec.md` 验收标准逐条核对 → 按 `docs/governance.md` §2 步骤 3.5 做实际运行验证（产物型任务必检产物本身）→ 全过才 commit，没过不许 commit。
- **失败自检（强制）**：操作失败不要直接重试，先答三问——缺信息？缺工具？缺约束？→ 告诉用户缺什么。
- **文档结构指路**：`docs/{模块}-spec.md`（需求/验收标准）、`docs/{模块}-plan.md`（方案/已知坑）、`references/`（已验证参考实现）。**references/ 触发规则**：遇外部 API / 复杂转换 / 图像文件批处理等高不确定实现，先建 references/ 最小跑通版，再写正式代码；禁止从纯文字描述直接实现。

### 2. `docs/governance.md`

**从 `templates/governance.example.md` 复制**，只替换 `{项目名称}`，placeholder 留给项目演化中填。不要内嵌改写模板正文。

### 3. `PROJECT_LOG.md`

**照 `templates/PROJECT_LOG.example.md` 的格式**建新文件，只留一行：`## [今天日期] init | /governance-init 项目初始化`。示例行不要抄进去。

### 4. 目录骨架（只建空目录，不建文件）

`src/ tests/ docs/ references/ logs/ output/`（目录名按技术栈惯例调整；`output/` 与 `logs/` 提醒用户加进 .gitignore）。

### 5. git init + 首提

`git init` → 只 add 刚生成的具体文件 → `git commit -m "init: project governance scaffold"`。不 push。

## 刻意不生成的（防出生即漂移）

- **CLAUDE_MAP.md / PROJECT_STATUS.md**：空项目没有值得记的依赖方向和健康指标，生成出来全是占位符=假文档。等预警信号出现（AI 开始找不到东西 / 重复踩坑 / 该删的又被重建）再跑 `/governance` 升级到四件套。
- **项目级 hook**：本插件自带的 Stop hook（`hooks/check-on-stop.sh`）检测到治理文件就自动生效，无需项目级 settings.json。

## 收尾汇报

列出：建了哪几个文件（真实路径）、CLAUDE.md 行数（超 60 行说明为什么）、git 首提的 commit id、下一步建议（写第一个 `docs/{模块}-spec.md` → 建 references/ 最小跑通版 → 写代码）。不要谎报"完成"。
