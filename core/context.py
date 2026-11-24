"""Cross-platform Unreal Engine project discovery and session context provider.

Replaces legacy shell-based context hooks with a pure Python standard library
implementation compatible with Windows, macOS, and Linux.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Dict, Optional


def is_project_root(directory: Path) -> bool:
    """Check if a directory contains definitive Unreal Engine project markers.

    Note: A bare 'Engine' directory is not sufficient because engine source submodules
    contain 'Source/Runtime/Engine'. We check for root marker files.
    """
    if not directory.is_dir():
        return False

    markers = (
        "GenerateProjectFiles.bat",
        "GenerateProjectFiles.sh",
        "GenerateProjectFiles.command",
    )
    for marker in markers:
        if (directory / marker).is_file():
            return True

    # Check for any .uproject in this directory
    try:
        for item in directory.glob("*.uproject"):
            if item.is_file():
                return True
    except (OSError, PermissionError):
        pass

    return False


def find_project_root(start_path: Optional[Path | str] = None) -> Optional[Path]:
    """Walk upward from start_path to discover the enclosing Unreal project or engine root."""
    current = Path(start_path or Path.cwd()).resolve()

    while True:
        if is_project_root(current):
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def inspect_project_context(start_path: Optional[Path | str] = None) -> Dict[str, Any]:
    """Inspect environment and return structured context metadata about the active Unreal project."""
    root = find_project_root(start_path)
    if not root:
        return {
            "found": False,
            "root": None,
            "project_type": None,
            "uproject_path": None,
            "uproject_name": None,
            "mcp_config_present": False,
        }

    is_engine = (root / "Engine").is_dir()
    project_type = "engine" if is_engine else "game"

    uproject_file = None
    try:
        candidates = list(root.glob("*.uproject"))
        if candidates:
            uproject_file = candidates[0]
    except (OSError, PermissionError):
        pass

    mcp_config = (root / "mcp_config.json").is_file() or (root / ".mcp.json").is_file()

    return {
        "found": True,
        "root": str(root),
        "project_type": project_type,
        "uproject_path": str(uproject_file) if uproject_file else None,
        "uproject_name": uproject_file.name if uproject_file else None,
        "mcp_config_present": mcp_config,
    }


def format_context_prompt(context: Dict[str, Any]) -> str:
    """Format structured project context into a clear system prompt addition."""
    if not context.get("found"):
        return ""

    parts = ["This working directory is an Unreal Engine project."]
    if context.get("project_type") == "engine":
        parts.append("It is an Engine source tree.")
    elif context.get("uproject_name"):
        parts.append(f"The project is `{context['uproject_name']}`.")

    parts.append("Prefer Unreal Engine conventions (C++/UObject patterns, Slate, UHT reflection) when suggesting code.")
    parts.append("Use the `unreal-mcp` skill for tasks that involve inspecting or driving the Unreal Editor via MCP.")

    if context.get("mcp_config_present"):
        parts.append("MCP configuration is present in the project.")
    else:
        parts.append("No MCP configuration is present at the project root yet. Configure it using `python scripts/configure.py`.")

    return " ".join(parts)


def execute_hook() -> int:
    """Handle Antigravity SessionStart hook contract via stdin/stdout."""
    payload: Dict[str, Any] = {}
    if not sys.stdin.isatty():
        try:
            content = sys.stdin.read()
            if content.strip():
                payload = json.loads(content)
        except Exception:
            pass

    search_paths = []
    for p in payload.get("workspacePaths", []):
        search_paths.append(Path(p))
    if payload.get("cwd"):
        search_paths.append(Path(payload["cwd"]))
    if not search_paths:
        search_paths.append(Path.cwd())

    found_context = None
    for candidate in search_paths:
        ctx = inspect_project_context(candidate)
        if ctx.get("found"):
            found_context = ctx
            break

    if found_context and found_context.get("found"):
        note = format_context_prompt(found_context)
        output = {
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": note
                    }
                }
            ]
        }
    else:
        output = {"injectSteps": []}

    print(json.dumps(output))
    return 0


def main() -> int:
    """CLI entrypoint for hooks and subprocesses."""
    if "--hook" in sys.argv:
        return execute_hook()

    context = inspect_project_context()
    if not context["found"]:
        return 0

    if "--json" in sys.argv:
        print(json.dumps(context, indent=2))
    else:
        note = format_context_prompt(context)
        print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
