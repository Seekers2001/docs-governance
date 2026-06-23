# PROJECT_STATUS.md — 插件健康仪表盘

> 红线块每次进会话必读；指标按需。

## 🔴 红线块（每次必读 —— 删除区 + 未决 P0）

### 删除区（故意删的，别重建）
- 暂无

### 未决 P0
- 发布前补 `README` 的"故事"段：文档+测试驱动 thesis + vs ECC（codebase-onboarding 管"前"、本插件管"维护期"）差异化。
- 发布前补：安装截图、命令示例、失败边界。

## 指标（按需读）

| 指标 | 现在 | 阈值 | 状态 |
|---|---|---|---|
| `scripts/verify.sh` | 通过 | 通过 = 绿 | 🟢 |
| skill / agent 内部去重 | 是（方法论仅 skill 一处） | 唯一源 | 🟢 |
| 真实项目 dogfood | 3/3（经营报表审计、礼仪 demo 审计+修复、本插件自治理） | ≥2 | 🟢 |
| 可发布底座 | git / LICENSE / CHANGELOG / .gitignore / verify 齐 | 齐 = 绿 | 🟢 |
