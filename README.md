# MCP Manager

# My Skills - AI Workflow 涓績

涓汉 Claude/Codex Skill 绠＄悊涓績锛岄泦鎴?Mysti 澶?Agent 鍗忎綔 + VSCode 鍙鍖栥€?

## 蹇€熷紑濮?

### 1. 涓€閿厤缃紙鑷姩锛?

```powershell
# 浠ョ鐞嗗憳韬唤杩愯 PowerShell
Set-ExecutionPolicy Bypass -Scope Process
& "$env:USERPROFILE\my-skills\setup-workflow.ps1"
```

### 2. 閰嶇疆瀹屾垚鍚庣殑蹇嵎鍛戒护

| 鍛戒护 | 浣滅敤 |
|------|------|
| `ss` | 鍚屾 skills 鍒?Codex + GitHub |
| `sd` | 杩涘叆寮€鍙戠洰褰?|
| `sh` | 杩涘叆 skill 涓婚〉 |
| `mystistart` | 鍚姩 Mysti |

### 3. VSCode 蹇嵎閿?

| 蹇嵎閿?| 鍔熻兘 |
|--------|------|
| `Ctrl+Shift+S` | 涓€閿?commit & push |
| `Ctrl+Shift+T` | 鎵撳紑浠诲姟鐪嬫澘 (Todo Tree) |
| `Ctrl+Shift+M` | 鎵撳紑 Mysti |
| `Ctrl+Shift+B` | Brainstorm Mode |

## 鐩綍缁撴瀯

```
my-skills/
鈹溾攢鈹€ superpowers/              # Superpowers 鎶€鑳介泦
鈹?  鈹溾攢鈹€ brainstorming/        # 璇煶鐗堝ご鑴戦鏆?
鈹?  鈹?  鈹溾攢鈹€ SKILL.md         # 瀹屾暣鐗?
鈹?  鈹?  鈹斺攢鈹€ SKILL-OPTIMIZED.md  # Token 浼樺寲鐗?
鈹?  鈹斺攢鈹€ ...
鈹溾攢鈹€ mysti-config.json         # Mysti 澶?Agent 閰嶇疆
鈹溾攢鈹€ setup-workflow.ps1        # 涓€閿厤缃剼鏈?
鈹溾攢鈹€ sync-and-push.sh          # 鍚屾鑴氭湰
鈹溾攢鈹€ token-monitor.md          # Token 棰勭畻鐩戞帶
鈹斺攢鈹€ README.md                 # 鏈枃浠?
```

## 宸ヤ綔娴佺▼

### 鏃ュ父寮€鍙?

```bash
# 1. 杩涘叆寮€鍙戠洰褰?
sd

# 2. 鍦?VSCode 涓紪杈?skill

# 3. 涓€閿悓姝?
ss
```

### 浣跨敤 Mysti 澶?Agent

```bash
# 鍚姩 Mysti
mystistart

# 鍦?VSCode 涓?
@claude @codex Review this design
# 鎴栨寜 Ctrl+Shift+B 鍚姩 Brainstorm Mode
```

## Token 浼樺寲

### 鑷姩鑺傜渷 Token 鐨勬満鍒?

1. **Mysti 鍐呯疆**: 涓婁笅鏂囧帇缂┿€丼kill 鎳掑姞杞姐€佸巻鍙插帇缂?
2. **閰嶇疆棰勭畻**: 8000 璀﹀憡锛?2000 闄愬埗
3. **浼樺寲鐗?Skill**: 绠€鍗曚换鍔＄敤绮剧畝鐗?

### 浣曟椂浣跨敤浼樺寲鐗?

```markdown
绠€鍗曚换鍔?/ Token 绱у紶 鈫?SKILL-OPTIMIZED.md
澶嶆潅璁捐 / 闇€瑕佹繁搴?鈫?SKILL.md (瀹屾暣鐗?
```

## 闆嗘垚璇存槑

### Mysti + Superpowers 鍏崇郴

```
Mysti (VS Code 鎵╁睍)
    鈫?璋冪敤
Claude Code CLI 鈫?璇诲彇 ~/.claude/ 閰嶇疆
    鈫?浣跨敤
Superpowers Skill (鏈」鐩?
```

**Mysti 涓嶄細鏇挎崲浣犵殑 skill锛岃€屾槸澧炲己璋冪敤鏂瑰紡銆?*

## 鍚屾鍒?GitHub

棣栨閰嶇疆锛?
```bash
cd ~/my-skills
gh repo create my-skills --public
git push -u origin main
```

鍚庣画鍚屾锛?
```bash
ss  # 涓€閿悓姝?
```

## 绯荤粺瑕佹眰

- VSCode 1.85+
- Claude Code CLI
- Codex CLI
- PowerShell 7+ (Windows)

## Auto Startup (Windows)

Register a login task to run one scan + recommendations refresh:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-startup-task.ps1
```

Remove the startup task:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/unregister-startup-task.ps1
```

## 鏁呴殰鎺掗櫎

| 闂 | 瑙ｅ喅 |
|------|------|
| Mysti 涓嶆樉绀?| 妫€鏌?mysti-config.json 璺緞 |
| Skill 涓嶇敓鏁?| 杩愯 `ss` 鍚屾 |
| Token 瓒呮敮 | 鏌ョ湅 token-monitor.md |

## 鏇存柊鏃ュ織

- 2026-02-19: 娣诲姞 Mysti 闆嗘垚 + Token 浼樺寲
- 2026-02-18: 鍒濆閰嶇疆 + Voice Support

## Start

- Web: start-web.bat
- TUI: start-tui.bat


## AI Hub
Global AI library: C:\\Users\\11918\\AI-Hub
Run scan: python -m mcp_manager.organize --scan

## AI-Hub Confirm-Only Mode
AI files require confirmation before moving. Non-AI files are ignored.
Rules live in C:\\Users\\11918\\AI-Hub\\_rules\\rules.json.

