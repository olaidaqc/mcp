# My Skills - AI Workflow 中心

个人 Claude/Codex Skill 管理中心，集成 Mysti 多 Agent 协作 + VSCode 可视化。

## 快速开始

### 1. 一键配置（自动）

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy Bypass -Scope Process
& "$env:USERPROFILE\my-skills\setup-workflow.ps1"
```

### 2. 配置完成后的快捷命令

| 命令 | 作用 |
|------|------|
| `ss` | 同步 skills 到 Codex + GitHub |
| `sd` | 进入开发目录 |
| `sh` | 进入 skill 主页 |
| `mystistart` | 启动 Mysti |

### 3. VSCode 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Shift+S` | 一键 commit & push |
| `Ctrl+Shift+T` | 打开任务看板 (Todo Tree) |
| `Ctrl+Shift+M` | 打开 Mysti |
| `Ctrl+Shift+B` | Brainstorm Mode |

## 目录结构

```
my-skills/
├── superpowers/              # Superpowers 技能集
│   ├── brainstorming/        # 语音版头脑风暴
│   │   ├── SKILL.md         # 完整版
│   │   └── SKILL-OPTIMIZED.md  # Token 优化版
│   └── ...
├── mysti-config.json         # Mysti 多 Agent 配置
├── setup-workflow.ps1        # 一键配置脚本
├── sync-and-push.sh          # 同步脚本
├── token-monitor.md          # Token 预算监控
└── README.md                 # 本文件
```

## 工作流程

### 日常开发

```bash
# 1. 进入开发目录
sd

# 2. 在 VSCode 中编辑 skill

# 3. 一键同步
ss
```

### 使用 Mysti 多 Agent

```bash
# 启动 Mysti
mystistart

# 在 VSCode 中:
@claude @codex Review this design
# 或按 Ctrl+Shift+B 启动 Brainstorm Mode
```

## Token 优化

### 自动节省 Token 的机制

1. **Mysti 内置**: 上下文压缩、Skill 懒加载、历史压缩
2. **配置预算**: 8000 警告，12000 限制
3. **优化版 Skill**: 简单任务用精简版

### 何时使用优化版

```markdown
简单任务 / Token 紧张 → SKILL-OPTIMIZED.md
复杂设计 / 需要深度 → SKILL.md (完整版)
```

## 集成说明

### Mysti + Superpowers 关系

```
Mysti (VS Code 扩展)
    ↓ 调用
Claude Code CLI → 读取 ~/.claude/ 配置
    ↓ 使用
Superpowers Skill (本项目)
```

**Mysti 不会替换你的 skill，而是增强调用方式。**

## 同步到 GitHub

首次配置：
```bash
cd ~/my-skills
gh repo create my-skills --public
git push -u origin main
```

后续同步：
```bash
ss  # 一键同步
```

## 系统要求

- VSCode 1.85+
- Claude Code CLI
- Codex CLI
- PowerShell 7+ (Windows)

## 故障排除

| 问题 | 解决 |
|------|------|
| Mysti 不显示 | 检查 mysti-config.json 路径 |
| Skill 不生效 | 运行 `ss` 同步 |
| Token 超支 | 查看 token-monitor.md |

## 更新日志

- 2026-02-19: 添加 Mysti 集成 + Token 优化
- 2026-02-18: 初始配置 + Voice Support

## MCP 管理网页 (Web UI)

启动：
```powershell
cd web_mcp_manager
start-web.bat
```

访问：
```
http://127.0.0.1:8765
```

说明：
- 页面包含：状态、快捷操作、实时日志
- 命令定义在 `web_mcp_manager/config/commands.json`
- 日志写入 `%USERPROFILE%\my-skills\runtime.log`
