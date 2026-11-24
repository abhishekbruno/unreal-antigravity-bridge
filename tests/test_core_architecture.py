"""Unit tests for the client-independent Unreal Engineering Core architecture.

Verifies:
1. Pure Python standard library imports (no runtime dependency on external AI client libraries).
2. Clean separation between core and client integration layers.
3. Project root detection and session context generation in core.context.
4. MCPClient instantiation with custom client identity.
"""

import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))

import core
from core.context import find_project_root, inspect_project_context, format_context_prompt, is_project_root
from core.transport import Client, MCPClient, MCPError, validate_endpoint
from core.session import UnrealSession, parse_toolsets, validate_inputs


class CoreArchitectureTests(unittest.TestCase):
    def test_core_package_exports(self):
        self.assertIsNotNone(core.__version__)
        self.assertIs(core.Client, Client)
        self.assertIs(core.MCPClient, MCPClient)
        self.assertIs(core.UnrealSession, UnrealSession)
        self.assertIs(core.inspect_project_context, inspect_project_context)

    def test_core_modules_do_not_import_client_libraries(self):
        """Verify that core modules have zero imports of Codex, Claude, OpenAI, or Anthropic packages."""
        core_dir = PACKAGE_ROOT / "core"
        forbidden = {"codex", "claude", "openai", "anthropic"}

        for py_path in core_dir.rglob("*.py"):
            with open(py_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(py_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".")[0].lower()
                        self.assertNotIn(top, forbidden, f"{py_path.name} imports forbidden client library {top}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    top = node.module.split(".")[0].lower()
                    self.assertNotIn(top, forbidden, f"{py_path.name} imports from forbidden client library {top}")

    def test_transport_client_name_customization(self):
        client = MCPClient("http://127.0.0.1:8000/mcp", client_name="unreal-antigravity-bridge", client_version="1.0.0")
        self.assertEqual(client.client_name, "unreal-antigravity-bridge")
        self.assertEqual(client.client_version, "1.0.0")

    def test_context_detection_with_uproject(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            game_dir = temp_path / "MyProject"
            game_dir.mkdir()
            uproject = game_dir / "MyProject.uproject"
            uproject.write_text('{"FileVersion": 3}')

            # Subdirectory
            content_dir = game_dir / "Content" / "Maps"
            content_dir.mkdir(parents=True)

            detected_root = find_project_root(content_dir)
            self.assertEqual(detected_root, game_dir)

            context = inspect_project_context(content_dir)
            self.assertTrue(context["found"])
            self.assertEqual(context["project_type"], "game")
            self.assertEqual(context["uproject_name"], "MyProject.uproject")
            self.assertFalse(context["mcp_config_present"])

            prompt = format_context_prompt(context)
            self.assertIn("The project is `MyProject.uproject`", prompt)
            self.assertIn("unreal-mcp", prompt)

    def test_context_detection_with_engine_marker(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            engine_dir = temp_path / "UnrealEngine"
            engine_dir.mkdir()
            (engine_dir / "GenerateProjectFiles.bat").write_text("@echo off")
            (engine_dir / "Engine").mkdir()

            context = inspect_project_context(engine_dir)
            self.assertTrue(context["found"])
            self.assertEqual(context["project_type"], "engine")

            prompt = format_context_prompt(context)
            self.assertIn("It is an Engine source tree.", prompt)

    def test_context_detection_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            context = inspect_project_context(temp_path)
            self.assertFalse(context["found"])
            prompt = format_context_prompt(context)
            self.assertEqual(prompt, "")


if __name__ == "__main__":
    unittest.main()
