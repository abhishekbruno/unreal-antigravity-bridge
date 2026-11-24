# Skill Usage Guide: Unreal Engine for Antigravity

This guide describes how Google Antigravity discovers and utilizes the five bundled developer skills.

---

## 1. Skill Catalog Overview

| Skill Name | Purpose | Trigger Conditions |
| :--- | :--- | :--- |
| **`unreal-mcp`** | Live editor inspection and asset mutation via native Unreal MCP | Interacting with running Unreal Editor, inspecting scene outliner, actor transforms, Live Coding |
| **`create-toolset`** | Authoring or extending C++ or Python editor toolsets | Adding `@toolset_registry.tool_call` functions, creating new toolset classes |
| **`unreal-skill`** | Authoring in-editor Agent Skills (`UAgentSkill`) | Creating reusable instructions registered with Unreal's `AgentSkillToolset` |
| **`unreal-game`** | End-to-end natural language game authoring workflow | "Create a playable scene", "Build a game loop", placing actors and PlayerStart |
| **`unreal-playtest`** | Automated Play-In-Editor (PIE) testing and log analysis | Testing game levels in editor, asserting gameplay variables, checking script errors |

---

## 2. Using `unreal-mcp`

The core bridge skill for inspecting and driving a running Unreal Editor instance.

### Execution Workflow:
1. **List registered toolsets:** Call meta-tool `list_toolsets` via MCP.
2. **Describe schemas:** Call meta-tool `describe_toolset` passing the toolset name (e.g. `ActorTools`).
3. **Dispatch tool:** Call meta-tool `call_tool` with `toolset_name`, `tool_name`, and validated arguments.
4. **Save touched packages:** Always invoke `AssetTools.save_asset` after completing edits.

---

## 3. Using `unreal-game`

Guides Antigravity through complete game development loops:
1. **Verify Connection:** Confirm editor is listening and matches the project.
2. **Retrieve Context:** Consult SQLite digest (`data/project_index.sqlite`).
3. **Author Content:** Confine all created assets to `/Game/` (never `/Engine/`).
4. **Verify Playability:** Spawn player pawn at `PlayerStart`, verify input bindings, and trigger Play-In-Editor verification.

---

## 4. Using `unreal-playtest`

Automates Play-In-Editor (PIE) test sessions:
```bash
python scripts/playtest.py run --project "/path/to/MyGame.uproject" --duration 10
```
- Starts PIE session.
- Monitors `Saved/Logs/<GameName>.log` for script runtime errors or assertion failures.
- Captures gameplay variables (e.g. player health, collected coins).
- Terminates PIE cleanly and generates a verification report.

---

## 5. Using `create-toolset` and `unreal-skill`

- **`create-toolset`:** Use when extending Unreal Engine's C++ or Python toolsets exposed to AI agents. Enforces CRUD symmetry, static method conventions, and parameter type annotations.
- **`unreal-skill`:** Use when authoring project-specific `UAgentSkill` assets in the Content Browser or Python skill classes in engine plugins.
