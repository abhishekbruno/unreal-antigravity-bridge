#!/usr/bin/env python3
"""Install Unreal Engine for Antigravity plugin, project settings, and MCP configuration.

Requires Python >=3.9 and only the standard library. Does not install Unreal Engine or third-party packages.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import sys

BUNDLE = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "unreal-antigravity-bridge"
BUNDLE_FILES = ("plugin.json", "mcp_config.json", "hooks.json", "LICENSE")
SKILL_NAMES = ("unreal-mcp", "create-toolset", "unreal-skill", "unreal-game", "unreal-playtest")
START_MARKER = "<!-- unreal-antigravity-start -->"
END_MARKER = "<!-- unreal-antigravity-end -->"


def write_text_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def enable_project_plugins(uproject: Path) -> bool:
    """Enable ModelContextProtocol and AllToolsets in the target .uproject file with backup."""
    with uproject.open(encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Project .uproject must contain a JSON object")
    plugins = data.setdefault("Plugins", [])
    if not isinstance(plugins, list):
        raise ValueError("Expected a Plugins JSON array in .uproject")

    changed = False
    for name in ("ModelContextProtocol", "AllToolsets"):
        existing = next((p for p in plugins if isinstance(p, dict) and p.get("Name") == name), None)
        if existing is None:
            plugins.append({"Name": name, "Enabled": True})
            changed = True
        elif existing.get("Enabled") is not True:
            existing["Enabled"] = True
            changed = True

    if changed:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = uproject.with_name(uproject.name + f".backup-{stamp}")
        shutil.copy2(uproject, backup)
        uproject.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  Enabled Unreal MCP and AllToolsets; backup: {backup}")
    return changed


def enable_autostart(project_dir: Path, port: int) -> None:
    """Configure Unreal MCP server auto-start in EditorPerProjectUserSettings.ini."""
    ini = project_dir / "Saved" / "Config" / "WindowsEditor" / "EditorPerProjectUserSettings.ini"
    header = "[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]"
    existing = ini.read_text(encoding="utf-8-sig") if ini.exists() else ""
    lines = existing.splitlines(keepends=True)
    target_index = next((i for i, line in enumerate(lines) if line.strip() == header), None)

    if target_index is None:
        if existing and not existing.endswith(("\n", "\r")):
            existing += "\n"
        existing += f"\n{header}\nbAutoStartServer=True\nServerPortNumber={port}\nServerUrlPath=/mcp\n"
        write_text_if_changed(ini, existing)
        return

    end = next((j for j in range(target_index + 1, len(lines)) if lines[j].strip().startswith("[")), len(lines))
    group = "".join(lines[target_index + 1:end])
    for key, value in (("bAutoStartServer", "True"), ("ServerPortNumber", str(port)), ("ServerUrlPath", "/mcp")):
        pattern = re.compile(rf"(?m)^\s*{re.escape(key)}\s*=\s*[^\r\n]*$")
        replacement = f"{key}={value}"
        if pattern.search(group):
            group = pattern.sub(replacement, group, count=1)
        else:
            if group and not group.endswith("\n"):
                group += "\n"
            group += replacement + "\n"
    write_text_if_changed(ini, "".join(lines[:target_index + 1]) + group + "".join(lines[end:]))


def install_plugin_files(target_dir: Path, port: int = 8000) -> Path:
    """Install plugin manifest, mcp_config.json, hooks.json, rules, and skills into target directory."""
    dst = target_dir / ".agents" / "plugins" / PLUGIN_NAME
    dst.mkdir(parents=True, exist_ok=True)

    for name in BUNDLE_FILES:
        src_file = BUNDLE / name
        if src_file.is_file():
            payload = src_file.read_text(encoding="utf-8")
            if name == "mcp_config.json":
                data = json.loads(payload)
                data.setdefault("mcpServers", {}).setdefault("unreal-mcp", {})["url"] = f"http://127.0.0.1:{port}/mcp"
                payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
            write_text_if_changed(dst / name, payload)

    # Copy rules/
    rules_src = BUNDLE / "rules"
    if rules_src.is_dir():
        shutil.copytree(rules_src, dst / "rules", dirs_exist_ok=True)

    # Copy skills/
    for skill in SKILL_NAMES:
        src = BUNDLE / "skills" / skill
        if src.is_dir():
            dest = dst / "skills" / skill
            shutil.copytree(src, dest, dirs_exist_ok=True)

    # Copy core/ and scripts/ for hook execution
    for mod in ("core", "adapters"):
        src = BUNDLE / mod
        if src.is_dir():
            dest = dst / mod
            shutil.copytree(src, dest, dirs_exist_ok=True)

    return dst


def merge_mcp_config(project_dir: Path, port: int = 8000) -> None:
    """Write or update project root mcp_config.json for Antigravity."""
    mcp_path = project_dir / "mcp_config.json"
    if mcp_path.exists():
        try:
            data = json.loads(mcp_path.read_text(encoding="utf-8-sig"))
        except Exception:
            data = {}
    else:
        data = {}

    servers = data.setdefault("mcpServers", {})
    servers["unreal-mcp"] = {
        "url": f"http://127.0.0.1:{port}/mcp"
    }
    write_text_if_changed(mcp_path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def merge_agent_guidance(project_dir: Path) -> None:
    """Install Antigravity rules into project rules/AGENTS.md."""
    rules_dir = project_dir / "rules"
    rules_file = rules_dir / "AGENTS.md"
    src_rules = BUNDLE / "rules" / "AGENTS.md"
    if src_rules.is_file():
        content = src_rules.read_text(encoding="utf-8")
        write_text_if_changed(rules_file, content)


# Backwards compatibility shims
def merge_marketplace(project_dir: Path) -> str:
    """Compatibility shim for legacy installer tests."""
    return "unreal-local"


def merge_codex_config(project_dir: Path, port: int, marketplace: str) -> None:
    """Compatibility shim: directs configuration to project mcp_config.json."""
    merge_mcp_config(project_dir, port)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Path to .uproject file")
    parser.add_argument("--port", type=int, default=8000, help="Unreal MCP listening port (default: 8000)")
    parser.add_argument("--no-autostart", action="store_true", help="Do not configure Unreal MCP auto-start")
    parser.add_argument("--global", dest="is_global", action="store_true", help="Install into global Antigravity plugins directory (~/.gemini/config/plugins)")

    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("--port must be between 1024 and 65535")

    uproject = Path(args.project).expanduser().resolve()
    if not uproject.is_file() or uproject.suffix.lower() != ".uproject":
        parser.error("--project must point to an existing .uproject file")

    if not (BUNDLE / "plugin.json").exists():
        parser.error("Run installer from within the unreal-antigravity-bridge repository root")

    project_dir = uproject.parent
    print(f"Installing Unreal Engine for Antigravity for: {uproject}")

    try:
        enable_project_plugins(uproject)
        if not args.no_autostart:
            enable_autostart(project_dir, args.port)

        target_root = (Path.home() / ".gemini" / "config") if args.is_global else project_dir
        installed_path = install_plugin_files(target_root, args.port)
        merge_mcp_config(project_dir, args.port)
        merge_agent_guidance(project_dir)

        print(f"Installed native Antigravity plugin to: {installed_path}")
        print(f"Project MCP configuration written to: {project_dir / 'mcp_config.json'}")
        print(f"Project rules written to: {project_dir / 'rules' / 'AGENTS.md'}")
        print("\nNext steps:")
        print("1. Launch or restart Unreal Editor with your project.")
        print(f"2. Verify MCP server starts on http://127.0.0.1:{args.port}/mcp.")
        print(f"3. Run diagnostic check: python scripts/doctor.py --project {uproject} --engine <engine-path>")
        print("4. In Antigravity, activate the 'unreal-mcp' skill and begin authoring.")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
