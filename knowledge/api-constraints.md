# API Constraints & Rules

## OpenAI Models on This Platform

### Model Names
- **SEARCH_MODEL**: `gpt-4.1-nano-2025-04-14`
- **DRAFTING_MODEL**: `gpt-5-nano-2025-08-07`

### Parameter Support

**❌ NOT SUPPORTED:**
- `temperature` parameter - These models only accept the default value (1.0)
- Any custom temperature values will cause: `"temperature does not support X with this model"`

**✅ SUPPORTED:**
- `messages` (required)
- `model` (required)

### Rule
**ALWAYS omit the `temperature` parameter when calling these models.** Use API defaults instead.

Last confirmed: 2026-04-10
