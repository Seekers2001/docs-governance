# governance-init 空项目首跑证据

- 日期：2026-08-13
- 范围：`commands/governance-init.md` 的 Codex 共享流程
- 临时项目：`/private/tmp/governance-init-smoke.yY0ID8`
- 结果：通过

## 输入

- 项目名：`governance-init-smoke`
- 技术栈：Python
- 模块：无业务模块
- 宿主：当前 Codex 按 `commands/governance-init.md` 直接执行

## 生成结果

首提只包含以下四个文件：

- `AGENTS.md`
- `CLAUDE.md`
- `PROJECT_LOG.md`
- `docs/governance.md`

`.git/hooks/pre-commit` 已安装且具有可执行权限。`CLAUDE.md` 为 31 行，没有超过 60 行限制。

未生成 `CLAUDE_MAP.md`、`PROJECT_STATUS.md`、`ARCHITECTURE.md`、`CONTEXT.md`、`CONTRACT.md`、`TESTS.md` 或 `REGRESSION.md` 空壳。

## Git 证据

- 首提：`6aac7c3 init: project governance scaffold`
- 提交数：1
- 提交后工作区：干净

## 验证

以下检查均通过：

1. 必需文件存在。
2. 可选治理载体没有提前生成。
3. pre-commit hook 存在且可执行。
4. `python3 -m compileall -q <临时项目>` 返回 0。
5. 首提成功且提交后无未提交改动。

## 尚未覆盖

本次证明共享 day-0 流程可由 Codex 在真实空仓执行，不等于 Claude Code 原生 slash command 已通过。当前机器安装的 `docs-governance` 旧版插件处于禁用状态；用当前仓库作为临时插件目录发起真实模型调用需要把私有仓库上下文发送到外部服务，因未获得明确的数据出境授权而未继续。
