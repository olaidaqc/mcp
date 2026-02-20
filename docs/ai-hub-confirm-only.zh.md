# AI-Hub Confirm-Only 技能说明（中文注释）

此文件为中文注释说明，不影响任何代码或配置读取。

## 功能概述

- 只处理 AI 相关文件，非 AI 文件完全不移动
- 所有 AI 文件都必须人工确认后才会移动
- 确认后会学习关键词，提升后续匹配准确度

## 核心目录

- AI-Hub 根目录: `C:\Users\11918\AI-Hub`
- 规则文件: `C:\Users\11918\AI-Hub\_rules\rules.json`
- 学习关键词: `C:\Users\11918\AI-Hub\_rules\learned_keywords.json`
- 扫描计划: `C:\Users\11918\AI-Hub\_reports\plan.json`

## 运行流程

1. 扫描生成计划  
   `python -m mcp_manager.organize --scan`
2. 打开网页确认  
   `http://127.0.0.1:8000/`
3. 勾选后点击 `Confirm Selected`

## 安全说明

- 不会自动移动任何文件
- 图片/视频等媒体默认排除
- 游戏/系统目录默认排除
