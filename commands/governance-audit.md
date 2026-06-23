---
description: 只读审计当前项目的文档治理质量，检查四件套是否漂移、重复、虚构路径、指标未量、LOG 非追加；不修改任何文件。
argument-hint: "[可选路径或审计重点]"
---

调用 **docs-auditor** 子 agent，对当前工作目录做一次**只读文档治理审计**。

用户参数（可选）：`$ARGUMENTS`
- 不带参数：审计整个项目的四件套治理质量。
- 带路径：重点审计该子目录/模块与 `CLAUDE_MAP.md`、`PROJECT_STATUS.md` 是否一致。
- 带 `contract`：同时重点审计 `CONTRACT.md` 与前后端接口治理。

执行要求：

1. 只读扫描，不修改任何文件。
2. 先检查 `CLAUDE.md` / `CLAUDE_MAP.md` / `PROJECT_STATUS.md` / `PROJECT_LOG.md` 是否存在；不存在就报告缺失，不要创建。
3. 抽查 `CLAUDE_MAP.md` 里的路径是否真实存在。
4. 检查 `PROJECT_STATUS.md` 的指标是否像是实际量过；无法验证就标“未验证”。
5. 检查 `PROJECT_LOG.md` 是否保持历史流水账职责。
6. 如存在 `CONTRACT.md`，检查其是否和前后端接口位置形成单一真相源。
7. 输出审计报告：总体结论、P0/P1/P2 发现、证据、建议、待人工确认项。
