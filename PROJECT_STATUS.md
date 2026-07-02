# PROJECT_STATUS.md — 插件健康仪表盘

> 红线块每次进会话必读；指标按需。

## 🔴 红线块（每次必读 —— 删除区 + 未决 P0）

### 删除区（故意删的，别重建）
- 暂无

### 未决 P0
- `/governance-init` 尚未在真实空项目上端到端首跑（2026-07-02 新增命令，逻辑齐但没实测）。
- `loop-design-check` skill 与两条主线主题不合（小磊已确认"没关系"），挪出待拍板。

## 📥 Backlog（方法论优化，2026-07-02 小磊逐条批准；等 dogfood 撞到或排期再做，不抢跑）

1. **审计事实层下沉成脚本**：`health.sh` 查路径存在/标称行数 vs 实测/LOG 改历史，退出码终审；LLM 只留语义层（矛盾/越界），判断留人。STATUS 可量化指标改为脚本自动生成。
2. ✅ **commit 前固化核对**（2026-07-02 已做：templates/pre-commit.example + 两命令接入 + 四段测试）：staged 含代码改动 → PROJECT_LOG.md 必须同批 staged；豁免=只改 tests//docs//治理文件 或 --no-verify；做成 templates/pre-commit.example，/governance-init 自动装。只拦这一条最小可判定不变量，MAP/STATUS 不在 commit 关口硬卡（防狼来了）。
3. **LOG 消费端**：audit 增加 fix 热点统计（grep fix 按模块聚合），流水账变复盘数据源。
4. **四件套并发约定**：LOG append-only 各写各行；STATUS/MAP 指定"谁拥有谁改"（同契约线"谁改契约谁是主任"）。
5. **文档复利三动作**（skill 加一节"文档作为再生产资料"）：① 跑通即存 references/ ② LOG fix 热点 ≥2 次的坑升级成 CLAUDE.md 硬规则 ③ ≥2 项目重复的 spec/references/placeholder 回流模板母版。

## 指标（按需读）

| 指标 | 现在 | 阈值 | 状态 |
|---|---|---|---|
| `scripts/verify.sh` | 通过 | 通过 = 绿 | 🟢 |
| skill / agent 内部去重 | 是（方法论仅 skill 一处） | 唯一源 | 🟢 |
| 真实项目 dogfood | 4（经营报表审计、礼仪 demo 审计+修复、本插件自治理、audit-blog 审计） | ≥2 | 🟢 |
| 可发布底座 | git / LICENSE / CHANGELOG / .gitignore / verify 齐 | 齐 = 绿 | 🟢 |
| README 安装/样例 | 市场安装命令 + 验收命令 + 真实审计样例（2026-07-02 补） | 齐 = 绿 | 🟢 |
