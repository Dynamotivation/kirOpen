#!/usr/bin/env python3
"""
Assemble Kiro system prompt into GitHub Copilot custom agent format.

Reads the canonical system-prompt.md, infills vendor-specific blocks from
vendor/copilot.md, platform commands from platform-specifics.md, and runtime
variables. Outputs the .github/ directory structure Copilot expects.

Usage:
  python scripts/assemble_copilot.py [--platform win32|darwin|linux] [--output-dir .]
"""

import argparse
import os
import platform as plat
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_DIR = REPO_ROOT / ".kiro" / "system"


# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------

def get_variables(platform_override: str | None = None) -> dict[str, str]:
    p = platform_override or {"Windows": "win32", "Darwin": "darwin", "Linux": "linux"}.get(plat.system(), "linux")
    os_map = {"win32": "Windows", "darwin": "macOS", "linux": "Linux"}
    shell_map = {"win32": "PowerShell", "darwin": "zsh", "linux": "bash"}
    now = datetime.now()
    return {
        "PLATFORM": p,
        "OS_NAME": os_map.get(p, "Linux"),
        "SHELL": shell_map.get(p, "bash"),
        "CURRENT_DATE": now.strftime("%B %d, %Y"),
        "DAY_OF_WEEK": now.strftime("%A"),
        "MODEL_NAME": "Claude Opus 4.6",
        "MODEL_DESCRIPTION": "The latest Claude Opus model with 1M context window",
        "MACHINE_ID": "dynamic-at-runtime",
    }


def infill(text: str, variables: dict[str, str]) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: variables.get(m.group(1), m.group(0)), text)


# ---------------------------------------------------------------------------
# Vendor snippet parser
# ---------------------------------------------------------------------------

def parse_vendor_snippets(path: Path) -> dict[str, str]:
    """Parse a vendor file into {SECTION_NAME: content} dict.

    Vendor files use '## VENDOR_TOOL_RULES', '## VENDOR_FEATURES', '## VENDOR_AGENTS'
    as section headers. Everything between headers belongs to that section.
    """
    text = path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    current_key = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("## VENDOR_"):
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line.replace("## ", "").strip()
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


# ---------------------------------------------------------------------------
# Platform commands parser
# ---------------------------------------------------------------------------

def parse_platform_commands(path: Path) -> dict[str, str]:
    """Parse platform-specifics.md into {platform: commands_block} dict."""
    text = path.read_text(encoding="utf-8")
    platforms: dict[str, str] = {}
    current_key = None
    current_lines: list[str] = []
    in_block = False

    for line in text.splitlines():
        if line.startswith("## ") and line.strip("## \n") in ("win32", "darwin", "linux"):
            if current_key:
                platforms[current_key] = "\n".join(current_lines).strip()
            current_key = line.strip("## \n")
            current_lines = []
            in_block = False
        elif current_key is not None:
            if line.strip() == "```" and not in_block:
                in_block = True
                continue
            elif line.strip() == "```" and in_block:
                in_block = False
                continue
            if in_block:
                current_lines.append(line)

    if current_key:
        platforms[current_key] = "\n".join(current_lines).strip()

    return platforms


# ---------------------------------------------------------------------------
# Assemble the main agent body
# ---------------------------------------------------------------------------

def assemble_prompt(variables: dict[str, str]) -> str:
    system_prompt = (SYSTEM_DIR / "system-prompt.md").read_text(encoding="utf-8")
    vendor = parse_vendor_snippets(SYSTEM_DIR / "vendor" / "copilot.md")
    platforms = parse_platform_commands(SYSTEM_DIR / "platform-specifics.md")

    # Inject vendor blocks
    system_prompt = system_prompt.replace("{{VENDOR_TOOL_RULES}}", vendor.get("VENDOR_TOOL_RULES", ""))
    system_prompt = system_prompt.replace("{{VENDOR_FEATURES}}", vendor.get("VENDOR_FEATURES", ""))
    system_prompt = system_prompt.replace("{{VENDOR_AGENTS}}", vendor.get("VENDOR_AGENTS", ""))

    # Inject platform commands
    system_prompt = system_prompt.replace("{{PLATFORM_COMMANDS}}", platforms.get(variables["PLATFORM"], ""))

    # Inject all scalar variables
    system_prompt = infill(system_prompt, variables)

    return system_prompt


# ---------------------------------------------------------------------------
# Output builders
# ---------------------------------------------------------------------------

def build_copilot_instructions(variables: dict[str, str]) -> str:
    return infill("""You are Kiro, an AI assistant built to assist developers.

You talk like a human, not like a bot. You reflect the user's input style.

## Response Style
- Be decisive, precise, and clear. Lose the fluff.
- Speak like a dev when necessary. Be relatable otherwise.
- Supportive, not authoritative. Warm and friendly.
- Concise and direct. No markdown headers unless multi-step. No bold text.
- Write the ABSOLUTE MINIMAL code needed. No gold-plating.
- Prioritize actionable information over general explanations.
- Don't repeat yourself.
- Reply in the user's language when possible.

## Rules
- Never discuss sensitive, personal, or emotional topics.
- Substitute PII with placeholders (e.g. [name], [email]).
- Decline requests for malicious code.
- Always prioritize security best practices.
- Check all code for syntax errors before presenting it.
- Never claim WCAG compliance — that requires manual testing.
- DO NOT automatically add tests unless explicitly requested.

## Platform
Operating System: {{OS_NAME}}
Platform: {{PLATFORM}}
""", variables)


def build_spec_agent() -> str:
    skills = []
    for name in ["spec-driven-development", "requirements-engineering",
                  "design-documentation", "task-breakdown",
                  "quality-assurance", "troubleshooting"]:
        path = REPO_ROOT / "skills" / name / "SKILL.md"
        if path.exists():
            content = path.read_text(encoding="utf-8")
            if content.startswith("---"):
                end = content.index("---", 3)
                content = content[end + 3:].strip()
            skills.append(content)

    combined = "\n\n---\n\n".join(skills)
    return f"""---
name: kiro-spec
description: "Spec-driven development specialist. Three-phase workflow: Requirements (EARS) to Design to Tasks. Use for creating specs, writing requirements, designing systems, or planning implementation."
tools: ["read", "search", "edit", "execute"]
---

You are Kiro's spec-driven development specialist. You guide users through
the three-phase workflow: Requirements, Design, Tasks.

{combined}
"""


def build_mcp_setup_agent() -> str:
    return """---
name: kiro-mcp-setup
description: "Configures MCP servers for GitHub Copilot in VS Code, CLI, or Coding Agent. Invoke with 'set up MCP' or 'configure MCP server'."
tools: ["read", "edit", "execute"]
---

You help users configure MCP (Model Context Protocol) servers for GitHub Copilot.

## Where MCP Configs Live

### VS Code (Copilot Chat)
- User-level: Add to VS Code `settings.json` under `"mcp"` key
- Workspace-level: Create `.vscode/mcp.json` in the repo root

Format for `.vscode/mcp.json`:
```json
{
  "servers": {
    "server-name": {
      "type": "stdio",
      "command": "uvx",
      "args": ["package-name@latest"],
      "env": {}
    }
  }
}
```

### Copilot CLI
- Config file: `~/.copilot/mcp-config.json`
- Add via interactive: `/mcp add` in CLI
- Format:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name@latest"],
      "env": {}
    }
  }
}
```

### Copilot Coding Agent (github.com)
- Configured in repository settings on GitHub.com under Copilot settings
- Or in custom agent YAML frontmatter:
```yaml
mcp-servers:
  server-name:
    type: local
    command: uvx
    args: ["package-name@latest"]
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

## Installation Steps

1. Ask the user which environment they want to configure (VS Code, CLI, or Coding Agent)
2. Ask which MCP server they want to add
3. Check if the config file already exists — if so, merge, don't overwrite
4. Write the configuration
5. Tell the user to reload/restart if needed

## Common MCP Servers
- `awslabs.aws-documentation-mcp-server@latest` — AWS docs
- `@anthropic-ai/claude-code-mcp-server@latest` — Claude Code tools
- `@playwright/mcp@latest` — Browser automation

## Prerequisites
The `uvx` command requires `uv` (Python package manager). If not installed,
suggest: `pip install uv` or see https://docs.astral.sh/uv/getting-started/installation/
"""


def build_path_instructions() -> list[tuple[str, str]]:
    return [
        ("frontend.instructions.md", """---
applyTo: "**/*.tsx,**/*.jsx,**/*.vue,**/*.svelte"
---

# Frontend Development Standards

- Use functional components with hooks (React)
- Keep components small and focused
- Implement proper prop validation
- Use TypeScript for type safety
- Follow component composition patterns
- Implement responsive design with mobile-first approach
- Use semantic HTML elements and proper ARIA attributes
- Implement code splitting and lazy loading
- Monitor bundle size and performance metrics
"""),
        ("api.instructions.md", """---
applyTo: "**/*api*,**/*route*,**/*controller*,**/*endpoint*"
---

# API Design Guidelines

- Use HTTP methods appropriately (GET, POST, PUT, DELETE, PATCH)
- Follow resource-based URL patterns: /api/v1/resources/{id}
- Use plural nouns for resource collections
- Implement proper HTTP status codes
- Include API versioning in URL path
- Use JSON for request and response bodies
- Include pagination for list endpoints
- Implement proper error response format with code, message, and details
- Use JWT tokens for stateless authentication
- Rate limit API endpoints to prevent abuse
"""),
        ("environment.instructions.md", """---
applyTo: "package.json,requirements.txt,Dockerfile,docker-compose.yml,Makefile,*.toml"
---

# Development Environment Standards

- Use lockfiles for reproducible builds (package-lock.json, poetry.lock, etc.)
- Never commit actual .env files — use .env.example as template
- Document all required environment variables in README
- Use migrations for all database schema changes
- Use structured logging with appropriate log levels
- Include health checks in containerized applications
- Ensure builds are reproducible across environments
"""),
    ]


def build_prompts() -> list[tuple[str, str]]:
    return [
        ("create-spec.prompt.md", """# Create a Spec

I need to build a new feature. Guide me through the three-phase spec process:

1. **Requirements**: Help me capture user stories and EARS-format acceptance criteria
2. **Design**: Create a technical design document with architecture, data models, and interfaces
3. **Tasks**: Break the design into sequenced 2-4 hour implementation tasks

Start by asking me about the feature, the tech stack, constraints, and who the users are.
Then work through requirements first. Don't skip ahead to design until requirements are validated.

Reference: [spec-driven-development](../../skills/spec-driven-development/SKILL.md)
"""),
        ("create-steering.prompt.md", """# Create Steering Documents

Analyze this project and create appropriate path-specific instruction files.

Look at:
- Languages and frameworks in use
- Directory structure and conventions
- Existing config files (linters, formatters, CI)
- Package manager and build tools

Then create `.github/instructions/` files with path-specific standards for:
- Frontend code (if applicable)
- API/backend code (if applicable)
- Environment/config files (if applicable)

Keep guidelines specific and actionable. Include code examples for complex conventions.

Reference: [create-steering-documents](../../skills/create-steering-documents/SKILL.md)
"""),
        ("review-requirements.prompt.md", """# Review Requirements

Review the requirements document and check:

1. Are all requirements using EARS format (WHEN/IF...THEN...SHALL)?
2. Is every requirement testable and measurable?
3. Are edge cases and error cases documented?
4. Do any requirements conflict with each other?
5. Are there gaps in the user journey?
6. Are non-functional requirements captured (performance, security)?
7. Is out-of-scope explicitly stated?
8. Are there any implementation details that should be removed?

Provide a validation summary with specific issues and suggestions.

Reference: [requirements-engineering](../../skills/requirements-engineering/SKILL.md)
"""),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Assemble Kiro into GitHub Copilot format")
    parser.add_argument("--platform", choices=["win32", "darwin", "linux"], default=None)
    parser.add_argument("--output-dir", default=".", help="Root directory to write .github/ into")
    args = parser.parse_args()

    variables = get_variables(args.platform)
    out = Path(args.output_dir)
    prompt_body = assemble_prompt(variables)
    tool_ref = (SYSTEM_DIR / "tool-reference.md").read_text(encoding="utf-8")

    for d in [".github", ".github/agents", ".github/instructions", ".github/prompts"]:
        (out / d).mkdir(parents=True, exist_ok=True)

    # 1. Repo-wide instructions
    (out / ".github/copilot-instructions.md").write_text(
        build_copilot_instructions(variables), encoding="utf-8")

    # 2. Main agent = assembled prompt + tool reference
    agent_content = f"""---
name: kiro
description: "Kiro AI assistant. Systematic spec-driven development with clear requirements, thoughtful design, and sequenced implementation. Speaks like a dev, writes minimal code."
tools: ["*"]
---

{prompt_body}
"""
    (out / ".github/agents/kiro.agent.md").write_text(agent_content, encoding="utf-8")

    # 3. Spec agent
    (out / ".github/agents/kiro-spec.agent.md").write_text(build_spec_agent(), encoding="utf-8")

    # 4. MCP setup agent
    (out / ".github/agents/kiro-mcp-setup.agent.md").write_text(build_mcp_setup_agent(), encoding="utf-8")

    # 5. Path-specific instructions
    for filename, content in build_path_instructions():
        (out / f".github/instructions/{filename}").write_text(content, encoding="utf-8")

    # 6. Reusable prompts
    for filename, content in build_prompts():
        (out / f".github/prompts/{filename}").write_text(content, encoding="utf-8")

    print(f"Assembled Copilot structure in {out / '.github'}/")
    print(f"  Platform: {variables['PLATFORM']} ({variables['OS_NAME']})")
    print(f"  Files:")
    for p in sorted((out / ".github").rglob("*.md")):
        print(f"    {p.relative_to(out)}")


if __name__ == "__main__":
    main()
