# My Skills 仓库

个人 Claude/Codex Skill 管理中心，自动同步到 GitHub。

## 目录结构

```
my-skills/
├── superpowers/          # Superpowers 技能集
│   ├── brainstorming/    # 增强版头脑风暴（含语音支持）
│   ├── writing-plans/
│   └── ...
├── sync-and-push.sh      # 一键同步脚本
└── README.md
```

## 使用方法

### 1. 修改 skill

直接编辑 `~/my-skills/` 下的文件。

### 2. 同步并提交

```bash
# 一键同步到 Codex + 提交到 GitHub
~/my-skills/sync-and-push.sh
```

### 3. 在任意项目使用

```bash
cd 任意项目目录
codex
# skill 自动生效
```

## GitHub 配置（首次）

```bash
cd ~/my-skills

# 配置 GitHub 远程仓库
git remote add origin https://github.com/你的用户名/my-skills.git

# 首次推送
git push -u origin main
```

## Token 优化说明

### 什么消耗 token？

| 操作 | 消耗 Token？ | 说明 |
|------|-------------|------|
| 编辑 skill 文件 | ❌ 否 | 本地操作 |
| 同步到 Codex | ❌ 否 | 文件系统操作 |
| 提交到 GitHub | ❌ 否 | git 操作 |
| AI 读取 skill | ✅ 是 | 每次会话按需加载 |

### 如何减少 token 消耗？

1. **精简 skill 文件** - 删除冗余描述
2. **拆分大 skill** - 一个 skill 专注一个功能
3. **使用 cross-reference** - 引用其他 skill，不重复内容
4. **避免频繁修改** - 稳定后再大量使用

### Token 预算估算

假设使用 GPT-4（$0.03/1K tokens）：

| 场景 | 单次消耗 | 100 次成本 |
|------|---------|-----------|
| 加载 brainstorming skill | ~1000 tokens | $3.00 |
| 完整 workflow（5 skills）| ~5000 tokens | $15.00 |

## 自动同步（可选）

添加 alias 到 `.bashrc` 或 `.zshrc`：

```bash
# 保存 skill 后自动同步
alias skillsave='~/my-skills/sync-and-push.sh'
```

## 备份与恢复

由于已配置 GitHub，skill 自动备份。

换电脑时恢复：
```bash
git clone https://github.com/你的用户名/my-skills.git ~/my-skills
~/my-skills/sync-and-push.sh
```
