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
import os
import platform as plat
import re
import sys
import tomllib
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
ANSI_ORANGE = "\033[38;5;208m"
ANSI_RESET = "\033[0m"

SPEC_SKILLS = [
    "spec-driven-development",
    "requirements-engineering",
    "design-documentation",
    "task-breakdown",
    "quality-assurance",
    "troubleshooting",
]
SPEC_PHASE_GATE_MARKER_FILES = {
    "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WHEN_TO_USE -->": "when-to-use.md",
    "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_1 -->": "phase-1.md",
    "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_2 -->": "phase-2.md",
    "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_3 -->": "phase-3.md",
    "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WORKFLOW -->": "workflow.md",
    "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_LIGHTWEIGHT -->": "lightweight.md",
}

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


def codex_home_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def codex_user_config_path() -> Path:
    return codex_home_dir() / "config.toml"


def normalize_repo_path_for_codex(repo_path: Path) -> str:
    resolved = str(repo_path.resolve())
    if re.match(r"^[A-Za-z]:", resolved):
        return resolved[0].lower() + resolved[1:]
    return resolved


def _canonical_project_key(project_key: str) -> str:
    canonical = project_key.strip()
    if os.name == "nt":
        canonical = canonical.replace("/", "\\")
        canonical = canonical.rstrip("\\")
        if re.match(r"^[A-Za-z]:", canonical):
            canonical = canonical[0].lower() + canonical[1:]
        return canonical or "\\"

    canonical = canonical.rstrip("/")
    return canonical or "/"


def _render_codex_project_header(project_key: str) -> str:
    if "'" not in project_key:
        return f"[projects.'{project_key}']"
    escaped = project_key.replace("\\", "\\\\").replace('"', '\\"')
    return f'[projects."{escaped}"]'


def _detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _parse_project_section_name(header: str) -> str | None:
    match = re.match(
        r"""^\s*projects\s*\.\s*(?P<quote>['"])(?P<name>.*)(?P=quote)\s*$""",
        header,
    )
    if not match:
        return None
    return match.group("name")


def _section_header_match(line: str) -> re.Match[str] | None:
    return re.match(r"^\s*\[(?P<header>[^\]]+)\]\s*(?:#.*)?$", line.rstrip("\r\n"))


def _find_project_section_range(
    lines: list[str], repo_key: str
) -> tuple[int, int] | None:
    normalized_repo_key = _canonical_project_key(repo_key)
    start: int | None = None
    for index, line in enumerate(lines):
        header_match = _section_header_match(line)
        if not header_match:
            continue
        project_name = _parse_project_section_name(header_match.group("header"))
        if (
            project_name is not None
            and _canonical_project_key(project_name) == normalized_repo_key
        ):
            start = index
            break
    if start is None:
        return None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if _section_header_match(lines[index]):
            end = index
            break
    return start, end


def _last_project_section_end(lines: list[str]) -> int | None:
    last_end: int | None = None
    for index, line in enumerate(lines):
        header_match = _section_header_match(line)
        if not header_match:
            continue
        if _parse_project_section_name(header_match.group("header")) is None:
            continue
        end = len(lines)
        for next_index in range(index + 1, len(lines)):
            if _section_header_match(lines[next_index]):
                end = next_index
                break
        last_end = end
    return last_end


def _replace_or_insert_trust_level(
    lines: list[str], section_start: int, section_end: int, newline: str
) -> list[str]:
    trust_pattern = re.compile(
        r'^(?P<indent>\s*)trust_level\s*=\s*.+?(?P<suffix>\s*(?:#.*)?)$'
    )
    updated_section: list[str] = []
    trust_written = False

    for line in lines[section_start + 1 : section_end]:
        line_without_newline = line.rstrip("\r\n")
        line_ending = line[len(line_without_newline) :]
        trust_match = trust_pattern.match(line_without_newline)
        if not trust_match:
            updated_section.append(line)
            continue
        if trust_written:
            continue
        suffix = trust_match.group("suffix")
        updated_section.append(
            f'{trust_match.group("indent")}trust_level = "trusted"{suffix}{line_ending or newline}'
        )
        trust_written = True

    if not trust_written:
        insertion_index = len(updated_section)
        while insertion_index > 0 and updated_section[insertion_index - 1].strip() == "":
            insertion_index -= 1
        updated_section.insert(
            insertion_index,
            f'trust_level = "trusted"{newline}',
        )

    return [
        *lines[: section_start + 1],
        *updated_section,
        *lines[section_end:],
    ]


def upsert_codex_project_trust(config_text: str, repo_path: Path) -> str:
    normalized_repo_key = normalize_repo_path_for_codex(repo_path)
    text = config_text or ""
    newline = _detect_newline(text)

    existing_repo_key = normalized_repo_key
    if text.strip():
        parsed = tomllib.loads(text)
        projects = parsed.get("projects", {})
        if isinstance(projects, dict):
            for project_key in projects:
                if _canonical_project_key(project_key) == _canonical_project_key(
                    normalized_repo_key
                ):
                    existing_repo_key = project_key
                    break

    lines = text.splitlines(keepends=True)
    section_range = _find_project_section_range(lines, existing_repo_key)
    if section_range is not None:
        updated = "".join(
            _replace_or_insert_trust_level(
                lines, section_range[0], section_range[1], newline
            )
        )
        tomllib.loads(updated)
        return updated

    insertion_index = _last_project_section_end(lines)
    new_section_lines = [
        _render_codex_project_header(normalized_repo_key) + newline,
        f'trust_level = "trusted"{newline}',
    ]

    if not lines:
        updated_lines = new_section_lines
    elif insertion_index is None:
        updated_lines = list(lines)
        if not updated_lines[-1].endswith(("\n", "\r")):
            updated_lines[-1] = updated_lines[-1] + newline
        if updated_lines[-1].strip():
            updated_lines.append(newline)
        updated_lines.extend(new_section_lines)
    else:
        updated_lines = list(lines[:insertion_index])
        if updated_lines and updated_lines[-1].strip():
            updated_lines.append(newline)
        updated_lines.extend(new_section_lines)
        if lines[insertion_index:] and lines[insertion_index].strip():
            updated_lines.append(newline)
        updated_lines.extend(lines[insertion_index:])

    updated = "".join(updated_lines)
    tomllib.loads(updated)
    return updated


def codex_project_trust_level(config_text: str, repo_path: Path) -> str | None:
    if not config_text.strip():
        return None

    parsed = tomllib.loads(config_text)
    projects = parsed.get("projects", {})
    if not isinstance(projects, dict):
        return None

    normalized_repo_key = normalize_repo_path_for_codex(repo_path)
    for project_key, project_config in projects.items():
        if _canonical_project_key(project_key) != _canonical_project_key(
            normalized_repo_key
        ):
            continue
        if not isinstance(project_config, dict):
            return None
        trust_level = project_config.get("trust_level")
        return trust_level if isinstance(trust_level, str) else None

    return None


def write_codex_project_trust(config_path: Path, repo_path: Path) -> tuple[bool, str]:
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        current_text = ""
        if config_path.exists():
            current_text = config_path.read_text(encoding="utf-8")
        updated_text = upsert_codex_project_trust(current_text, repo_path)
        if updated_text != current_text:
            config_path.write_text(updated_text, encoding="utf-8")
            return True, f"Updated Codex trust in {config_path}"
    except tomllib.TOMLDecodeError as exc:
        return (
            False,
            f"Could not update {config_path} because it is not valid TOML: {exc}",
        )
    except OSError as exc:
        return False, f"Could not update {config_path}: {exc}"

    return True, f"Codex trust was already configured in {config_path}"


def _print_orange(text: str) -> None:
    if sys.stdout.isatty():
        print(f"{ANSI_ORANGE}{text}{ANSI_RESET}")
        return
    print(text)


def resolve_codex_root_doc(
    targets: list[str], mode: str, codex_root_doc: str
) -> str:
    if mode != "default":
        return "CODEX.md"

    if codex_root_doc == "agents":
        if targets != ["codex"]:
            raise SystemExit(
                "AGENTS.md can only be selected when generating default mode for Codex alone."
            )
        return "AGENTS.md"

    return "CODEX.md"


def _codex_trust_instructions_text(
    config_path: Path, repo_key: str, root_doc_filename: str
) -> str:
    return (
        f"In order to make Codex follow the {root_doc_filename} file, you need to trust this repo. "
        f"Do you want us to add this repo to your trusted list in your {config_path.parent}/config.toml file?\n"
        "You can also trust this repo manually using the Codex CLI, Codex App or by adding this to your "
        f"{config_path.parent}/config.toml\n"
        f"{_render_codex_project_header(repo_key)}\n"
        'trust_level = "trusted"'
    )


def build_codex_default_choice_prompt(
    config_path: Path,
    repo_key: str,
    root_doc_filename: str,
    include_agents_option: bool,
) -> str:
    lines = [_codex_trust_instructions_text(config_path, repo_key, root_doc_filename)]
    if include_agents_option:
        lines.extend(
            [
                "",
                "Since you are only setting up for Codex, we can also use AGENTS.md",
            ]
        )
    lines.extend(["", "1. Auto trust", "2. Trust manually"])
    if include_agents_option:
        lines.extend(
            [
                "3. Use AGENTS.md instead",
                "Please mind that this will cause issues if you ever switch your AI harness.",
            ]
        )
    return "\n".join(lines)


def normalize_codex_default_choice(
    selection: str, include_agents_option: bool
) -> str | None:
    value = selection.strip().lower()
    if value in {"1", "yes", "auto", "auto trust"}:
        return "yes"
    if value in {"2", "manual", "trust manually"}:
        return "manual"
    if include_agents_option and value in {"3", "agents", "use agents.md instead"}:
        return "agents"
    if value == "no":
        return "manual"
    return None


def switch_codex_root_doc_to_agents(out: Path) -> tuple[bool, str]:
    codex_path = out / "CODEX.md"
    agents_path = out / "AGENTS.md"
    config_path = out / ".codex" / "config.toml"

    if agents_path.exists():
        return (
            False,
            f"Could not switch to AGENTS.md because {agents_path} already exists.",
        )
    if not codex_path.exists():
        return (
            False,
            f"Could not switch to AGENTS.md because {codex_path} was not generated.",
        )

    try:
        codex_path.replace(agents_path)
        if config_path.exists():
            config_path.unlink()
    except OSError as exc:
        return False, f"Could not switch Codex root doc to AGENTS.md: {exc}"

    return (
        True,
        "Switched Codex root doc to AGENTS.md and removed .codex/config.toml.",
    )


def maybe_handle_codex_trust(
    targets: list[str],
    mode: str,
    out: Path,
    codex_trust: str,
    codex_root_doc_filename: str,
) -> None:
    if mode != "default" or "codex" not in targets:
        return

    if codex_root_doc_filename != "CODEX.md":
        return

    config_path = codex_user_config_path()
    repo_key = normalize_repo_path_for_codex(out)
    include_agents_option = targets == ["codex"]
    instructions_text = _codex_trust_instructions_text(
        config_path, repo_key, codex_root_doc_filename
    )
    existing_trust_level: str | None = None
    try:
        if config_path.exists():
            existing_trust_level = codex_project_trust_level(
                config_path.read_text(encoding="utf-8"), out
            )
    except (OSError, tomllib.TOMLDecodeError):
        existing_trust_level = None

    selection = codex_trust
    if existing_trust_level == "trusted":
        return

    if selection == "prompt":
        if not sys.stdin.isatty():
            print("Skipping automatic Codex trust update because no interactive input is available.")
            return
        while True:
            _print_orange(
                build_codex_default_choice_prompt(
                    config_path,
                    repo_key,
                    codex_root_doc_filename,
                    include_agents_option,
                )
            )
            raw_selection = input("Selection [1]: ").strip() or "1"
            selection = normalize_codex_default_choice(
                raw_selection, include_agents_option
            )
            if selection is not None:
                break
            print("Unrecognized Codex setup choice. Please try again.")

    if selection == "yes":
        success, message = write_codex_project_trust(config_path, out)
        print(message)
        return

    if selection == "manual":
        _print_orange(instructions_text)
        return

    if selection == "agents":
        success, message = switch_codex_root_doc_to_agents(out)
        print(message)
        return

    if selection != "no":
        print("Unrecognized Codex trust selection. Leaving the trust list unchanged.")


# ── Collision detection ───────────────────────────────────────────────────


def find_conflicting_outputs(
    out: Path, targets: list[str], mode: str, codex_root_doc: str
) -> list[Path]:
    planned: dict[Path, str] = {}
    for target in targets:
        variables = get_variables(target)
        planned.update(
            plan_target_outputs(target, variables, mode, codex_root_doc, targets)
        )
    return sorted(path for path in (out / p for p in planned) if path.exists())


def plan_outputs_for_targets(
    targets: list[str],
    mode: str,
    platform_override: str | None = None,
    codex_root_doc: str = "auto",
) -> dict[Path, str]:
    planned: dict[Path, str] = {}
    for target in targets:
        variables = get_variables(target, platform_override)
        planned.update(
            plan_target_outputs(target, variables, mode, codex_root_doc, targets)
        )
    return planned


def _prompt_with_default(prompt: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def _prompt_targets() -> list[str]:
    while True:
        raw = _prompt_with_default(
            "Targets (all, codex, copilot, or comma-separated list)", "all"
        ).lower()
        if raw == "all":
            return list(ALL_TARGETS)

        targets = [part.strip() for part in raw.split(",") if part.strip()]
        invalid = [target for target in targets if target not in ALL_TARGETS]
        if not invalid and targets:
            return targets
        print(
            "Invalid targets for interactive mode. "
            f"Choose from: {', '.join(ALL_TARGETS)} or 'all'."
        )


def _prompt_mode() -> str:
    while True:
        mode = _prompt_with_default("Mode (agent or default)", "agent").lower()
        if mode in {"agent", "default"}:
            return mode
        print("Invalid mode for interactive mode. Choose 'agent' or 'default'.")


def _prompt_platform() -> str | None:
    while True:
        platform_value = _prompt_with_default(
            "Platform override (auto, win32, darwin, linux)", "auto"
        ).lower()
        if platform_value == "auto":
            return None
        if platform_value in {"win32", "darwin", "linux"}:
            return platform_value
        print(
            "Invalid platform for interactive mode. Choose 'auto', 'win32', 'darwin', or 'linux'."
        )


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
        codex_trust="prompt",
        codex_root_doc="auto",
    )


# ── Codex builder ─────────────────────────────────────────────────────────


def _codex_spec_skill_infixes() -> dict[str, str]:
    infixes: dict[str, str] = {}
    for marker, filename in SPEC_PHASE_GATE_MARKER_FILES.items():
        infixes[marker] = read_assembly_template(
            "codex", "spec-phase-gates-infixes", filename
        ).strip()
    return infixes


def _inject_skill_infixes(
    skill_body: str, infixes: dict[str, str]
) -> str:
    rendered = skill_body
    for marker, infix_text in infixes.items():
        if marker not in rendered:
            raise ValueError(f"Missing skill infix marker: {marker}")
        rendered = rendered.replace(marker, infix_text)
    return rendered


def _codex_spec_skill_body() -> str:
    combined = collect_skill_bodies(SPEC_SKILLS)
    combined = _inject_skill_infixes(combined, _codex_spec_skill_infixes())
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
    variables: dict[str, str], mode: str, root_doc_filename: str
) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    prompt_body = assemble_prompt(variables, "codex")

    if mode == "default":
        outputs[Path(root_doc_filename)] = prompt_body
        if root_doc_filename == "CODEX.md":
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
    target: str,
    variables: dict[str, str],
    mode: str,
    codex_root_doc: str = "auto",
    targets: list[str] | None = None,
) -> dict[Path, str]:
    selected_targets = targets or [target]
    if target == "codex":
        return plan_codex_outputs(
            variables,
            mode,
            resolve_codex_root_doc(selected_targets, mode, codex_root_doc),
        )
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
    parser.add_argument(
        "--codex-trust",
        choices=["prompt", "yes", "no", "manual"],
        default="prompt",
        help=(
            "When generating Codex default mode, choose whether to prompt, "
            "write trust automatically, or leave it for manual setup."
        ),
    )
    parser.add_argument(
        "--codex-root-doc",
        choices=["auto", "codex", "agents"],
        default="auto",
        help=(
            "For Codex default mode, choose whether to keep CODEX.md or, when "
            "Codex is the only target, use AGENTS.md instead."
        ),
    )
    if len(sys.argv) == 1:
        args = interactive_args()
    else:
        args = parser.parse_args()

    targets: list[str] = args.targets if args.targets else list(ALL_TARGETS)
    out = Path(args.output_dir).resolve()
    codex_root_doc_filename = resolve_codex_root_doc(
        targets, args.mode, args.codex_root_doc
    )

    # Only check collisions for the targets being generated
    conflicts = find_conflicting_outputs(
        out, targets, args.mode, args.codex_root_doc
    )
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
        plan_outputs_for_targets(
            targets, args.mode, args.platform, args.codex_root_doc
        ),
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

    maybe_handle_codex_trust(
        targets,
        args.mode,
        out,
        args.codex_trust,
        codex_root_doc_filename,
    )


if __name__ == "__main__":
    main()
