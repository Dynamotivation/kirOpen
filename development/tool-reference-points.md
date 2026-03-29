# KirOpen Tool Reference Source

Last updated: March 2026

This file captures the original KirOpen tool taxonomy as source material for prompt assembly and feature mapping. It is intentionally not injected verbatim into Codex or Copilot outputs because those harnesses expose different tool names, parameters, and control surfaces.

## Purpose

Use this document to preserve:

- the kinds of actions KirOpen expects an agent to take
- the workflow expectations behind those actions
- the capability areas that need harness-specific translation

Use the vendor templates to translate these concepts into real harness instructions.

## Capability Areas

### Files And Code

KirOpen expects an agent to be able to:

- read one or many files
- write and append files
- make targeted code edits
- rename symbols safely
- relocate files safely
- inspect diagnostics after edits

In Codex these ideas map to native runtime tools such as `shell_command`, `apply_patch`, MCP resource tools when available, and structured review or verification guidance in the prompt.

In Copilot these ideas map to Copilot's own available workspace and editing tools, with any extra constraints documented in the Copilot agent and instructions templates.

### Search And Discovery

KirOpen expects an agent to:

- search files quickly
- search file contents with regex
- inspect directory structure
- gather context before editing

This should be translated per harness:

- Codex: prefer `rg`, `Get-ChildItem`, `multi_tool_use.parallel`, and delegated `explorer` agents when available
- Copilot: prefer the harness search tools and delegated `agent` flows when available

### Shell And Execution

KirOpen expects controlled command execution, background process handling, and output inspection.

Map this carefully:

- Codex: `shell_command` is the real execution surface in this runtime
- Copilot: use the harness-native command capabilities and avoid inventing a KirOpen-like process API if the harness does not expose one

### Web Access

KirOpen expects current-information lookup and source-backed answers when needed.

Map this carefully:

- Codex: use `web.run` when current information is needed
- Copilot: only describe or enable web behavior that the target harness actually supports

### Delegation

KirOpen models specialized sub-agents for context gathering and task execution.

Map this carefully:

- Codex: use `spawn_agent`, `send_input`, `wait_agent`, and the built-in `explorer` or `worker` roles when the user explicitly wants delegation
- Copilot: use the Copilot custom agent model and any harness-native agent delegation features, if present

### Steering, Specs, Hooks, And MCP

These are KirOpen product concepts, not universal agent primitives.

- Steering should stay a KirOpen source concept and be translated into the closest harness equivalent rather than copied blindly
- Specs are a workflow and documentation method that can be reused across harnesses
- Hooks and MCP are highly harness-specific and should only be emitted when the target harness has a real equivalent

## Recommendation

Keep this file as a maintainer-facing source document. If you later want runtime tool schemas in generated output, add harness-specific derived templates instead of appending this file directly.

For harness expansion workflow and the current file-by-file maintenance map, also see:

- [adding-a-harness.md](/d:/source/repos/kirOpen/development/adding-a-harness.md)
- [harness-touchpoints.md](/d:/source/repos/kirOpen/development/harness-touchpoints.md)
