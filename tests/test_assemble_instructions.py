import tomllib
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from assemble_instructions import (
    assemble_prompt,
    build_codex_default_choice_prompt,
    codex_project_trust_level,
    get_variables,
    maybe_handle_codex_trust,
    normalize_codex_default_choice,
    normalize_repo_path_for_codex,
    _prompt_mode,
    _prompt_targets,
    plan_outputs_for_targets,
    resolve_codex_root_doc,
    upsert_codex_project_trust,
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
        prompt = build_codex_default_choice_prompt(
            Path(r"C:\Users\Daniel\.codex\config.toml"),
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
            selection = _prompt_mode()

        self.assertEqual(selection, "default")
        self.assertIn("Invalid mode for interactive mode.", stdout.getvalue())

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


class PromptIdentityTests(unittest.TestCase):
    def test_non_kiro_prompts_include_explicit_kiropen_identity(self) -> None:
        expected_identity = (
            "I'm KirOpen, an open reimplementation of Amazon's Kiro AI harness."
        )

        for vendor in ("codex", "copilot"):
            variables = get_variables(vendor, platform_override="win32")
            prompt = assemble_prompt(variables, vendor)
            self.assertIn(expected_identity, prompt)


class SpecPhaseGateInfixTests(unittest.TestCase):
    def test_spec_skill_contains_required_infix_markers(self) -> None:
        skill_path = (
            Path(__file__).resolve().parent.parent
            / "templates"
            / "skills"
            / "spec-driven-development"
            / "SKILL.md"
        )
        skill_text = skill_path.read_text(encoding="utf-8")

        markers = [
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WHEN_TO_USE -->",
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_1 -->",
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_2 -->",
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_PHASE_3 -->",
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WORKFLOW -->",
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_LIGHTWEIGHT -->",
        ]
        for marker in markers:
            self.assertIn(marker, skill_text)

    def test_codex_spec_agent_includes_injected_phase_gates(self) -> None:
        outputs = plan_outputs_for_targets(["codex"], "agent")
        spec_agent = outputs[Path(".codex") / "agents" / "kiropen_spec.toml"]

        self.assertIn("produce exactly one phase per turn by default", spec_agent)
        self.assertIn("approve requirements", spec_agent)
        self.assertIn("design then auto tasks", spec_agent)
        self.assertIn("generate all phases now", spec_agent)
        self.assertIn(
            "Do not treat planning behavior, plan UIs, or task-plan tools as user approval",
            spec_agent,
        )
        self.assertNotIn(
            "<!-- KIROOPEN-INFIX:SPEC_PHASE_GATES_WHEN_TO_USE -->",
            spec_agent,
        )


if __name__ == "__main__":
    unittest.main()
