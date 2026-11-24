import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("unreal_antigravity_installer", PACKAGE_ROOT / "scripts" / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.project = self.root / "MyGame.uproject"
        self.project.write_text(
            json.dumps({"FileVersion": 3, "Plugins": [{"Name": "MyPlugin", "Enabled": True}]}),
            encoding="utf-8",
        )

    def install(self, port=8000):
        installer.enable_project_plugins(self.project)
        installer.enable_autostart(self.root, port)
        installer.install_plugin_files(self.root, port)
        installer.merge_mcp_config(self.root, port)
        installer.merge_agent_guidance(self.root)

    def test_project_plugins_backup_and_idempotence(self):
        self.install()
        source = json.loads(self.project.read_text(encoding="utf-8"))
        enabled = {p["Name"] for p in source["Plugins"] if p.get("Enabled")}
        self.assertTrue({"ModelContextProtocol", "AllToolsets", "MyPlugin"} <= enabled)

        # Check backup created
        backups = list(self.root.glob("MyGame.uproject.backup-*"))
        self.assertEqual(len(backups), 1)

        # Re-run install; verify idempotence and no duplicate backup
        self.install()
        self.assertEqual(len(list(self.root.glob("MyGame.uproject.backup-*"))), 1)

        # Check project MCP config
        project_mcp = json.loads((self.root / "mcp_config.json").read_text())
        self.assertIn("unreal-mcp", project_mcp["mcpServers"])
        self.assertEqual(project_mcp["mcpServers"]["unreal-mcp"]["url"], "http://127.0.0.1:8000/mcp")

        # Check installed plugin bundle
        plugin_dir = self.root / ".agents" / "plugins" / "unreal-antigravity-bridge"
        self.assertTrue((plugin_dir / "plugin.json").is_file())
        self.assertTrue((plugin_dir / "mcp_config.json").is_file())
        self.assertTrue((plugin_dir / "hooks.json").is_file())
        self.assertTrue((plugin_dir / "rules" / "AGENTS.md").is_file())
        self.assertTrue((plugin_dir / "skills" / "unreal-mcp" / "SKILL.md").is_file())

        installed_mcp = json.loads((plugin_dir / "mcp_config.json").read_text())
        self.assertEqual(installed_mcp["mcpServers"]["unreal-mcp"]["url"], "http://127.0.0.1:8000/mcp")

    def test_custom_port_configuration(self):
        self.install(port=8500)
        project_mcp = json.loads((self.root / "mcp_config.json").read_text())
        self.assertEqual(project_mcp["mcpServers"]["unreal-mcp"]["url"], "http://127.0.0.1:8500/mcp")

        plugin_dir = self.root / ".agents" / "plugins" / "unreal-antigravity-bridge"
        installed_mcp = json.loads((plugin_dir / "mcp_config.json").read_text())
        self.assertEqual(installed_mcp["mcpServers"]["unreal-mcp"]["url"], "http://127.0.0.1:8500/mcp")

    def test_autostart_updates_existing_section(self):
        ini = self.root / "Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini"
        ini.parent.mkdir(parents=True)
        ini.write_text(
            "[Other]\nFoo=Bar\n[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]\nbAutoStartServer=False\nServerPortNumber=9900\n[After]\nBaz=Qux\n"
        )
        installer.enable_autostart(self.root, 8000)
        content = ini.read_text()
        self.assertIn("[Other]\nFoo=Bar", content)
        self.assertIn("[After]\nBaz=Qux", content)
        self.assertIn("bAutoStartServer=True", content)
        self.assertIn("ServerPortNumber=8000", content)
        installer.enable_autostart(self.root, 8000)
        self.assertEqual(ini.read_text(), content)

    def test_mcp_skill_frontmatter(self):
        skill = (PACKAGE_ROOT / "skills/unreal-mcp/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: unreal-mcp\n"))


if __name__ == "__main__":
    unittest.main()
