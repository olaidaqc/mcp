# Token 预算监控

## 当前配置

| 工具 | 单次预算 | 警告阈值 | 限制阈值 |
|------|---------|---------|---------|
| Mysti | 8000 | 8000 | 12000 |
| Claude | - | 100K | 200K |
| Codex | - | 50K | 100K |

## Skill Token 成本

| Skill | 估算 Token | 成本 (GPT-4) |
|-------|-----------|-------------|
| brainstorming (完整版) | ~1500 | $0.045 |
| brainstorming (优化版) | ~800 | $0.024 |
| writing-plans | ~2000 | $0.06 |
| test-driven-development | ~1200 | $0.036 |

## 节省 Token 策略

1. **简单任务** → 用优化版 skill
2. **复杂设计** → Brainstorm Mode (Debates 更值)
3. **日常代码** → 单 Agent
4. **代码审查** → @claude @codex 双审

## 监控命令

```bash
# 查看今日消耗（估算）
claude stats

# Mysti 内置监控
# 达到 8000 自动警告，12000 自动停止
```
