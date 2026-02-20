# AI-Hub Rules Keys

This file documents the keys expected in `C:\Users\11918\AI-Hub\_rules\rules.json`.

## Core Matching
- `core_exts`: Model weight extensions treated as Models
- `ai_keywords`: General AI keywords that allow AI-only matching

## Categories
- `tool_keywords`: Tools and frameworks (Tools)
- `plugin_keywords`: MCP/IDE plugins (Plugins)
- `dataset_keywords`: Dataset signals (Datasets)
- `doc_keywords`: Documentation signals (Docs)
- `code_keywords`: Code and SDK signals (Code)

## Families
- `model_families`: Map of model families to keywords
- `tool_families`: Map of tool families to keywords

## Exclusions
- `exclude_exts`: Extensions to ignore (media, etc.)
- `exclude_paths`: Folder substrings to skip (games/system)

## Size
- `large_threshold_bytes`: Large-file threshold used for policy checks
