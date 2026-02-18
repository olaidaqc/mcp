#!/bin/bash
# 自动同步 skill 到 Codex 并提交到 GitHub

echo "=== Skill 同步脚本 ==="

# 1. 同步到 Codex 全局目录
echo "[1/4] 同步到 ~/.agents/skills/..."
cp -r ~/my-skills/superpowers ~/.agents/skills/ 2>/dev/null || echo "superpowers 已同步"
ls ~/.agents/skills/

# 2. 添加所有修改到 git
echo ""
echo "[2/4] 添加修改到 git..."
cd ~/my-skills
git add -A
git status --short

# 3. 提交（如果有修改）
echo ""
echo "[3/4] 提交修改..."
if git diff --cached --quiet; then
    echo "没有需要提交的修改"
else
    git commit -m "Update skills: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "已提交"
fi

# 4. 推送到 GitHub（如果配置了远程）
echo ""
echo "[4/4] 推送到 GitHub..."
if git remote get-url origin 2>/dev/null; then
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "推送失败，请检查远程配置"
    echo "已推送到 GitHub"
else
    echo "未配置 GitHub 远程仓库，请先运行:"
    echo "  git remote add origin https://github.com/你的用户名/my-skills.git"
fi

echo ""
echo "=== 同步完成 ==="
