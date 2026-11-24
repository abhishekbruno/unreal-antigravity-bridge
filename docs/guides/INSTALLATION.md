# Installation Guide: Unreal Engine for Antigravity

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Target Environment:** Windows 10/11 & macOS (Apple Silicon & Intel)  
**Supported AI Client:** Google Antigravity (IDE / CLI)  
**Target Engine:** Unreal Engine 5.8+  

---

## 1. Prerequisites

Before installing the plugin:
1. **Unreal Engine 5.8+** installed on your workstation.
2. **Python 3.10+** (tested on 3.10, 3.11, and 3.12; standard library only).
3. **Google Antigravity** installed (`agy` CLI executable available or Antigravity IDE running).

---

## 2. Plugin Installation Options

Antigravity supports discovering plugins at the user configuration level (global) or at the project level (workspace local).

### Option A: Project-Level Installation (Recommended for Teams)

Install the plugin directly inside your Unreal project workspace:

```bash
# From within the unreal-antigravity-bridge repository:
python scripts/install.py --project "/path/to/MyGame/MyGame.uproject"
```

This automated installer:
1. Validates the `.uproject` file and creates a timestamped backup (`MyGame.uproject.backup-*`).
2. Enables `ModelContextProtocol` and `AllToolsets` in `.uproject`.
3. Configures auto-start on loopback (`http://127.0.0.1:8000/mcp`) in `EditorPerProjectUserSettings.ini`.
4. Copies the native plugin bundle (`plugin.json`, `mcp_config.json`, `hooks.json`, `rules/`, `skills/`) into `<ProjectRoot>/.agents/plugins/unreal-antigravity-bridge`.
5. Writes the project MCP configuration file `mcp_config.json`.
6. Installs Antigravity development rules into `rules/AGENTS.md`.

### Option B: Global User Profile Installation

To make the plugin available across all your workspaces in Antigravity:

```bash
python scripts/install.py --project "/path/to/MyGame/MyGame.uproject" --global
```

This installs the plugin bundle into:
- Windows: `C:\Users\<Username>\.gemini\config\plugins\unreal-antigravity-bridge`
- macOS / Linux: `~/.gemini/config/plugins/unreal-antigravity-bridge`

And enables project-level plugins and auto-start in the specified `.uproject`.

---

## 3. Verifying Installation

### 1. Antigravity Plugin Conformance
Validate the installed plugin using the Antigravity CLI:

```bash
agy plugin validate . --strict --json
```

Expected output:
```json
{
  "dir": ".",
  "manifest": "plugin.json",
  "name": "unreal-antigravity-bridge",
  "agentPluginsSpec": false,
  "components": {
    "agents": 0,
    "hooks": 1,
    "mcpServers": 1,
    "rules": 1,
    "sidecars": 0,
    "skills": 5
  }
}
```

### 2. Preflight Diagnostics
Run the diagnostic suite:

```bash
python scripts/doctor.py --project "/path/to/MyGame/MyGame.uproject" --engine "/path/to/UE_5.8"
```

Verify that all checks report `PASS` or `BLOCKED` (expected if Unreal Editor is not yet launched).

---

## 4. Uninstalling or Reverting

To cleanly revert project integration settings:

```bash
python scripts/editor_lifecycle.py uninstall --project "/path/to/MyGame/MyGame.uproject"
```

This removes MCP server registrations and restores backed-up configurations.
