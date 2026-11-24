"""Unit tests for native Google Antigravity plugin manifest, MCP config, hooks, and skill packaging."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PluginPackagingTests(unittest.TestCase):
    def test_native_plugin_json_schema(self):
        manifest_path = ROOT / "plugin.json"
        self.assertTrue(manifest_path.is_file(), f"Missing plugin.json at {manifest_path}")

        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "unreal-antigravity-bridge")
        self.assertEqual(data.get("displayName"), "Unreal Engine for Antigravity")
        self.assertEqual(data.get("version"), "0.1.0-alpha.2")
        self.assertIn("description", data)
        self.assertEqual(data.get("license"), "MIT")
        self.assertEqual(data.get("repository"), "https://github.com/abhishekbruno/unreal-antigravity-bridge")
        self.assertEqual(data.get("logo"), "assets/logo.svg")
        self.assertTrue((ROOT / data["logo"]).is_file(), "Referenced logo file does not exist")

        prompts = data.get("suggestedPrompts", [])
        self.assertIsInstance(prompts, list)
        self.assertEqual(len(prompts), 3, "Expected exactly 3 suggestedPrompts")

    def test_mcp_config_json_schema(self):
        mcp_path = ROOT / "mcp_config.json"
        self.assertTrue(mcp_path.is_file(), f"Missing mcp_config.json at {mcp_path}")

        data = json.loads(mcp_path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers", {})
        self.assertIn("unreal-mcp", servers)

        unreal_cfg = servers["unreal-mcp"]
        url = unreal_cfg.get("url", "")
        self.assertTrue(url.startswith("http://127.0.0.1:"), f"URL {url} must bind to loopback")
        self.assertTrue(url.endswith("/mcp"), f"URL {url} must route to /mcp")

    def test_hooks_json_schema(self):
        hooks_path = ROOT / "hooks.json"
        self.assertTrue(hooks_path.is_file(), f"Missing hooks.json at {hooks_path}")

        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        self.assertIn("unreal-session-context", data)
        session_hook = data["unreal-session-context"]
        self.assertIn("SessionStart", session_hook)
        handlers = session_hook["SessionStart"]
        self.assertIsInstance(handlers, list)
        self.assertTrue(len(handlers) >= 1)

        handler = handlers[0]
        self.assertEqual(handler.get("type"), "command")
        self.assertIn("core/context.py --hook", handler.get("command", ""))
        self.assertTrue(handler.get("timeout", 0) > 0)

    def test_rules_agents_md_present(self):
        rules_path = ROOT / "rules/AGENTS.md"
        self.assertTrue(rules_path.is_file(), f"Missing rules/AGENTS.md at {rules_path}")
        text = rules_path.read_text(encoding="utf-8")
        self.assertIn("Unreal Engine Development Rules for Google Antigravity", text)

    def test_absence_of_legacy_artifacts(self):
        legacy_paths = [
            ROOT / ".codex-plugin",
            ROOT / ".agents/plugins/marketplace.json",
            ROOT / "AGENTS.unreal-codex.md",
            ROOT / ".mcp.json",
            ROOT / "mcp.json",
        ]
        for p in legacy_paths:
            self.assertFalse(p.exists(), f"Legacy client artifact must not exist: {p}")

    def test_all_skills_have_valid_frontmatter(self):
        skills_dir = ROOT / "skills"
        self.assertTrue(skills_dir.is_dir())

        skill_files = list(skills_dir.glob("*/SKILL.md"))
        self.assertTrue(len(skill_files) >= 5, f"Expected at least 5 skills, found {len(skill_files)}")

        skill_names = set()
        for sf in skill_files:
            text = sf.read_text(encoding="utf-8")
            match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
            self.assertIsNotNone(match, f"Skill {sf} missing YAML frontmatter")

            frontmatter = match.group(1)
            name_m = re.search(r"^name:\s*([a-zA-Z0-9_\-]+)", frontmatter, re.M)
            desc_m = re.search(r"^description:\s*(.+)", frontmatter, re.M)

            self.assertIsNotNone(name_m, f"Skill {sf} missing name")
            self.assertIsNotNone(desc_m, f"Skill {sf} missing description")

            name = name_m.group(1)
            self.assertNotIn(name, skill_names, f"Duplicate skill name: {name}")
            skill_names.add(name)

        expected_skills = {"unreal-mcp", "create-toolset", "unreal-skill", "unreal-game", "unreal-playtest"}
        self.assertTrue(expected_skills.issubset(skill_names), f"Missing skills: {expected_skills - skill_names}")

    def test_antigravity_cli_validate_passes_strict(self):
        agy_bin = shutil.which("agy.cmd") or shutil.which("agy.exe") or shutil.which("agy")
        if not agy_bin:
            gemini_bin = Path.home() / ".gemini/bin/agy.exe"
            if gemini_bin.is_file():
                agy_bin = str(gemini_bin)

        if not agy_bin:
            self.skipTest("Antigravity CLI (agy) not available on this host")

        res = subprocess.run(
            [agy_bin, "plugin", "validate", ".", "--strict", "--json"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(res.returncode, 0, f"agy plugin validate failed:\n{res.stdout}\n{res.stderr}")
        data = json.loads(res.stdout)
        self.assertEqual(data.get("name"), "unreal-antigravity-bridge")
        components = data.get("components", {})
        self.assertEqual(components.get("skills"), 5)
        self.assertEqual(components.get("hooks"), 1)
        self.assertEqual(components.get("mcpServers"), 1)
        self.assertEqual(components.get("rules"), 1)


if __name__ == "__main__":
    unittest.main()
