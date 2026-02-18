# VSCode + Mysti + Skills 一键配置脚本
# 运行方式: PowerShell -ExecutionPolicy Bypass -File setup-workflow.ps1

Write-Host "=== AI Workflow 自动化配置 ===" -ForegroundColor Cyan

# 1. 检查 CLI 工具
Write-Host "`n[1/5] 检查 CLI 工具..." -ForegroundColor Yellow
$claude = Get-Command claude -ErrorAction SilentlyContinue
$codex = Get-Command codex -ErrorAction SilentlyContinue

if ($claude) { Write-Host "  ✓ Claude Code 已安装" -ForegroundColor Green }
else { Write-Host "  ✗ Claude Code 未安装 (npm install -g @anthropic-ai/claude-code)" -ForegroundColor Red }

if ($codex) { Write-Host "  ✓ Codex 已安装" -ForegroundColor Green }
else { Write-Host "  ✗ Codex 未安装 (npm install -g @openai/codex)" -ForegroundColor Red }

# 2. 同步 Skills
Write-Host "`n[2/5] 同步 Skills 到全局目录..." -ForegroundColor Yellow
$source = "$env:USERPROFILE\my-skills\superpowers"
$target = "$env:USERPROFILE\.agents\skills\superpowers"

if (Test-Path $source) {
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse $source $target
    Write-Host "  ✓ Skills 已同步" -ForegroundColor Green
} else {
    Write-Host "  ✗ 源目录不存在: $source" -ForegroundColor Red
}

# 3. 配置 Git
Write-Host "`n[3/5] 配置 Git..." -ForegroundColor Yellow
cd "$env:USERPROFILE\my-skills"
git config user.name "AI Workflow" 2>$null
git config user.email "workflow@local" 2>$null
Write-Host "  ✓ Git 配置完成" -ForegroundColor Green

# 4. 安装 VSCode 扩展
Write-Host "`n[4/5] 检查 VSCode 扩展..." -ForegroundColor Yellow
$extensions = @(
    "DeepMyst.mysti",
    "Gruntfuggly.todo-tree",
    "eamodio.gitlens"
)

foreach ($ext in $extensions) {
    $installed = code --list-extensions | Select-String $ext
    if ($installed) {
        Write-Host "  ✓ $ext 已安装" -ForegroundColor Green
    } else {
        Write-Host "  → 安装 $ext..." -ForegroundColor Yellow
        code --install-extension $ext --force
    }
}

# 5. 创建快捷方式
Write-Host "`n[5/5] 创建快捷命令..." -ForegroundColor Yellow
$profilePath = "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
if (-not (Test-Path $profilePath)) {
    New-Item -ItemType File -Path $profilePath -Force | Out-Null
}

$aliases = @"
`n# AI Workflow 快捷命令
function skillsync { & "$env:USERPROFILE\my-skills\sync-and-push.sh" }
function skilldev { Set-Location "$env:USERPROFILE\Desktop\claude\superpowers-main" }
function skillhome { Set-Location "$env:USERPROFILE\my-skills" }
function mystistart { code --enable-proposed-api DeepMyst.mysti }
Set-Alias -Name ss -Value skillsync
Set-Alias -Name sd -Value skilldev
Set-Alias -Name sh -Value skillhome
"@

if (-not (Select-String -Path $profilePath -Pattern "AI Workflow" -Quiet)) {
    Add-Content -Path $profilePath -Value $aliases
    Write-Host "  ✓ 快捷命令已添加到 PowerShell Profile" -ForegroundColor Green
} else {
    Write-Host "  ✓ 快捷命令已存在" -ForegroundColor Green
}

Write-Host "`n=== 配置完成 ===" -ForegroundColor Cyan
Write-Host "快捷命令:" -ForegroundColor Yellow
Write-Host "  ss    - 同步 skills 到 GitHub" -ForegroundColor Gray
Write-Host "  sd    - 进入开发目录" -ForegroundColor Gray
Write-Host "  sh    - 进入 skill 主页" -ForegroundColor Gray
Write-Host "  mystistart - 启动 Mysti" -ForegroundColor Gray
Write-Host "`nVSCode 快捷键:" -ForegroundColor Yellow
Write-Host "  Ctrl+Shift+S - 一键 commit & push" -ForegroundColor Gray
Write-Host "  Ctrl+Shift+T - 打开任务看板" -ForegroundColor Gray
Write-Host "  Ctrl+Shift+M - 打开 Mysti" -ForegroundColor Gray
Write-Host "  Ctrl+Shift+B - Brainstorm Mode" -ForegroundColor Gray
