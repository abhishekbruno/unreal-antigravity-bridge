---
name: unreal-mcp
description: "Use this skill to inspect and modify a live Unreal Engine project via Epic Games' native Model Context Protocol (MCP) server. Trigger when the user wants to inspect, query, or execute operations inside an active Unreal Engine project. Concrete triggers: spawn/move/duplicate/transform actors in a level, open or query a .uproject, inspect scene outliner, add gameplay actors around PlayerStart, create or edit Blueprints/Widgets/Materials/Niagara/Control Rig/Sequencer/State Trees/GAS abilities, read or write actor properties, trigger Live Coding recompilation, or inspect project assets. Treat as Unreal context even without the explicit word 'Unreal' when asset prefixes (BP_, WBP_, M_, MI_, NS_, CR_, SK_, SM_, ABP_), Unreal reflection macros (UPROPERTY, UFUNCTION, AActor, UObject), or .uproject files are present. Skip for: pure conceptual questions unrelated to live project manipulation, non-Unreal game engines, or unrelated uses of 'blueprint'."
---

# Unreal Engine MCP for Google Antigravity

You are connected to a running Unreal Engine Editor session through the native `ModelContextProtocol` server (endpoint `http://127.0.0.1:8000/mcp` or via `unreal_mcp_proxy`). The engine exposes hundreds of tools across 30+ toolsets (actors, blueprints, materials, Niagara, Sequencer, Control Rigs, GAS, automation tests, Live Coding, and more) registered through Unreal's native `ToolsetRegistry`.

Use this connection to inspect and programmatically mutate live editor state rather than directing the user to perform manual GUI steps.

---

## 1. Toolset Discovery & Execution Contract

In Unreal Engine 5.8+, **Tool Search is enabled by default**. The MCP server advertises only three primary meta-tools for the session:
1. `list_toolsets`: Lists all registered toolsets (e.g. `ActorTools`, `BlueprintTools`, `LevelTools`, `AssetTools`, `StaticMeshTools`, `LogsToolset`).
2. `describe_toolset`: Returns the complete JSON input schema for all tools inside a specific toolset.
3. `call_tool`: Dispatches a tool invocation server-side.

Individual tool methods (such as `ActorTools.spawn_actor` or `BlueprintTools.get_graph_dsl_docs`) are **not in the global `tools/list`**. They are dispatched dynamically through `call_tool`. This keeps your context window compact and prompt caching efficient.

### Standard Step-by-Step Execution Workflow:

1. **Verify Session Reality:**
   - Confirm the MCP connection is live. If disconnected, follow `references/setup.md`.
   - Never fabricate or guess tool names or parameter schemas.
2. **Discover Toolset & Tools:**
   - Call `list_toolsets` to inspect what toolsets are registered in the active editor.
   - Call `describe_toolset` passing `toolset_name` (e.g. `editor_toolset.toolsets.actor.ActorTools` or `ActorTools`) to retrieve exact parameter schemas and return types.
3. **Dispatch Tool:**
   - Invoke `call_tool` with:
     - `toolset_name`: The target toolset name.
     - `tool_name`: The method name.
     - `arguments`: The parameter dictionary conforming exactly to the discovered JSON schema.
4. **Inspect Result:**
   - Always verify the returned `structuredContent` or `content`. Many Unreal tools return a status dictionary indicating success or failure without raising protocol-level exceptions.

---

## 2. Operational Safety Guards

Follow these strict rules to protect live editor and project state:

- **Two-Factor Project Verification:** Before issuing scene mutations, verify that the active editor process belongs to the designated project (`.uproject`) and engine build. In multi-editor setups, inspect process IDs or log entries to confirm port ownership.
- **Save Early and Often:** Call `AssetTools.save_asset` or instruct the editor to save modified packages. MCP mutations alter live in-memory `UObject` state; uncaught crashes or uncompiled Blueprints will lose unsaved changes.
- **Compilation Synchronization:** Do not issue mutations while C++ compilation or shader generation is active. When rebuilding C++, call `LiveCodingToolset.CompileLiveCoding` and await its completion.
- **Play-In-Editor (PIE) State:** Editor asset mutation tools behave differently or fail when PIE is running. Verify PIE is inactive before attempting asset creation or graph modifications.
- **Safe Test Map Isolation:** When executing automated verification workflows, duplicate clean template levels (e.g., `/Engine/Maps/Templates/Template_Default`) into isolated test levels (e.g., `/Game/AntigravityBridgeTests/...`). Never overwrite user production levels.
- **Ordered Execution:** Tool calls execute synchronously on the Unreal Editor main game thread. Do not attempt concurrent conflicting mutations against the same asset or actor hierarchy.

---

## 3. Project Agent Skills

Unreal Engine projects can register in-editor **Agent Skills** via `AgentSkillToolset`:
- Call `AgentSkillToolset.ListSkills` via `call_tool` to view project-specific instructions and domain conventions.
- Call `AgentSkillToolset.GetSkills` on matching skills to read specialized project instructions.

---

## 4. Reference Documentation

- [`references/setup.md`](references/setup.md): Initial MCP server setup, INI configuration, auto-start, and optional proxy installation.
- [`references/operations.md`](references/operations.md): Editor console commands, settings, proxy recovery, and diagnostic troubleshooting.
- **Companion Skills:**
  - `create-toolset`: Guide for authoring C++ native toolsets in Unreal plugins.
  - `unreal-skill`: Guide for authoring project-level Agent Skills.
  - `unreal-game`: Full-cycle game level and actor authoring workflow.
  - `unreal-playtest`: Automated PIE execution and log error harvesting.
