# GitHub 配置指南

## 快速配置

### 1. 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名: `my-skills`
3. 选择 "Public" 或 "Private"
4. 不要勾选 "Initialize with README"
5. 点击 "Create repository"

### 2. 推送本地仓库

```bash
cd ~/my-skills

# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/my-skills.git

# 推送
git push -u origin master
```

### 3. 验证

```bash
git remote -v
# 应显示:
# origin  https://github.com/你的用户名/my-skills.git (fetch)
# origin  https://github.com/你的用户名/my-skills.git (push)
```

## 日常使用

修改 skill 后，一键同步：

```bash
~/my-skills/sync-and-push.sh
```

这会：
1. 同步到 Codex 全局目录
2. 提交到本地 git
3. 推送到 GitHub

## 换电脑恢复

```bash
# 克隆仓库
git clone https://github.com/你的用户名/my-skills.git ~/my-skills

# 同步到 Codex
~/my-skills/sync-and-push.sh
```
