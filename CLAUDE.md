# CLAUDE.md — docs-governance 插件自治理（用自己的方法论治自己）

> 进会话读取（分级）：本文件全文 + `PROJECT_STATUS.md` 红线块；MAP / LOG 按需。
> 本插件**刻意保持轻量治理**——它自己的 skill 写着"别给小项目过度治理"，这套四件套就是个**薄示范**，别往里堆。

## 硬规则
- **方法论唯一源在 skill**（`living-docs-governance` / `contract-first`）；agent / command 只指过去，**不复制方法论**（防插件自己内部漂移）。
- 改任何文件后、提交前：跑 `bash scripts/verify.sh`，**绿了才提交**。
- 文件名 kebab-case；正文中文，英文仅保留 skill description 里的触发词。
- commit message 用英文；`git push` 等小磊说。

## 路标
- 结构 / 依赖 / 误导 → `CLAUDE_MAP.md`
- 当前健康 / 待办 → `PROJECT_STATUS.md`
- 改了什么 → `PROJECT_LOG.md`
- 方法论本体 → `skills/*/SKILL.md`
- 给用户怎么用 → `README.md` / `使用说明.md`
