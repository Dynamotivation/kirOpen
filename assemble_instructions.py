"""
Assemble KirOpen guidance into vendor-specific project files.

Supported targets:
  codex   - .codex/agents/*.toml + .agents/skills/*/SKILL.md
  copilot - .github/agents/*.agent.md + .agents/skills/*/SKILL.md + .github/instructions/ + .github/prompts/

Modes:
  agent   - keep KirOpen as a custom agent profile
  default - emit KirOpen into the harness's default-behavior file instead

Usage:
  python assemble_instructions.py [--platform win32|darwin|linux] [--output-dir .] [--mode agent|default] [targets ...]

If no targets are given, all targets are generated.
"""

from __future__ import annotations

import argparse
import platform as plat
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = REPO_ROOT / "templates"
PLATFORM_DIR = TEMPLATES_DIR / "platform-specifics"
VENDOR_DIR = TEMPLATES_DIR / "vendor-specifics"
SKILLS_DIR = TEMPLATES_DIR / "skills"
PROMPTS_DIR = TEMPLATES_DIR / "prompts"
STEERING_DIR = TEMPLATES_DIR / "steering"

ALL_TARGETS = ["codex", "copilot"]

SPEC_SKILLS = [
    "spec-driven-development",
    "requirements-engineering",
    "design-documentation",
    "task-breakdown",
    "quality-assurance",
    "troubleshooting",
]

# ── Shared helpers ────────────────────────────────────────────────────────


def get_variables(
    target: str, platform_override: str | None = None
) -> dict[str, str]:
    platform_name = platform_override or {
        "Windows": "win32",
        "Darwin": "darwin",
        "Linux": "linux",
    }.get(plat.system(), "linux")
    os_map = {"win32": "Windows", "darwin": "macOS", "linux": "Linux"}
    shell_map = {"win32": "PowerShell", "darwin": "zsh", "linux": "bash"}
    now = datetime.now()
    return {
        "PLATFORM": platform_name,
        "OS_NAME": os_map.get(platform_name, "Linux"),
        "SHELL": shell_map.get(platform_name, "bash"),
        "CURRENT_DATE": now.strftime("%B %d, %Y"),
        "DAY_OF_WEEK": now.strftime("%A"),
        "MACHINE_ID": "dynamic-at-runtime",
    }


def infill(text: str, variables: dict[str, str]) -> str:
    return re.sub(
        r"\{\{(\w+)\}\}",
        lambda m: variables.get(m.group(1), m.group(0)),
        text,
    )


def read_vendor_snippet(vendor_name: str, snippet_name: str) -> str:
    path = VENDOR_DIR / vendor_name / f"{snippet_name}.md"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing vendor snippet template: {path}"
        )
    return path.read_text(encoding="utf-8").strip()


def read_shared_template(filename: str) -> str:
    path = TEMPLATES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing shared template: {path}")
    return path.read_text(encoding="utf-8").strip()


def read_platform_commands(platform_name: str) -> str:
    path = PLATFORM_DIR / f"{platform_name}.md"
    return path.read_text(encoding="utf-8").strip()


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text.strip()
    end = text.find("\n---", 3)
    if end == -1:
        return text.strip()
    return text[end + 4 :].strip()


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text.strip()
    end = text.find("\n---", 3)
    if end == -1:
        return "", text.strip()
    return text[: end + 4].strip(), text[end + 4 :].strip()


def collect_skill_bodies(names: list[str]) -> str:
    blocks: list[str] = []
    for name in names:
        path = SKILLS_DIR / name / "SKILL.md"
        if not path.exists():
            raise FileNotFoundError(
                f"Missing skill template: {path}"
            )
        blocks.append(strip_frontmatter(path.read_text(encoding="utf-8")))
    return "\n\n---\n\n".join(blocks).strip()


def read_assembly_template(*parts: str) -> str:
    return (VENDOR_DIR.joinpath(*parts)).read_text(encoding="utf-8")


def read_steering_template(filename: str) -> str:
    path = STEERING_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing steering template: {path}")
    return path.read_text(encoding="utf-8")


def render_assembly_template(
    *parts: str,
    variables: dict[str, str] | None = None,
    replacements: dict[str, str] | None = None,
) -> str:
    text = read_assembly_template(*parts)
    if replacements:
        for key, value in replacements.items():
            text = text.replace(key, value)
    if variables:
        text = infill(text, variables)
    return text


def replace_tokens(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace(f"{{{key}}}", value)
    return text


def build_codex_default_config() -> str:
    return read_assembly_template("codex", "config.toml")


def build_vendor_tokens(vendor_name: str, variables: dict[str, str]) -> dict[str, str]:
    kiro_interop_primer = (
        read_shared_template("kiro-interop-primer.md")
        if vendor_name != "kiro"
        else ""
    )
    return {
        "KIRO_INTEROP_PRIMER": kiro_interop_primer,
        "VENDOR_TOOL_RULES": read_vendor_snippet(vendor_name, "tool-rules"),
        "VENDOR_EXPLORATION_AGENT": read_vendor_snippet(
            vendor_name, "exploration-agent"
        ),
        "VENDOR_PARALLEL_HINT": read_vendor_snippet(
            vendor_name, "parallel-hint"
        ),
        "VENDOR_FEATURES": read_vendor_snippet(vendor_name, "features"),
        "VENDOR_AGENTS": read_vendor_snippet(vendor_name, "agents"),
        "PLATFORM_COMMANDS": read_platform_commands(variables["PLATFORM"]),
    }


def _steering_target_dir(filename: str) -> str:
    name = filename.replace(".instructions.md", "")
    return str(Path(".codex") / f"copy-me-into-your-{name}-directories")


def _global_skill_templates() -> list[tuple[str, str]]:
    skills: list[tuple[str, str]] = []
    for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skills.append((path.parent.name, path.read_text(encoding="utf-8")))
    return skills


def assemble_prompt(
    variables: dict[str, str], vendor_name: str
) -> str:
    system_prompt = (TEMPLATES_DIR / "base-prompt.md").read_text(
        encoding="utf-8"
    )
    system_prompt = infill(
        system_prompt,
        {
            **variables,
            **build_vendor_tokens(vendor_name, variables),
        },
    )
    system_prompt = infill(system_prompt, variables)
    return system_prompt


# ── Collision detection ───────────────────────────────────────────────────


def find_conflicting_outputs(
    out: Path, targets: list[str], mode: str
) -> list[Path]:
    planned: dict[Path, str] = {}
    for target in targets:
        variables = get_variables(target)
        planned.update(plan_target_outputs(target, variables, mode))
    return sorted(path for path in (out / p for p in planned) if path.exists())


def plan_outputs_for_targets(
    targets: list[str], mode: str, platform_override: str | None = None
) -> dict[Path, str]:
    planned: dict[Path, str] = {}
    for target in targets:
        variables = get_variables(target, platform_override)
        planned.update(plan_target_outputs(target, variables, mode))
    return planned


def _prompt_with_default(prompt: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def _prompt_targets() -> list[str]:
    raw = _prompt_with_default(
        "Targets (all, codex, copilot, or comma-separated list)", "all"
    ).lower()
    if raw == "all":
        return list(ALL_TARGETS)

    targets = [part.strip() for part in raw.split(",") if part.strip()]
    invalid = [target for target in targets if target not in ALL_TARGETS]
    if invalid or not targets:
        raise SystemExit(
            "Invalid targets for interactive mode. "
            f"Choose from: {', '.join(ALL_TARGETS)} or 'all'."
        )
    return targets


def _prompt_mode() -> str:
    mode = _prompt_with_default("Mode (agent or default)", "agent").lower()
    if mode not in {"agent", "default"}:
        raise SystemExit("Invalid mode for interactive mode. Choose 'agent' or 'default'.")
    return mode


def _prompt_platform() -> str | None:
    platform_value = _prompt_with_default(
        "Platform override (auto, win32, darwin, linux)", "auto"
    ).lower()
    if platform_value == "auto":
        return None
    if platform_value not in {"win32", "darwin", "linux"}:
        raise SystemExit(
            "Invalid platform for interactive mode. Choose 'auto', 'win32', 'darwin', or 'linux'."
        )
    return platform_value


def interactive_args() -> argparse.Namespace:
    print("Interactive mode")
    targets = _prompt_targets()
    mode = _prompt_mode()
    output_dir = _prompt_with_default("Output directory", ".")
    platform_value = _prompt_platform()
    return argparse.Namespace(
        targets=targets,
        mode=mode,
        output_dir=output_dir,
        platform=platform_value,
    )


# ── Codex builder ─────────────────────────────────────────────────────────


def _codex_spec_skill_body() -> str:
    combined = collect_skill_bodies(SPEC_SKILLS)
    return render_assembly_template(
        "codex",
        "spec_skill_body_prefix.md",
        replacements={"{{COMBINED_SKILLS}}": combined},
    )


def _codex_custom_agents() -> list[tuple[str, str]]:
    return [
        (
            "kiropen_spec.toml",
            f'''\
name = "kiropen_spec"
description = "Spec-driven development specialist for requirements, design, and task breakdown."
developer_instructions = """
{_codex_spec_skill_body()}
"""
''',
        ),
    ]


def _codex_vendor_skills() -> list[tuple[str, str]]:
    return [
        (
            "port-kiro-configuration-to-kiropen-on-codex",
            read_assembly_template(
                "codex",
                "skills",
                "port-kiro-configuration-to-kiropen-on-codex.SKILL.md",
            ),
        ),
    ]


def _codex_steering_placeholders() -> list[tuple[Path, str]]:
    placeholders: list[tuple[Path, str]] = []
    for path in sorted(STEERING_DIR.glob("*.instructions.md")):
        _, body = split_frontmatter(path.read_text(encoding="utf-8"))
        target = Path(_steering_target_dir(path.name)) / "AGENTS.override.md"
        content = f"""\
<!-- Move this file into the directory whose files should receive this guidance. -->
<!-- Source template: templates/steering/{path.name} -->

{body}
"""
        placeholders.append((target, content))
    return placeholders


def _copilot_spec_agent() -> str:
    skills: list[str] = []
    for name in SPEC_SKILLS:
        path = SKILLS_DIR / name / "SKILL.md"
        if not path.exists():
            raise FileNotFoundError(
                f"Missing skill template: {path}"
            )
        skills.append(
            strip_frontmatter(path.read_text(encoding="utf-8"))
        )
    combined = "\n\n---\n\n".join(skills)
    return render_assembly_template(
        "copilot",
        "agents-frontmatter",
        "kiropen-spec.agent.md",
        replacements={"{{COMBINED_SKILLS}}": combined},
    )


def _copilot_path_instructions() -> list[tuple[str, str]]:
    instructions: list[tuple[str, str]] = []
    for path in sorted(STEERING_DIR.glob("*.instructions.md")):
        instructions.append((path.name, path.read_text(encoding="utf-8")))
    return instructions


def _copilot_prompts() -> list[tuple[str, str]]:
    vendor_prompt = (
        "port-kiro-configuration-to-kiropen-on-copilot.prompt.md"
    )
    return [
        (
            vendor_prompt,
            read_assembly_template("copilot", vendor_prompt),
        )
    ]


def plan_codex_outputs(
    variables: dict[str, str], mode: str
) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    prompt_body = assemble_prompt(variables, "codex")

    if mode == "default":
        outputs[Path("CODEX.md")] = prompt_body
        outputs[Path(".codex") / "config.toml"] = build_codex_default_config()

    for filename, content in _codex_custom_agents():
        outputs[Path(".codex") / "agents" / filename] = content

    for name, content in [*_global_skill_templates(), *_codex_vendor_skills()]:
        outputs[Path(".agents") / "skills" / name / "SKILL.md"] = content

    for relative_path, content in _codex_steering_placeholders():
        outputs[relative_path] = content

    return outputs


def plan_copilot_outputs(
    variables: dict[str, str], mode: str
) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    prompt_body = assemble_prompt(variables, "copilot")

    if mode == "default":
        outputs[Path(".github") / "copilot-instructions.md"] = prompt_body

    if mode == "agent":
        outputs[Path(".github") / "agents" / "kiropen.agent.md"] = f"""\
---
name: kiropen
description: "KirOpen AI assistant. Systematic spec-driven development with clear requirements, thoughtful design, and sequenced implementation. Speaks like a dev, writes minimal code."
tools: ["*"]
---

{prompt_body}
"""

    outputs[Path(".github") / "agents" / "kiropen-spec.agent.md"] = _copilot_spec_agent()

    for filename, content in _copilot_path_instructions():
        outputs[Path(".github") / "instructions" / filename] = content

    for name, content in _global_skill_templates():
        outputs[Path(".agents") / "skills" / name / "SKILL.md"] = content

    for filename, content in _copilot_prompts():
        outputs[Path(".github") / "prompts" / filename] = content

    return outputs


def plan_target_outputs(
    target: str, variables: dict[str, str], mode: str
) -> dict[Path, str]:
    if target == "codex":
        return plan_codex_outputs(variables, mode)
    if target == "copilot":
        return plan_copilot_outputs(variables, mode)
    raise ValueError(f"Unknown target: {target}")


def write_outputs(out: Path, outputs: dict[Path, str]) -> list[Path]:
    written: list[Path] = []
    for relative_path, content in outputs.items():
        path = out / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


# ── Main ──────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assemble KirOpen into vendor-specific guidance files"
    )
    parser.add_argument(
        "targets",
        nargs="*",
        choices=ALL_TARGETS,
        default=[],
        help=(
            "Target harnesses to generate. "
            "If omitted, all targets are generated."
        ),
    )
    parser.add_argument(
        "--platform",
        choices=["win32", "darwin", "linux"],
        default=None,
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Root directory to write output into",
    )
    parser.add_argument(
        "--mode",
        choices=["agent", "default"],
        default="agent",
        help="Whether KirOpen should stay a custom agent or replace default harness behavior.",
    )
    if len(sys.argv) == 1:
        args = interactive_args()
    else:
        args = parser.parse_args()

    targets: list[str] = args.targets if args.targets else list(ALL_TARGETS)
    out = Path(args.output_dir).resolve()

    # Only check collisions for the targets being generated
    conflicts = find_conflicting_outputs(out, targets, args.mode)
    if conflicts:
        formatted = "\n".join(
            f"  - {p.relative_to(out)}" for p in conflicts
        )
        raise SystemExit(
            "Refusing to generate because conflicting legacy output "
            "paths are present.\n"
            "Delete these paths manually, then rerun the builder:\n"
            f"{formatted}"
        )

    all_written = write_outputs(
        out,
        plan_outputs_for_targets(targets, args.mode, args.platform),
    )

    variables = get_variables(targets[0], args.platform)
    if (
        variables["PLATFORM"] == "win32"
        and args.output_dir.startswith("/")
        and not args.output_dir.startswith("//")
    ):
        print(
            f"Note: On Windows, '{args.output_dir}' resolves to "
            f"'{out}'"
        )

    print(f"Assembled {', '.join(targets)} in {out}")
    print(f"  Mode: {args.mode}")
    print(f"  Platform: {variables['PLATFORM']}")
    print("  Files:")
    for p in sorted(all_written):
        print(f"    {p.relative_to(out)}")


if __name__ == "__main__":
    main()
