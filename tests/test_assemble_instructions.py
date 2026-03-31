import re
import tomllib
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from assemble_instructions import (
    BUILDER_VERSION,
    _select_mode_interactively,
    assemble_prompt,
    build_codex_default_choice_prompt,
    codex_project_trust_level,
    effective_mode_for_target,
    fallback_targets_for_mode,
    get_variables,
    interactive_args,
    mode_fallback_warning,
    maybe_handle_codex_trust,
    normalize_codex_default_choice,
    normalize_mode,
    normalize_repo_path_for_codex,
    _prompt_mode,
    _prompt_targets,
    plan_outputs_for_targets,
    resolve_codex_root_doc,
    upsert_codex_project_trust,
    supported_modes_for_targets,
    validate_mode_for_targets,
)


class CodexTrustConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_path = Path(__file__).resolve().parent.parent / "FakeRepo"
        self.repo_key = normalize_repo_path_for_codex(self.repo_path)

    def test_windows_repo_key_uses_lower_drive_and_verbatim_path(self) -> None:
        if self.repo_path.drive:
            self.assertEqual(self.repo_key[0], self.repo_key[0].lower())
            self.assertIn("FakeRepo", self.repo_key)
            self.assertIn("kirOpen", self.repo_key)
            self.assertIn("\\", self.repo_key)

    def test_updates_existing_repo_section_in_place(self) -> None:
        existing_key = self.repo_key
        if self.repo_path.drive:
            existing_key = self.repo_key[0].upper() + self.repo_key[1:]
        config = (
            f"[projects.'{existing_key}']\n"
            'trust_level = "read-only"\n'
            'approval_policy = "on-request"\n'
            "\n"
            "[features]\n"
            "codex_hooks = false\n"
        )

        updated = upsert_codex_project_trust(config, self.repo_path)

        self.assertIn(f"[projects.'{existing_key}']", updated)
        if existing_key != self.repo_key:
            self.assertNotIn(f"[projects.'{self.repo_key}']", updated)
        self.assertIn('trust_level = "trusted"', updated)
        self.assertIn('approval_policy = "on-request"', updated)
        self.assertEqual(updated.count('trust_level = "trusted"'), 1)

    def test_miscapitalized_windows_repo_key_does_not_match_existing_section(self) -> None:
        if not self.repo_path.drive:
            self.skipTest("Windows-specific path semantics")

        miscapitalized_key = self.repo_key.replace("kirOpen", "kiropen")
        config = (
            f"[projects.'{miscapitalized_key}']\n"
            'trust_level = "read-only"\n'
            "\n"
            "[features]\n"
            "codex_hooks = false\n"
        )

        updated = upsert_codex_project_trust(config, self.repo_path)

        self.assertIn(f"[projects.'{miscapitalized_key}']", updated)
        self.assertIn(f"[projects.'{self.repo_key}']", updated)
        self.assertEqual(updated.count('trust_level = "trusted"'), 1)
        self.assertIn('trust_level = "read-only"', updated)

    def test_inserts_trust_level_into_existing_repo_section(self) -> None:
        config = (
            f"[projects.'{self.repo_key}']\n"
            'approval_policy = "on-request"\n'
            "\n"
            "[features]\n"
            "codex_hooks = false\n"
        )

        updated = upsert_codex_project_trust(config, self.repo_path)
        project_section = updated.split("[features]")[0]

        self.assertIn('approval_policy = "on-request"', project_section)
        self.assertIn('trust_level = "trusted"', project_section)
        self.assertEqual(updated.count(f"[projects.'{self.repo_key}']"), 1)

    def test_adds_new_repo_section_after_existing_project_sections(self) -> None:
        other_repo_key = f"{self.repo_key}-other"
        config = (
            f"[projects.'{other_repo_key}']\n"
            'trust_level = "trusted"\n'
            "\n"
            "[features]\n"
            "codex_hooks = false\n"
        )

        updated = upsert_codex_project_trust(config, self.repo_path)

        features_index = updated.index("[features]")
        new_project_index = updated.index(f"[projects.'{self.repo_key}']")
        self.assertLess(new_project_index, features_index)
        self.assertEqual(updated.count(f"[projects.'{self.repo_key}']"), 1)
        self.assertEqual(updated.count('trust_level = "trusted"'), 2)

    def test_invalid_toml_raises_parse_error(self) -> None:
        config = (
            "[projects.'broken']\n"
            'trust_level = "trusted"\n'
            'trust_level = "read-only"\n'
        )

        with self.assertRaises(tomllib.TOMLDecodeError):
            upsert_codex_project_trust(config, self.repo_path)

    def test_reads_existing_trusted_project_level(self) -> None:
        config = (
            f"[projects.'{self.repo_key}']\n"
            'trust_level = "trusted"\n'
        )

        trust_level = codex_project_trust_level(config, self.repo_path)

        self.assertEqual(trust_level, "trusted")


class CodexRootDocTests(unittest.TestCase):
    def test_codex_default_choice_prompt_includes_agents_option(self) -> None:
        config_path = Path(r"C:\Users\Daniel\.codex\config.toml")
        prompt = build_codex_default_choice_prompt(
            config_path,
            r"d:\source\repos\kirOpen Codex Test",
            "CODEX.md",
            True,
        )

        self.assertIn(
            "Since you are only setting up for Codex, we can also use AGENTS.md",
            prompt,
        )
        self.assertIn(
            "Please mind that this will cause issues if you ever switch your AI harness.",
            prompt,
        )
        self.assertIn("1. Auto trust", prompt)
        self.assertIn("2. Trust manually", prompt)
        self.assertIn("3. Use AGENTS.md instead", prompt)
        self.assertIn(f"\"{config_path}\"", prompt)

    def test_codex_default_choice_parser_supports_three_options(self) -> None:
        self.assertEqual(normalize_codex_default_choice("1", True), "yes")
        self.assertEqual(normalize_codex_default_choice("2", True), "manual")
        self.assertEqual(normalize_codex_default_choice("3", True), "agents")
        self.assertIsNone(normalize_codex_default_choice("3", False))

    def test_prompt_mode_retries_after_invalid_choice(self) -> None:
        with (
            patch("builtins.input", side_effect=["wrong", "default"]),
            patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            selection = _prompt_mode(["codex"])

        self.assertEqual(selection, "default")
        self.assertIn("Invalid mode for interactive mode.", stdout.getvalue())

    def test_prompt_mode_accepts_always_alias(self) -> None:
        with patch("builtins.input", side_effect=["always"]):
            selection = _prompt_mode(["codex"])
        self.assertEqual(selection, "default")

    def test_copilot_prompt_mode_accepts_lite(self) -> None:
        with patch("builtins.input", side_effect=["lite"]):
            selection = _prompt_mode(["copilot"])
        self.assertEqual(selection, "lite")

    def test_mixed_prompt_mode_accepts_lite(self) -> None:
        with patch("builtins.input", side_effect=["lite"]):
            selection = _prompt_mode(["codex", "copilot"])
        self.assertEqual(selection, "lite")

    def test_prompt_targets_retries_after_invalid_choice(self) -> None:
        with (
            patch("builtins.input", side_effect=["wat", "codex"]),
            patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            selection = _prompt_targets()

        self.assertEqual(selection, ["codex"])
        self.assertIn("Invalid targets for interactive mode.", stdout.getvalue())

    def test_codex_final_prompt_retries_after_invalid_choice(self) -> None:
        with (
            patch("builtins.input", side_effect=["oops", "2"]),
            patch("pathlib.Path.exists", return_value=False),
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            maybe_handle_codex_trust(
                ["codex"],
                "default",
                Path(r"d:\source\repos\kirOpen Codex Test"),
                "prompt",
                "CODEX.md",
            )

        output = stdout.getvalue()
        self.assertIn("Unrecognized Codex setup choice. Please try again.", output)
        self.assertIn(
            "You can also trust this repo manually using the Codex CLI, Codex App",
            output,
        )

    def test_codex_final_prompt_skips_trust_menu_when_repo_already_trusted(self) -> None:
        config = (
            "[projects.'d:\\source\\repos\\kirOpen Codex Test']\n"
            'trust_level = "trusted"\n'
        )

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.read_text", return_value=config),
            patch("builtins.input", side_effect=["1"]),
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            maybe_handle_codex_trust(
                ["codex"],
                "default",
                Path(r"d:\source\repos\kirOpen Codex Test"),
                "prompt",
                "CODEX.md",
            )

        output = stdout.getvalue()
        self.assertEqual(output, "")
        self.assertNotIn("1. Auto trust", output)
        self.assertNotIn("2. Trust manually", output)

    def test_codex_only_can_use_agents_root_doc(self) -> None:
        outputs = plan_outputs_for_targets(
            ["codex"], "default", codex_root_doc="agents"
        )

        self.assertIn(Path("AGENTS.md"), outputs)
        self.assertNotIn(Path("CODEX.md"), outputs)
        self.assertNotIn(Path(".codex") / "config.toml", outputs)

    def test_agents_root_doc_is_rejected_for_mixed_targets(self) -> None:
        with self.assertRaises(SystemExit):
            resolve_codex_root_doc(["codex", "copilot"], "default", "agents")

    def test_normalizers_support_always_aliases(self) -> None:
        self.assertEqual(normalize_mode("always"), "default")
        self.assertEqual(normalize_mode("always-on"), "default")
        self.assertEqual(normalize_mode("agent-only"), "agent")

    def test_lite_mode_is_rejected_for_non_copilot_targets(self) -> None:
        with self.assertRaises(SystemExit):
            validate_mode_for_targets(["codex"], "lite")

    def test_lite_mode_is_allowed_for_mixed_targets(self) -> None:
        validate_mode_for_targets(["codex", "copilot"], "lite")

    def test_supported_modes_for_targets_uses_union_of_capabilities(self) -> None:
        self.assertEqual(supported_modes_for_targets(["codex"]), ["default", "agent"])
        self.assertEqual(
            supported_modes_for_targets(["codex", "copilot"]),
            ["default", "lite", "agent"],
        )

    def test_mode_fallback_warning_names_unsupported_harnesses(self) -> None:
        self.assertEqual(
            fallback_targets_for_mode(["codex", "copilot"], "lite"),
            ["codex"],
        )
        self.assertEqual(
            mode_fallback_warning(["codex", "copilot"], "lite"),
            "Warning: codex will fall back to always-on mode.",
        )
        self.assertIsNone(mode_fallback_warning(["copilot"], "lite"))

    def test_effective_mode_for_target_falls_back_to_default(self) -> None:
        self.assertEqual(effective_mode_for_target("codex", "lite"), "default")
        self.assertEqual(effective_mode_for_target("copilot", "lite"), "lite")

    def test_plan_outputs_falls_back_to_default_for_unsupported_targets(self) -> None:
        outputs = plan_outputs_for_targets(["codex", "copilot"], "lite")

        self.assertIn(Path("CODEX.md"), outputs)
        self.assertIn(Path(".codex") / "config.toml", outputs)
        self.assertIn(Path(".github") / "copilot-instructions.md", outputs)

    def test_interactive_args_uses_plain_prompts_without_tty(self) -> None:
        with (
            patch("sys.stdin.isatty", return_value=False),
            patch("sys.stdout.isatty", return_value=False),
            patch("assemble_instructions._prompt_targets", return_value=["copilot"]),
            patch("assemble_instructions._prompt_mode", return_value="lite"),
            patch("assemble_instructions._prompt_with_default", return_value="."),
            patch("sys.stdout", new_callable=StringIO),
        ):
            args = interactive_args()

        self.assertEqual(args.targets, ["copilot"])
        self.assertEqual(args.mode, "lite")
        self.assertEqual(args.output_dir, ".")

    def test_interactive_mode_selector_uses_up_and_down(self) -> None:
        keys = iter(["down", "enter"])

        with patch("assemble_instructions._render_mode_selector"):
            selection = _select_mode_interactively(
                ["codex", "copilot"],
                read_key=lambda: next(keys),
            )

        self.assertEqual(selection, "lite")

    def test_interactive_mode_selector_starts_on_always_on(self) -> None:
        rendered_modes: list[str] = []

        def record_render(
            targets: list[str], available_modes: list[str], selected_mode: str
        ) -> None:
            rendered_modes.append(selected_mode)

        with patch("assemble_instructions._render_mode_selector", side_effect=record_render):
            selection = _select_mode_interactively(
                ["codex", "copilot"],
                read_key=lambda: "enter",
            )

        self.assertEqual(rendered_modes[0], "default")
        self.assertEqual(selection, "default")


class PromptIdentityTests(unittest.TestCase):
    def test_non_kiro_prompts_include_explicit_kiropen_identity(self) -> None:
        expected_identity = (
            "You are KirOpen, an open, cross harness reimplementation of Amazon's Kiro AI assistant"
        )

        for vendor in ("codex", "copilot"):
            variables = get_variables(vendor)
            prompt = assemble_prompt(variables, vendor)
            self.assertIn(expected_identity, prompt)

    def test_codex_prompt_treats_spec_intent_as_explicit_spec_mode_consent(self) -> None:
        variables = get_variables("codex")
        prompt = assemble_prompt(variables, "codex")

        self.assertIn(
            "treat requests for `spec mode`, `spec session`, `spec design`, `feature spec`, `bugfix spec`, or `generate a spec` as explicit consent to invoke the `spec_mode` agent when available",
            prompt,
        )

    def test_codex_prompt_requires_wait_agent_after_spec_mode_delegation(self) -> None:
        variables = get_variables("codex")
        prompt = assemble_prompt(variables, "codex")

        self.assertIn(
            "wait for that agent's result with `wait_agent` before doing same-scope local spec work",
            prompt,
        )
        self.assertIn(
            "After delegating to `spec_mode`, call `wait_agent` for that result before continuing same-scope spec authoring locally.",
            prompt,
        )


class SpecPhaseGateTests(unittest.TestCase):
    def test_spec_skill_has_no_vendor_markers(self) -> None:
        skill_path = (
            Path(__file__).resolve().parent.parent
            / "templates"
            / "skills"
            / "spec-driven-development"
            / "SKILL.md"
        )
        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertNotRegex(skill_text, r"\{\{[A-Z_]+?\}\}")

    def test_codex_spec_agent_includes_phase_gate_steering(self) -> None:
        outputs = plan_outputs_for_targets(["codex"], "agent")
        spec_agent = outputs[Path(".codex") / "agents" / "spec_mode.toml"]

        self.assertIn("produce exactly one phase per turn by default", spec_agent)
        self.assertIn("stop and wait for the user to indicate what they want next", spec_agent)
        self.assertIn("Do not use Codex plan mode", spec_agent)
        self.assertIn(
            "treat that as explicit consent to invoke this agent",
            spec_agent,
        )
        self.assertIn(
            "owns the delegated spec scope until completion",
            spec_agent,
        )

    def test_copilot_spec_agent_includes_phase_gate_steering(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "agent")
        spec_agent = outputs[Path(".github") / "agents" / "spec-mode.agent.md"]

        self.assertIn("produce exactly one phase per turn by default", spec_agent)
        self.assertIn("stop and wait for the user to indicate what they want next", spec_agent)
        self.assertIn("Do not use Copilot's plan mode to manage spec phases", spec_agent)
        self.assertIn("If the current Copilot surface exposes a todo-capable tool such as `#todo`", spec_agent)
        self.assertIn("`Draft requirements`, `Ask user for feedback`, `Draft design`, `Draft tasks`", spec_agent)
        self.assertIn("mark completed work in both the todo list and `tasks.md`", spec_agent)


class CopilotModeOutputTests(unittest.TestCase):
    def test_copilot_default_emits_full_outputs(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "default")

        self.assertIn(Path(".github") / "copilot-instructions.md", outputs)
        self.assertFalse(
            any(path.parts[:2] == (".github", "agents") for path in outputs)
        )
        self.assertIn(
            Path(".github") / "instructions" / "api.instructions.md",
            outputs,
        )
        self.assertIn(
            Path(".agents") / "skills" / "spec-driven-development" / "SKILL.md",
            outputs,
        )
        self.assertIn(Path(".kiropen") / "copilot-user-guide.md", outputs)

    def test_copilot_default_instructions_do_not_require_generated_agents(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "default")
        prompt = outputs[Path(".github") / "copilot-instructions.md"]

        self.assertIn("do not assume a generated Copilot custom agent is available", prompt)
        self.assertNotIn("prefer delegating to the `spec-mode` agent", prompt)
        self.assertIn("Do not use Copilot's plan mode to manage spec phases", prompt)
        self.assertIn("If the current Copilot surface exposes a todo-capable tool such as `#todo`", prompt)
        self.assertIn("`Draft requirements` -> `Ask user for feedback` -> `Draft design` -> `Draft tasks`", prompt)

    def test_copilot_lite_emits_instruction_and_agents_only(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "lite")

        self.assertIn(Path(".github") / "copilot-instructions.md", outputs)
        self.assertIn(Path(".github") / "agents" / "kiropen.agent.md", outputs)
        self.assertIn(Path(".github") / "agents" / "spec-mode.agent.md", outputs)
        self.assertFalse(
            any(path.parts[:2] == (".github", "instructions") for path in outputs)
        )
        self.assertFalse(
            any(path.parts[:2] == (".agents", "skills") for path in outputs)
        )
        self.assertNotIn(Path(".kiropen") / "copilot-user-guide.md", outputs)

    def test_copilot_agent_mode_emits_agents_only(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "agent")

        self.assertIn(Path(".github") / "agents" / "kiropen.agent.md", outputs)
        self.assertIn(Path(".github") / "agents" / "spec-mode.agent.md", outputs)
        self.assertNotIn(Path(".github") / "copilot-instructions.md", outputs)
        self.assertFalse(
            any(path.parts[:2] == (".github", "instructions") for path in outputs)
        )
        self.assertFalse(
            any(path.parts[:2] == (".agents", "skills") for path in outputs)
        )
        self.assertNotIn(Path(".kiropen") / "copilot-user-guide.md", outputs)


class PortSkillMismatchGuardTests(unittest.TestCase):
    def test_codex_port_skill_includes_cross_harness_confirmation_gate(self) -> None:
        path = (
            Path(__file__).resolve().parent.parent
            / "templates"
            / "vendor-specifics"
            / "codex"
            / "skills"
            / "port-kiro-configuration-to-kiropen-on-codex.SKILL.md"
        )
        text = path.read_text(encoding="utf-8")

        self.assertIn("Cross-Harness Confirmation Gate", text)
        self.assertIn("Refuse execution once and ask for explicit confirmation.", text)
        self.assertIn(
            "target harness may have better aptitude for its own conventions",
            text,
        )

    def test_copilot_port_prompt_includes_cross_harness_confirmation_gate(self) -> None:
        path = (
            Path(__file__).resolve().parent.parent
            / "templates"
            / "vendor-specifics"
            / "copilot"
            / "skills"
            / "port-kiro-configuration-to-kiropen-on-copilot.SKILL.md"
        )
        text = path.read_text(encoding="utf-8")

        self.assertIn("Cross-Harness Confirmation Gate", text)
        self.assertIn("Refuse execution once and ask for explicit confirmation.", text)
        self.assertIn(
            "target harness may have better aptitude for its own conventions",
            text,
        )


class OmittedSkillsTests(unittest.TestCase):
    def test_ai_prompting_skill_is_not_emitted_for_codex(self) -> None:
        outputs = plan_outputs_for_targets(["codex"], "agent")
        self.assertNotIn(
            Path(".agents") / "skills" / "ai-prompting" / "SKILL.md",
            outputs,
        )

    def test_ai_prompting_skill_is_not_emitted_for_copilot(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "agent")
        self.assertNotIn(
            Path(".agents") / "skills" / "ai-prompting" / "SKILL.md",
            outputs,
        )


class RuntimeGuideDocsTests(unittest.TestCase):
    def test_codex_guide_includes_builder_version_and_required_quirks(self) -> None:
        outputs = plan_outputs_for_targets(["codex"], "agent")
        text = outputs[Path(".kiropen") / "codex-user-guide.md"]

        self.assertIn(f"Builder version: `{BUILDER_VERSION}`", text)
        self.assertIn("## Mapping Table", text)
        self.assertIn("Plan Mode Competes With Spec Mode", text)
        self.assertIn("Spec Mode Auto Progression", text)
        self.assertIn("@spec_mode", text)
        self.assertIn("Higher-Level Policy Overrides Template Behavior", text)
        self.assertNotIn("Generated File Drift", text)

    def test_copilot_target_does_not_emit_codex_runtime_guide(self) -> None:
        outputs = plan_outputs_for_targets(["copilot"], "agent")
        self.assertNotIn(Path(".kiropen") / "codex-user-guide.md", outputs)


class UnfilledMarkerTests(unittest.TestCase):
    """Every output file for every target × mode permutation must be free of
    unfilled ``{{PLACEHOLDER}}`` markers.  The regex uses a non-greedy
    quantifier so it catches each marker individually."""

    _UNFILLED_MARKER = re.compile(r"\{\{[A-Z_]+?\}\}")

    def _assert_no_markers(
        self, outputs: dict[Path, str], label: str
    ) -> None:
        for path, content in outputs.items():
            match = self._UNFILLED_MARKER.search(content)
            self.assertIsNone(
                match,
                f"[{label}] {path} contains unfilled marker: {match.group() if match else ''}",
            )

    def test_no_unfilled_markers_in_any_permutation(self) -> None:
        target_modes = {
            "codex": ["agent", "default"],
            "copilot": ["agent", "default", "lite"],
        }
        for target, modes in target_modes.items():
            for mode in modes:
                with self.subTest(target=target, mode=mode):
                    outputs = plan_outputs_for_targets(
                        [target], mode
                    )
                    self._assert_no_markers(outputs, f"{target}/{mode}")


if __name__ == "__main__":
    unittest.main()
