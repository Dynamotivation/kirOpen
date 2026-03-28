# KirOpen

> [!IMPORTANT]
> KirOpen is not Kiro itself.
> This is an independent community research and development project. It is not affiliated with, endorsed by, or maintained by the official Kiro team.
> Without the original work of the Kiro team, Amazon, and Jason Kneen's upstream repository and research, this project would not exist.

KirOpen is an open interoperability project inspired by Kiro's spec-driven development workflow and surrounding agent concepts.

It exists to:

- Reduce downtime when a single vendor or model surface is unavailable
- Reduce single points of failure in AI-assisted development workflows
- Help other vendors' models work better with Kiro-style spec-driven development
- Keep useful Kiro concepts portable instead of trapped in one IDE or one file format

KirOpen translates Kiro concepts such as specs, steering, hooks, MCP, powers, vibe mode, and autonomy preferences into the closest equivalent features offered by other harnesses.

## What KirOpen Preserves

- Spec-driven development
  Requirements, design, and task planning under `.kiro/specs/...`
- Vibe mode and spec mode
  Lightweight exploratory work versus structured planned work
- Similar model behavior through observed guidelines and guardrails
- Conversion skill from Kiro's Steering, Hooks, MCP and Powers formats into each harness's native equivalents (if supported)

## Supported Harnesses

- Codex
- GitHub Copilot
- Antigravity

## Planned Harnesses

- Kilo Code
- Claude Code
- Cursor
- Windsurf
- Kiro-native parity templates

## How It Works

The repository contains shared templates plus vendor-specific adapters.

The main entrypoint is:

```bash
python assemble_instructions.py
```

Supported CLI usage:

```bash
python assemble_instructions.py [--platform win32|darwin|linux] [--output-dir <dir>] [--mode agent|default] [codex] [copilot] [antigravity]
```

If your system exposes Python as `python3`, use `python3` in the examples below.

## Choosing A Mode

- `agent`
  Use this when you want KirOpen to stay mostly opt-in. In this mode, the builder generates harness-specific agents, workflows, skills, prompts, and scoped guidance surfaces, but it does not try to replace the harness's default project-wide behavior unless that harness always needs a supporting file for activation.
- `default`
  Use this when you want KirOpen to shape the harness's default behavior for the whole repository. In this mode, the builder also emits the harness's main default instruction surface, such as `CODEX.md` for Codex, `.github/copilot-instructions.md` for Copilot, or an always-on main rule for Antigravity.
  If you are generating only for Codex, you can optionally use `AGENTS.md` instead via `--codex-root-doc agents`, but that can cause issues later if you switch AI harnesses.

Practical difference:

- `agent` mode is safer when you want to add KirOpen alongside an existing setup without changing every chat by default
- `default` mode is better when KirOpen should become the repo's primary assistant behavior immediately
- Both modes still generate the reusable KirOpen workflow assets for the selected harness
- `default` mode adds more global behavior and should be chosen deliberately, especially in repos that already have harness-specific instruction files

## Installation

> [!TIP]
> If you run the script with no arguments, it starts in interactive mode.

Prebuilding cannot be offered since for some harnesses you need to configure the harnesses on the users machine.

### Installing into empty Repositories

If the target repo has no prior Kiro setup:

- Generate the harness output you want
- Generate directly into the repo root with `--output-dir .` when you are already inside the target repository
- Start using the shared KirOpen skills and harness-specific agents
- Create `.kiro/specs/...` when you want to run the full spec-driven workflow

Examples:

```bash
python /path/to/kirOpen/assemble_instructions.py --output-dir . codex
python /path/to/kirOpen/assemble_instructions.py --output-dir . copilot
python /path/to/kirOpen/assemble_instructions.py --output-dir . antigravity
python /path/to/kirOpen/assemble_instructions.py --mode default --output-dir . codex
python /path/to/kirOpen/assemble_instructions.py --mode default --codex-root-doc agents --output-dir . codex
python /path/to/kirOpen/assemble_instructions.py --mode default --output-dir . copilot
python /path/to/kirOpen/assemble_instructions.py --mode default --output-dir . antigravity
```


### Installing into existing Repositories

If the target repo already contains `.kiro` content:

- Keep `.kiro/specs/...` as the source of truth for the spec workflow
- Keep `.kiro/steering/...` until you deliberately port or translate it
- Use the generated porting assets to translate Kiro-specific configuration into each harness's native surfaces
- Do not blindly rename `.kiro` to vendor folders

KirOpen is designed to preserve Kiro semantics, not erase them.
You may encounter file conflicts when you generate into an existing repo. This is intentional to prevent accidental overwrites. If a generated file already exists, review the differences and merge the relevant changes manually.
Running in agent mode might be easier.

#### How to merge into conflicting repositories

<details>
<summary><strong>Codex</strong></summary>

Generate into a temporary review folder first:

```bash
python assemble_instructions.py --output-dir review_codex codex
```

In `agent` mode, review and copy:

- `review_codex/.codex/agents/kiropen_spec.toml` -> `<repo>/.codex/agents/kiropen_spec.toml`
- `review_codex/.agents/skills/...` -> `<repo>/.agents/skills/...`
- `review_codex/.codex/copy-me-into-your-api-directories/AGENTS.override.md` -> Move into the API directory that should receive that scoped guidance
- `review_codex/.codex/copy-me-into-your-environment-directories/AGENTS.override.md` -> Move into the environment or config directory that should receive that scoped guidance
- `review_codex/.codex/copy-me-into-your-frontend-directories/AGENTS.override.md` -> Move into the frontend or app directory that should receive that scoped guidance

If you built in `default` mode, also copy:

- `review_codex/CODEX.md` -> `<repo>/CODEX.md`
- `review_codex/.codex/config.toml` -> `<repo>/.codex/config.toml`

If you built with `--codex-root-doc agents`, copy instead:

- `review_codex/AGENTS.md` -> `<repo>/AGENTS.md`

How Kiro features map to KirOpen on Codex:

| Kiro feature | KirOpen on Codex | Main outputs in this repo | Notes |
| --- | --- | --- | --- |
| Skills | Map directly to Codex skills | `.agents/skills/*/SKILL.md` | This is the closest one-to-one mapping for reusable workflow guidance. |
| Spec workflow | Keep the Kiro methodology, but implement it with Codex skills and a custom specialist agent | `.agents/skills/spec-driven-development/`, `.codex/agents/kiropen_spec.toml` | Specs stay a workflow pattern, not a Codex-native artifact type. |
| Steering | Translate to directory-scoped Codex instruction files | `AGENTS.override.md`, optional `CODEX.md` in default mode | Prefer local `AGENTS.override.md` files over one giant repo-wide prompt. |
| Powers | Split into the nearest Codex surfaces | Skills, custom agents, MCP config, hooks | Do not copy the Kiro power format directly. |
| Hooks | Translate only when the user wants hooks and Codex supports the behavior | `.codex/hooks.json` | Hooks are experimental, require `[features] codex_hooks = true`, and are disabled on Windows. |
| MCP | Translate to Codex MCP server config | `.codex/config.toml` with `[mcp_servers.<name>]` | Codex MCP can also be managed with `codex mcp add`. |
| Autopilot / Supervised | Translate into Codex approval and sandbox settings | `.codex/config.toml` or user config | Treat this as a collaboration-style preference, not a literal Kiro mode. |
| Chat context like `#File`, `#Folder`, `#Problems`, `#Git Diff` | Reinterpret through Codex context files, tools, and local instructions | `AGENTS.override.md`, `CODEX.md`, tool usage rules | Kiro syntax is not copied literally. |
| Subagents | Translate to Codex subagents and custom agents | `.codex/agents/*.toml` | Use Codex-native delegation instead of Kiro-specific agent names. |
| Internet access | Use Codex web tooling | Prompt assembly via vendor snippets | KirOpen treats current-info tasks as web-enabled work in Codex. |

</details>

<details>
<summary><strong>GitHub Copilot</strong></summary>

Generate into a temporary review folder first:

```bash
python assemble_instructions.py --output-dir review_copilot copilot
```

In `agent` mode, review and copy:

- `review_copilot/.github/agents/kiropen.agent.md` -> `<repo>/.github/agents/kiropen.agent.md`
- `review_copilot/.github/agents/kiropen-spec.agent.md` -> `<repo>/.github/agents/kiropen-spec.agent.md`
- `review_copilot/.github/instructions/*.instructions.md` -> `<repo>/.github/instructions/*.instructions.md`
- `review_copilot/.agents/skills/*/SKILL.md` -> `<repo>/.agents/skills/*/SKILL.md`
- `review_copilot/.github/prompts/port-kiro-configuration-to-kiropen-on-copilot.prompt.md` -> `<repo>/.github/prompts/port-kiro-configuration-to-kiropen-on-copilot.prompt.md`

If you built in `default` mode, also copy:

- `review_copilot/.github/copilot-instructions.md` -> `<repo>/.github/copilot-instructions.md`

How Kiro features map to KirOpen on GitHub Copilot:

| Kiro feature | KirOpen on Copilot | Main outputs in this repo | Notes |
| --- | --- | --- | --- |
| Skills | Map to reusable repo skills | `.agents/skills/*/SKILL.md` | Skills carry reusable workflow logic across Copilot surfaces that support them. |
| Spec workflow | Keep the Kiro methodology, but implement it with Copilot skills, agents, and prompts | `.agents/skills/spec-driven-development/`, `.github/agents/kiropen-spec.agent.md` | Specs remain a workflow, not a Copilot-native artifact type. |
| Steering | Translate to Copilot instruction surfaces | `.github/instructions/*.instructions.md`, optional `.github/copilot-instructions.md` in default mode | Use path-scoped instructions for situational guidance. |
| Powers | Split into the nearest Copilot surfaces | Skills, agents, prompts, hooks, MCP config | Do not copy Kiro powers directly. |
| Hooks | Translate to repository hook files when the active Copilot surface supports them | `.github/hooks/*.json` | Hook support differs by Copilot surface, so current GitHub docs should win. |
| MCP | Translate to the MCP surface for the active Copilot environment | Repository MCP config, `~/.copilot/mcp-config.json`, or supported agent frontmatter | Pick the right surface before writing config. |
| Autopilot / Supervised | Translate into the active Copilot approval and review behavior | Depends on Copilot surface | Treat this as a behavior preference, not a literal Kiro mode. |
| Chat context like `#File`, `#Folder`, `#Problems`, `#Git Diff` | Reinterpret through Copilot's context tools and instruction surfaces | Instructions, agents, prompts | Kiro context syntax is not portable as-is. |
| Subagents / specialists | Translate to Copilot custom agents | `.github/agents/*.agent.md` | Use Copilot's custom agent model instead of Kiro-specific personas. |
| Internet access | Use Copilot's available web and agent capabilities where supported | Prompt assembly via vendor snippets | Do not promise web behavior the active Copilot surface does not actually have. |

</details>

<details>
<summary><strong>Antigravity</strong></summary>

Generate into a temporary review folder first:

```bash
python assemble_instructions.py --output-dir review_antigravity antigravity
```

In `agent` mode, review and copy:

- `review_antigravity/.agent/rules/kiropen.md` -> `<repo>/.agent/rules/kiropen.md`
- `review_antigravity/.agent/rules/kiro-interop.md` -> `<repo>/.agent/rules/kiro-interop.md`
- `review_antigravity/.agents/skills/*/SKILL.md` -> `<repo>/.agents/skills/*/SKILL.md`

In `default` mode, copy the same files, but note that `kiropen.md` is generated as an always-on rule instead of a manual rule.

How Kiro features map to KirOpen on Antigravity:

| Kiro feature | KirOpen on Antigravity | Main outputs in this repo | Notes |
| --- | --- | --- | --- |
| Skills | Map to shared Antigravity skills | `.agents/skills/*/SKILL.md` | KirOpen now uses the shared skills surface for reusable behavior. |
| Spec workflow | Keep the Kiro methodology, but implement it as reusable skills | `.agents/skills/spec-driven-development/SKILL.md` and related skill files | Specs remain a workflow pattern, not a native Antigravity artifact type. |
| Steering | Translate to Antigravity rules | `.agent/rules/*.md` | Persistent context and behavior belong in rules, not in one giant prompt. |
| Powers | Split into rules, skills, MCP, or documented exceptions | Rules, skills, active MCP config | Do not copy Kiro powers directly. |
| Hooks | No documented Kiro-equivalent hook surface is used in KirOpen on Antigravity | Usually rules, skills, approval guidance, or an explicit exception | Hook intent must be translated by behavior, not by file format. |
| MCP | Translate to the active Antigravity MCP surface | Active Antigravity MCP configuration, not a repo-local Kiro JSON clone | Recreate servers in the real Antigravity MCP surface the user is using. |
| Autopilot / Supervised | Translate into Antigravity approval, review, and execution policies | Antigravity settings and collaboration guidance | Treat this as an autonomy preference, not a literal Kiro mode. |
| Chat context like `#File`, `#Folder`, `#Problems`, `#Git Diff` | Reinterpret through Antigravity `@` references, rules, skills, and built-in context tools | Rules, skills, `@` context usage | Kiro chat syntax is not copied literally. |
| Subagents / specialists | Use Antigravity's built-in planning and browser-agent model, plus reusable skills | Rules and skills | Prefer native Antigravity capabilities over extra always-on specialist personas. |
| Internet access | Use Antigravity search, URL reading, and browser subagent behavior | Prompt assembly via vendor snippets | Browser work should stay native to Antigravity when needed. |

</details>


### How To Build It Yourself

<details>
KirOpen is a plain Python script and currently depends only on the Python standard library.

#### Requirements

- Python 3.10 or newer
- `pip`

There are currently no third-party Python dependencies to install.

#### Run the builder

Build both supported harnesses into a review folder:

```bash
python assemble_instructions.py --output-dir review_build codex copilot antigravity
```

Build one harness only:

```bash
python assemble_instructions.py --output-dir review_build codex
python assemble_instructions.py --output-dir review_build copilot
python assemble_instructions.py --output-dir review_build antigravity
```

Build in default-behavior mode:

```bash
python assemble_instructions.py --mode default --output-dir review_build codex
python assemble_instructions.py --mode default --output-dir review_build copilot
python assemble_instructions.py --mode default --output-dir review_build antigravity
```

Run in interactive mode:

```bash
python assemble_instructions.py
```

The builder refuses to overwrite existing generated output. If a target file already exists, delete it manually and rerun.
</details>
