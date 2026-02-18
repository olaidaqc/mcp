#!/bin/bash
# AI Workflow 自动激活与检测脚本

echo "==================================="
echo "  AI Workflow 自动激活与检测"
echo "==================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# 检测函数
check_item() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} $2"
        ((FAIL++))
    fi
}

echo "[1/8] 检测 CLI 工具..."
claude --version > /dev/null 2>&1
check_item $? "Claude Code CLI"

codex --version > /dev/null 2>&1
check_item $? "Codex CLI"

echo ""
echo "[2/8] 检测 Skill 文件..."
[ -f "$HOME/my-skills/superpowers/brainstorming/SKILL.md" ]
check_item $? "Brainstorming SKILL.md"

[ -f "$HOME/my-skills/superpowers/brainstorming/SKILL-OPTIMIZED.md" ]
check_item $? "Brainstorming SKILL-OPTIMIZED.md"

echo ""
echo "[3/8] 检测 Mysti 配置..."
[ -f "$HOME/my-skills/mysti-config.json" ]
check_item $? "mysti-config.json"

echo ""
echo "[4/8] 检测 VSCode 配置..."
[ -f "$HOME/.vscode/settings.json" ]
check_item $? "VSCode settings.json"

[ -f "$HOME/.vscode/keybindings.json" ]
check_item $? "VSCode keybindings.json"

echo ""
echo "[5/8] 同步 Skills 到 Codex 全局目录..."
if [ -d "$HOME/my-skills/superpowers" ]; then
    mkdir -p "$HOME/.agents/skills"
    rm -rf "$HOME/.agents/skills/superpowers" 2>/dev/null
    cp -r "$HOME/my-skills/superpowers" "$HOME/.agents/skills/"
    [ -d "$HOME/.agents/skills/superpowers/brainstorming" ]
    check_item $? "Skills 同步成功"
else
    check_item 1 "Skills 同步失败"
fi

echo ""
echo "[6/8] 检测 Git 配置..."
cd "$HOME/my-skills"
git status > /dev/null 2>&1
check_item $? "Git 仓库正常"

echo ""
echo "[7/8] 检测 VSCode 扩展..."
check_ext() {
    code --list-extensions 2>/dev/null | grep -i "$1" > /dev/null
    check_item $? "$2"
}

check_ext_optional() {
    if code --list-extensions 2>/dev/null | grep -i "$1" > /dev/null; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASS++))
    else
        echo -e "${YELLOW}○${NC} $2 (未安装，可选)"
    fi
}

echo "  检查已安装扩展..."
check_ext "todo-tree" "Todo Tree"
check_ext_optional "mysti" "Mysti"

echo ""
echo "[8/8] 检测快捷键配置..."
[ -f "$HOME/.vscode/keybindings.json" ] && grep -q "ctrl+shift+s" "$HOME/.vscode/keybindings.json"
check_item $? "一键提交快捷键 (Ctrl+Shift+S)"

echo ""
echo "==================================="
echo "  检测结果"
echo "==================================="
echo -e "通过: ${GREEN}$PASS${NC}"
echo -e "失败: ${RED}$FAIL${NC}"

if [ $FAIL -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ 所有检测通过！配置已激活。${NC}"
    echo ""
    echo "快速开始:"
    echo "  1. 打开 VSCode"
    echo "  2. 安装扩展: DeepMyst.mysti (如未安装)"
    echo "  3. 按 Ctrl+Shift+S 一键提交代码"
    echo "  4. 按 Ctrl+Shift+T 打开任务看板"
    echo "  5. 按 Ctrl+Shift+M 打开 Mysti"
    echo ""
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠ 部分检测失败，请检查上述项目${NC}"
    exit 1
fi
