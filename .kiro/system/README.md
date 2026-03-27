# Kiro System Prompt Kit

This directory contains the canonical Kiro system prompt, structured exactly as it is received at runtime.

## Files

- `system-prompt.md` — The complete system prompt. One file. Uses `{{VAR}}` tokens for runtime values.
- `tool-reference.md` — Complete tool catalog with parameter schemas (appended when tools are available).
- `platform-specifics.md` — Documents the three platform variants that get infilled into the system prompt.
- `README.md` — This file.

## How It Works

The system prompt is a single document. At assembly time:

1. Replace `{{VAR}}` tokens with runtime values
2. Infill the `{{PLATFORM_COMMANDS}}` block with the appropriate platform section from `platform-specifics.md`
3. Optionally append `tool-reference.md` content for agents that need tool schemas

That's it. No module concatenation, no dependency ordering, no conditional includes.

## Template Variables

| Variable | Example |
|----------|---------|
| `{{MODEL_NAME}}` | Claude Opus 4.6 |
| `{{MODEL_DESCRIPTION}}` | The latest Claude Opus model with 1M context window |
| `{{OS_NAME}}` | Windows |
| `{{PLATFORM}}` | win32 |
| `{{SHELL}}` | bash |
| `{{CURRENT_DATE}}` | March 27, 2026 |
| `{{DAY_OF_WEEK}}` | Friday |
| `{{MACHINE_ID}}` | 2804640f... |
| `{{PLATFORM_COMMANDS}}` | Replaced with platform-specific command block |
| `{{INSTALLED_POWERS}}` | Runtime list of installed powers |
| `{{AVAILABLE_SKILLS}}` | Runtime list of available skills |
| `{{OPEN_EDITOR_FILES}}` | Runtime IDE state |
| `{{ACTIVE_EDITOR_FILE}}` | Runtime IDE state |
