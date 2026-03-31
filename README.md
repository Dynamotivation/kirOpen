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

## Table Of Contents

- [What KirOpen Enables](#what-kiropen-enables)
- [Supported Harnesses and IDEs](#supported-harnesses-and-ides)
  - [GitHub Copilot](#github-copilot)
  - [OpenAI Codex](#openai-codex)

## What KirOpen Enables

- Spec-driven development
  Requirements, design, and task planning under `.kiro/specs/...`
- Vibe mode and spec mode
  Lightweight exploratory work versus structured planned work
- Similar model behavior through observed guidelines and guardrails
- Conversion skill from Kiro's Steering, Hooks, MCP and Powers formats into each harness's native equivalents (if supported)

## Deliberate Differences

- Kiro may claim to possess an AI prompting guide skill, but this is omitted in KirOpen since different, non-Claude models respond differently to prompts.
- The `create-steering-documents` skill is updated to create canonical `.kiro/steering/*.md` files plus wrapper files for each supported harness, instead of trying to copy Kiro steering files directly into each harness's native format. This preserves the original Kiro steering content as the source of truth avoids duplication.

## Supported Harnesses and IDEs
The following Harnesses and IDEs are supported.

### GitHub Copilot

[Install into new project](#installing-into-empty-repositories)

<table>
  <tr>
    <td align="center"><img src="docs/screenshots/copilot-1.avif" /></td>
    <td align="center"><img src="docs/screenshots/copilot-2.avif" /></td>
    <td align="center"><img src="docs/screenshots/copilot-3.avif" /></td>
  </tr>
  <tr>
    <td align="center"><em>KirOpen in action</em></td>
    <td align="center"><em>Spec Mode and Bugfix</em></td>
    <td align="center"><em>Spec Mode selection</em></td>
  </tr>
</table>

<table>
  <tr>
    <td align="center"><img src="docs/screenshots/copilot-4.avif" /></td>
  </tr>
  <tr>
    <td align="center"><em>Spec Mode in CLI</em></td>
  </tr>
</table>

#### Features

| Feature name | Status | Details |
|---|---|---|
| Kiro Migration Skill | ✅ | Generated as `port-kiro-configuration-to-kiropen-on-copilot` for porting Kiro configuration into Copilot-native features. |
| Vibe Mode | ✅ | Fully supported vibe mode as long as KirOpen provided `copilot-instructions.md` is installed. Disable plan mode during vibe sessions. |
| Spec Mode | ✅ | Implemented entirely in KirOpen's `copilot-instructions.md` and skills due to recurring bugs in agent-skill-interactions in Copilot. Disable plan mode during spec sessions. |
| Spec Agent | ⚠️ | `kiropen.agent.md` is generated, but contains token inefficient skill workarounds due to mentioned issues. Use only if you can't spare `copilot-instructions.md` and the skills won't behave correctly with your custom files in place. |
| UI Dialogs | ✅ | KirOpen will use Copilot UI and CLI dialogs like Kiro, with chat fallback if tool is unavailable. |
| Kiro Hooks | ⚠️ | Copilot hooks are supported, but behavior depends on the active Copilot surface. Per GitHub docs they are available for Copilot coding agent and Copilot CLI, and Windows hook definitions must use the `powershell` field instead of `bash`. |
| Steering Support | ✅ | Steering wrappers in `.github/instructions/*.instructions.md` pointing to `.kiro/steering/*` are supported and can be generated using the migration skill. |
| Kiro Powers | ⚠️ | Kiro Powers are not supported as a first-class Copilot feature, but migration skill offers best effort conversions using scripts, skills and MCPs. |

#### IDE & CLI Support

- VS Code
- Copilot CLI

#### Untested IDEs & CLIs

- OpenCode
- JetBrains (Rider, IntelliJ IDEA, PyCharm, etc.)
- GitHub.com coding agent
- Visual Studio
- Other

<details>
<summary>Install into existing project</summary>

Generate into a temporary review folder first:

```bash
python assemble_instructions.py --output-dir review_copilot copilot
```

In `agent` mode, review and copy:

- `review_copilot/.github/agents/kiropen.agent.md` -> `<repo>/.github/agents/kiropen.agent.md`
- `review_copilot/.github/agents/spec-mode.agent.md` -> `<repo>/.github/agents/spec-mode.agent.md`
- `review_copilot/.github/instructions/*.instructions.md` -> `<repo>/.github/instructions/*.instructions.md`
- `review_copilot/.agents/skills/*/SKILL.md` -> `<repo>/.agents/skills/*/SKILL.md`

If you built in `default` mode, also copy:

- `review_copilot/.github/copilot-instructions.md` -> `<repo>/.github/copilot-instructions.md`

> **Known issue:** Copilot agent subagent depth is currently limited to 1, which means the `spec-mode` agent cannot spawn a discovery subagent during the spec workflow. Skills should be usable by agents per the [this resolved Copilot issue](https://github.com/github/copilot-cli/issues/839), but is reported broken again ([related report](https://github.com/easingthemes/dx-aem-flow/issues/20)). Workaround: run codebase exploration in the parent agent before delegating to `spec-mode`, or use default mode where the main agent runs skills directly with full tool access.

</details>

<br />
<br />

### OpenAI Codex

[Install into new project](#installing-into-empty-repositories)

<!-- <table>
  <tr>
    <td align="center"><em>KirOpen in action</em><br /><img src="docs/screenshots/codex-1.png" /></td>
    <td align="center"><em>Spec Mode and Bugfix</em><br /><img src="docs/screenshots/codex-2.png" /></td>
    <td align="center"><em>Spec Mode selection</em><br /><img src="docs/screenshots/codex-3.png" /></td>
  </tr>
  <tr>
    <td align="center"><em>Spec Mode in CLI</em><br /><img src="docs/screenshots/codex-4.png" /></td>
  </tr>
</table> -->

#### Features

| Feature name | Status | Details |
|---|---|---|
| Kiro Migration Skill | ✅ | Generated as `port-kiro-configuration-to-kiropen-on-codex` for porting Kiro configuration into Codex-native features. |
| Vibe Mode | ✅ | Fully supported vibe mode as long as KirOpen provided `CODEX.md` and `config.toml` is installed. Disable plan mode during vibe sessions. |
| Spec Mode | ✅ | Implemented entirely in KirOpen's `CODEX.md` and skills. Disable plan mode during spec sessions. |
| Spec Agent | ? | TBD |
| UI Dialogs | ❌ | Not supported. Codex does not provide Kiro-like UI dialog interactions here, and structured user-input tooling is not available in normal Default mode, so KirOpen must fall back to plain chat questions and replies. |
| Kiro Hooks | ⚠️ | Codex hooks exist, but OpenAI documents them as experimental and currently disabled on Windows. They require `codex_hooks = true` in `config.toml`, so KirOpen can only offer best-effort hook mapping today. |
| Steering Support | ✅ | Steering wrappers in `AGENTS.override.md` pointing to `.kiro/steering/` are supported and can be generated using the migration skill. You can also prompt KirOpen to find locations for them since these are file location dependant. |
| Kiro Powers | ⚠️ | Kiro Powers are not supported as a first-class Codex feature, but migration skill offers best effort conversions using skills, hooks, MCPs and Codex guidance files. |

#### IDE & CLI Support

- VS Code

#### Untested IDEs & CLIs

- Codex CLI
- Codex App
- OpenCode
- T3 Code
- JetBrains AI Assistant Codex Agent (Rider, IntelliJ IDEA, PyCharm, etc.)
- Other

<details>
<summary>Install into existing project</summary>

Generate into a temporary review folder first:

```bash
python assemble_instructions.py --output-dir review_codex codex
```

In `agent` mode, review and copy:

- `review_codex/.codex/agents/spec_mode.toml` -> `<repo>/.codex/agents/spec_mode.toml`
- `review_codex/.agents/skills/...` -> `<repo>/.agents/skills/...`
- `review_codex/.kiropen/codex-guide.md` -> `<repo>/.kiropen/codex-guide.md`
- `review_codex/.codex/copy-me-into-your-api-directories/AGENTS.override.md` -> Move into the API directory that should receive that scoped guidance
- `review_codex/.codex/copy-me-into-your-environment-directories/AGENTS.override.md` -> Move into the environment or config directory that should receive that scoped guidance
- `review_codex/.codex/copy-me-into-your-frontend-directories/AGENTS.override.md` -> Move into the frontend or app directory that should receive that scoped guidance

If you built in `default` mode, also copy:

- `review_codex/CODEX.md` -> `<repo>/CODEX.md`
- `review_codex/.codex/config.toml` -> `<repo>/.codex/config.toml`

If you built with `--codex-root-doc agents`, copy instead:

- `review_codex/AGENTS.md` -> `<repo>/AGENTS.md`

</details>

## Planned Harnesses

- Antigravity (Soon)
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
python assemble_instructions.py [--platform win32|darwin|linux] [--output-dir <dir>] [--mode agent|default] [codex] [copilot]
```

If your system exposes Python as `python3`, use `python3` in the examples below.

## Choosing A Mode

- `agent`
  Use this when you want KirOpen to stay mostly opt-in. In this mode, the builder generates harness-specific agents, skills, prompts, and scoped guidance surfaces, but it does not try to replace the harness's default project-wide behavior unless that harness always needs a supporting file for activation.
- `default`
  Use this when you want KirOpen to shape the harness's default behavior for the whole repository. In this mode, the builder also emits the harness's main default instruction file, such as `CODEX.md` for Codex or `.github/copilot-instructions.md` for Copilot.
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
python /path/to/kirOpen/assemble_instructions.py --mode default --output-dir . codex
python /path/to/kirOpen/assemble_instructions.py --mode default --codex-root-doc agents --output-dir . codex
python /path/to/kirOpen/assemble_instructions.py --mode default --output-dir . copilot
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
python assemble_instructions.py --output-dir review_build codex copilot
```

Build one harness only:

```bash
python assemble_instructions.py --output-dir review_build codex
python assemble_instructions.py --output-dir review_build copilot
```

Build in default-behavior mode:

```bash
python assemble_instructions.py --mode default --output-dir review_build codex
python assemble_instructions.py --mode default --output-dir review_build copilot
```

Run in interactive mode:

```bash
python assemble_instructions.py
```

The builder refuses to overwrite existing generated output. If a target file already exists, delete it manually and rerun.
</details>
