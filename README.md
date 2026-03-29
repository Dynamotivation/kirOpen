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

## Deliberate Differences

- Kiro may claim to possess an AI prompting guide skill, but this is omitted in KirOpen since different, non-Claude models respond differently to prompts.
- The `create-steering-documents` skill is updated to create canonical `.kiro/steering/*.md` files plus wrapper files for each supported harness, instead of trying to copy Kiro steering files directly into each harness's native format. This preserves the original Kiro steering content as the source of truth avoids duplication.

## Supported Harnesses

- Codex
- GitHub Copilot

## Planned Harnesses

- Antigravity
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

#### How to merge into conflicting repositories

<details>
<summary><strong>Codex</strong></summary>

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
