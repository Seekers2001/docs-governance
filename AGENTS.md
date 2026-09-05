# AGENTS.md — Codex 入口桥接

本仓库的共享项目章程以 `CLAUDE.md` 为唯一来源。开始实质工作前，读取并遵守 `CLAUDE.md`，同时读取 `PROJECT_STATUS.md` 顶部红线块；不要把这些规则复制进本文件。

需要定位文件、理解非显然路径、新建/删除/重命名文件时，先读取 `CLAUDE_MAP.md`。理解整体结构或改变 Module 权责、状态、Interface、依赖和核心流转时，再读取 `ARCHITECTURE.md`。追溯历史时按需检索 `PROJECT_LOG.md`。

Codex 安装入口是 `.codex-plugin/plugin.json`，Claude Code 安装入口是 `.claude-plugin/plugin.json`。两端共用 `skills/` 方法论；`commands/` 与 `agents/` 是 Claude Code 的交互适配层。
