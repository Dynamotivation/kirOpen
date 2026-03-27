# Kiro Tool Reference

Last updated: March 2026

This document describes the complete set of tools available to Kiro, including their parameters and usage rules.

---

## File System Tools

### fsWrite
Create or overwrite a file. If the content is larger than 50 lines, use fsWrite for the first part and fsAppend for the rest.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | Path to file, e.g. `file.py` or `repo/file.js` |
| text | string | yes | Contents to write into the file |

### fsAppend
Append text content to the end of an existing file. Automatically handles newline formatting. The target file MUST already exist.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | Relative path to the existing file from workspace root |
| text | string | yes | Text content to append |

### deleteFile
Delete a file at the specified path. Fails gracefully if the file doesn't exist or can't be deleted.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| targetFile | string | yes | Path of the file to delete, relative to workspace root |
| explanation | string | yes | One sentence explaining why |

### readFile
Read a single file with optional line range specification.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | Path to file, relative to workspace root |
| explanation | string | yes | Why this file is being read (used for intelligent pruning) |
| start_line | number | no | Starting line number |
| end_line | number | no | Ending line number |
| skipPruning | boolean | no | Set true only when complete unmodified content is needed. Default false. |

### readMultipleFiles
Read multiple files at once. Preferred over multiple single-file reads.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | string[] | yes | Array of file paths relative to workspace root |
| explanation | string | yes | Why these files are being read |
| start_line | number | no | Starting line number (applied to all files) |
| end_line | number | no | Ending line number |
| skipPruning | boolean | no | Default false |

### listDirectory
List directory contents in long format (similar to `ls -la`).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | Absolute path or relative to workspace root |
| explanation | string | yes | Why listing this directory |
| depth | number | no | Depth for recursive listing |
| skipPruning | boolean | no | Default false |

---

## Code Tools

### readCode
AST-based code file reader. Preferred over readFile for code files. For small files (<10k chars), returns full content. For larger files, extracts function/class signatures via AST parsing.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | File or directory path to analyze |
| explanation | string | yes | Why this tool is being used |
| selector | string | no | Symbol name to search (supports `Class.method` syntax) |
| language | string | no | Programming language (auto-detected if not specified) |

Supported patterns: functions, arrow functions, async functions, generators, class properties, getters/setters, abstract classes, nested classes, enums, namespaces, interfaces, constructors.

### editCode
AST-based code editor with auto-indentation, syntax validation, and auto-repair.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | File path to modify |
| operation | enum | yes | `replace_node`, `insert_node`, or `delete_node` |
| selector | string | yes | Target: `ClassName`, `functionName`, `ClassName.methodName`, or `"start"` |
| replacement | string | no | New code (required for replace_node and insert_node) |
| language | string | no | Programming language (auto-detected) |

AST languages supported: Python, Java, C, C++, JavaScript, TypeScript, Go, Rust, Ruby, PHP, C#.
For non-AST files (JSON, YAML, HTML, CSS, Markdown, config), use strReplace instead.

Rules:
- `"start"` selector is only valid with insert_node (inserts after file headers/imports)
- insert_node with ClassName inserts INSIDE the class as last member, not after it
- insert_node with functionName inserts AFTER the function
- Prefer strReplace for small edits (< 5 lines)
- Use editCode for adding new functions/methods, deleting entire functions/classes, or complete rewrites (>30% change)

### strReplace
Replace text in files. Especially useful for targeted edits in long files.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | Path to the file |
| oldStr | string | yes | Exact text to find (must match exactly one location, whitespace-sensitive) |
| newStr | string | yes | Replacement text (must differ from oldStr) |

Critical rules:
- oldStr must match EXACTLY one or more consecutive lines
- All whitespace must match exactly (critical for Python)
- Include 2-3 lines of context for uniqueness
- Multiple independent replacements should be invoked in parallel

### semanticRename
Rename a symbol across the entire codebase. Finds all references and renames them consistently.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | yes | Path to file containing the symbol |
| line | number | yes | Line number where symbol is located (0-indexed) |
| character | number | yes | Character position on the line (0-indexed) |
| oldName | string | yes | Current name of the symbol (for validation) |
| newName | string | yes | New name for the symbol |

### smartRelocate
Move or rename files with automatic import/reference updates across the codebase.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sourcePath | string | yes | Current relative path to the file |
| destinationPath | string | yes | New relative path for the file |

### getDiagnostics
Get compile, lint, type, and other semantic issues in code files. Use this instead of bash commands for checking code issues.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | string[] | yes | Array of relative file paths to check |

---

## Search Tools

### fileSearch
Fast fuzzy file path search. Results capped at 10.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | yes | Regex pattern to search for |
| explanation | string | yes | Why searching |
| excludePattern | string | no | Glob pattern for files to exclude |
| includeIgnoredFiles | string | no | "yes" or "no" to include .gitignore files |

### grepSearch
Fast regex text search using ripgrep. Results include line numbers and 2 lines of context. Capped at 50 matches.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | yes | Regex pattern (Rust regex syntax) |
| explanation | string | no | Why searching |
| caseSensitive | boolean | no | Default case-insensitive |
| includePattern | string | no | Glob pattern for files to include (use `**` for recursive) |
| excludePattern | string | no | Glob pattern for files to exclude |
| skipPruning | boolean | no | Default false |

---

## Shell Execution Tools

### executePwsh
Execute a shell command (CMD or PowerShell).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| command | string | yes | Shell command to execute |
| cwd | string | no | Working directory (defaults to workspace root) |
| explanation | string | no | Why running this command |
| timeout | number | no | Timeout in milliseconds |
| ignoreWarning | boolean | no | Bypass long-running command warnings |
| skipPruning | boolean | no | Default false |

Rules:
- NEVER use `cd` command — use `cwd` parameter instead
- Avoid long-running commands (dev servers, watchers) — use controlPwshProcess instead
- Avoid search commands (cat, find, grep, ls) — use dedicated search tools instead
- Avoid file writing commands (mkdir, piping) — use fsWrite instead

### controlPwshProcess
Start or stop background processes (dev servers, build watchers, etc.).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | enum | yes | `"start"` or `"stop"` |
| command | string | for start | The command to run as background process |
| cwd | string | no | Working directory |
| terminalId | string | for stop | ID of the process to terminate |

### listProcesses
List all background processes managed by Kiro. No parameters.

Returns: processes with terminalId, command, path, status (running/stopped/unknown).

### getProcessOutput
Read output from a background process.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| terminalId | string | yes | ID of the background process |
| explanation | string | no | What information you need |
| lines | number | no | Number of lines to limit output (default 100) |
| skipPruning | boolean | no | Default false |

---

## Web Tools

### remote_web_search
Search the internet for current information. Query must be 200 characters or fewer.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | yes | Search query (max 200 chars) |

Returns: title, url, snippet, publishedDate, isPublicDomain, domain.

Content compliance rules:
- ALWAYS provide inline links to original sources
- NEVER reproduce more than 30 consecutive words from any single source
- Paraphrase and summarize rather than quote directly
- Prioritize latest published sources and official documentation

### webFetch
Fetch and extract content from a specific URL. Content is from UNTRUSTED SOURCES.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | yes | Complete HTTPS URL (no query params or fragments) |
| mode | enum | no | `"truncated"` (default, 8KB), `"full"` (10MB), `"selective"`, or `"rendered"` (JS-heavy pages, retry only) |
| searchPhrase | string | for selective | Phrase to search for in selective mode |

Rules:
- Only HTTPS protocol allowed
- URL must not contain query parameters or fragments
- Use "rendered" mode only as a retry when normal fetch returned insufficient content

---

## Sub-Agent Tool

### invokeSubAgent
Delegate tasks to specialized agents that run autonomously.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Agent name: `context-gatherer`, `general-task-execution`, or `custom-agent-creator` |
| prompt | string | yes | Clear, specific task description for the agent |
| explanation | string | yes | Why delegating this task |
| contextFiles | object[] | no | Array of `{path, startLine?, endLine?}` file references |
| preset | string | no | Optional preset identifier |

Available agents:
- **context-gatherer**: Analyzes repo structure to identify relevant files. Use for unfamiliar codebases, bug investigation, understanding component interactions. Use ONCE per query.
- **general-task-execution**: General-purpose agent with all tools. For well-defined subtasks or parallelizing work.
- **custom-agent-creator**: For creating and configuring new custom agents.

Sub-agents are only available in Autopilot mode.

---

## Hook Tool

### createHook
Create agent hooks that automate actions based on IDE events.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | yes | Short 3-word dashed id (e.g. `my-new-hook`) |
| name | string | yes | Short title |
| description | string | yes | What the hook does |
| eventType | string | yes | One of: `fileEdited`, `fileCreated`, `fileDeleted`, `userTriggered`, `promptSubmit`, `agentStop`, `preToolUse`, `postToolUse`, `preTaskExecution`, `postTaskExecution` |
| hookAction | string | yes | `askAgent` or `runCommand` |
| why | string | yes | One sentence on why |
| outputPrompt | string | for askAgent | Prompt to give to the agent |
| command | string | for runCommand | Shell command to execute |
| filePatterns | string | for file events | Comma-separated file patterns (e.g. `*.ts, *.tsx`) |
| toolTypes | string | for tool events | Comma-separated tool categories or regex patterns. Categories: `read`, `write`, `shell`, `web`, `spec`, `*` |
| timeout | number | no | Timeout in seconds for runCommand (default 60, 0 to disable) |

---

## Powers Tool

### kiroPowers
Manage and use Kiro Powers (packaged documentation, workflow guides, and MCP servers).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | enum | yes | `"list"`, `"activate"`, `"use"`, `"readSteering"`, or `"configure"` |
| powerName | string | for most | Name of the power |
| serverName | string | for use | MCP server name (from activate response) |
| toolName | string | for use | Tool name within the server |
| arguments | object | for use | Tool parameters matching inputSchema |
| steeringFile | string | for readSteering | Steering file name (including .md extension) |

Workflow:
1. `list` — discover installed powers and their keywords
2. `activate` — get documentation, tool schemas, and steering files for a power
3. `use` — execute a tool from an activated power's MCP server
4. `readSteering` — read detailed workflow guides
5. `configure` — open the powers management panel

Rules:
- NEVER call `use` without calling `activate` first
- Tool names and input schemas come from the activate response
- Power names are case-sensitive
- Proactively activate powers when user's message matches a power's keywords

---

## Diagnostics Tool

### getDiagnostics
Get compile, lint, type, and other semantic issues in code files.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | string[] | yes | Array of relative file paths to check |

Notes:
- Use this instead of bash commands for finding compile errors
- Use after editing a file to validate the change
- If no problems found, no need to run bash commands afterwards
- Only available when language extensions are installed that provide diagnostic information

---

## Skills Tool

### discloseContext
Activate skills or auto-inclusion steering files to load their full instructions into context.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | yes | Exact name of the skill or steering file to activate |

Skills can be added to `~/.kiro/skills/` (user-level) or `.kiro/skills/` (workspace-level).
