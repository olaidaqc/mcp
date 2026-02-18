---
name: brainstorming-optimized
description: "Optimized version with token-efficient voice support. Use when token budget is limited but voice features needed."
---

# Brainstorming (Token-Optimized)

## Quick Start
1. Detect voice → 2. Paraphrase → 3. Hybrid output → 4. Single question loop

## Voice Detection (Auto)
- >100 chars + >=2 of: fillers("那个/um"), corrections("不对/wait"), sparse punctuation

## Response Format
```
[VOICE_SUMMARY] 1-line confirmation
[TEXT_DETAILS] Bulleted details
Q: [Single question]
```

## Exit Voice Mode
- "/text" or <30 chars without voice patterns

## Low Confidence
List 2-3 options: "A) x B) y C) other?"

## Token Rules
- Max 150 tokens per response in Voice Mode
- No redundant explanations
- Cross-ref other skills instead of repeating
- One excellent example only
