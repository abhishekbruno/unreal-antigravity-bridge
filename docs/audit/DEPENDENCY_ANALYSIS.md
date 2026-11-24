# Dependency and Coupling Analysis

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Audit Date:** 2026-11-24  

---

## 1. Executive Summary

A comprehensive architectural dependency and coupling analysis was performed across the complete execution chains of both source repositories:
- `unreal-codex-bridge-main`
- `unreal-engine-skills-for-claude-code-plugin-main`

The objective is to isolate AI-client-independent engineering capabilities from client-specific packaging, operating-system quirks, and Unreal Engine protocol expectations, ensuring that the new `unreal-antigravity-bridge` requires neither Codex nor Claude Code at runtime.

---

## 2. Four-Tier Architectural Classification

To establish clean boundaries, all components, data flows, and scripts are categorized into four distinct architectural tiers:

```
+---------------------------------------------------------------------------------+
| Tier 4: AI-Client Integration Infrastructure                                    |
| (Client manifests, plugin discovery, slash commands, prompt hooks, marketplace) |
+----------------------------------------+----------------------------------------+
                                         |
+----------------------------------------v----------------------------------------+
| Tier 1: AI-Client-Independent Engineering Infrastructure                        |
| (JSON-RPC transport, SQLite index, AST parser, dependency DAG, mutation locks)  |
+-------------------+-----------------------------------+-------------------------+
                    |                                   |
+-------------------v-------------------+   +-----------v-------------------------+
| Tier 2: Unreal Engine Infrastructure  |   | Tier 3: OS-Specific Infrastructure  |
| (Toolset discovery, .uproject, INI,   |   | (PowerShell CIM, lsof, WinRegistry, |
|  LogsToolset telemetry, PIE test map) |   |  process inspectors, loopback)      |
+---------------------------------------+   +-------------------------------------+
```

### Tier 1: AI-Client-Independent Engineering Infrastructure
- **Definition:** Pure computational, algorithmic, and protocol logic that operates identically regardless of which AI assistant or CLI invokes it.
- **Identified Modules:**
  - `scripts/bridge_mcp.py` (`core/transport.py`): Streamable HTTP and SSE client, JSON-RPC 2.0 parser, loopback validator.
  - `scripts/blueprint_parser.py` (`core/blueprint/blueprint_parser.py`): S-expression tokenizer, AST recursive descent parser, cyclomatic complexity counter.
  - `scripts/blueprint_spec.py` (`core/blueprint/blueprint_spec.py`): Declarative graph schema, pin connection rules, node validation.
  - `scripts/blueprint_mutation.py` (`core/blueprint/blueprint_mutation.py`): Atomic mutation transaction manager with `.mutation.lock` file locking and journal rollbacks.
  - `scripts/blueprint_verify.py` (`core/blueprint/blueprint_verify.py`): Verification of Blueprint compilation status and graph integrity.
  - `scripts/project_dependencies.py` (`core/intelligence/project_dependencies.py`): Asset dependency DAG builder, Tarjan's SCC cycle detector, transitive impact / blast radius analyzer.
  - `scripts/project_index.py` (`core/indexing/project_index.py`): SQLite persistent database with FTS5 full-text indexing, deterministic SHA-256 asset IDs, and incremental `mtime` refresh.
  - `scripts/query_project_index.py` (`core/indexing/query_project_index.py`): Ranked multi-tier context search query engine.
  - `scripts/generate_project_digest.py` (`core/indexing/generate_project_digest.py`): Token-budgeted project digest markdown generator.
- **Client Dependency Status:** **100% Free of AI Client Dependencies.** Zero imports of Codex, Claude, OpenAI, or Anthropic packages.

### Tier 2: Unreal Engine-Specific Infrastructure
- **Definition:** Modules that interface directly with Unreal Engine file formats, configuration conventions, plugins, and native toolsets.
- **Identified Components:**
  - `scripts/unreal_session.py` (`core/session.py`): Manages toolset catalog discovery (`list_toolsets`, `describe_toolset`, `call_tool`), tool input schema validation, dynamic on-demand tool loading.
  - Two-Factor Project Identity: Queries `LogsToolset.GetLogEntries` through MCP to match active project name and engine build version.
  - Engine INI Parser (`scripts/configure.py`): Reads and writes `DefaultEngine.ini`, specifically `[HTTPServer.Listeners]` directives.
  - Project Manifest (`.uproject`): Enables `ModelContextProtocol` and `AllToolsets` plugins.
  - Play-In-Editor Runner (`scripts/playtest.py`): Automates PIE execution via `EditorAppToolset` and inspects `Saved/Logs/`.
  - Non-Colliding Test Map Creator (`scripts/live_test.py`): Duplicates `/Engine/Maps/Templates/Template_Default` into test level namespace.
- **Client Dependency Status:** Independent of AI clients; dependent strictly on Epic Games Unreal Engine 5.8+ native MCP server.

### Tier 3: Operating-System-Specific Infrastructure
- **Definition:** Platform-specific process inspection, directory conventions, and operating system tooling.
- **Identified Components:**
  - `scripts/platform_adapter/windows.py`:
    - Process inspection via PowerShell `Get-CimInstance Win32_Process` or `Get-Process`.
    - Engine installation detection via Windows Registry (`HKLM:\SOFTWARE\EpicGames\Unreal Engine` and `HKCU:\SOFTWARE\Epic Games\Unreal Engine\Builds`).
    - Standard install paths (`C:\Program Files\Epic Games\UE_5.8`).
  - `scripts/platform_adapter/macos.py`:
    - Port ownership inspection via `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
    - Process arguments inspection via `ps -Ao pid,command`.
    - Engine bundle detection (`/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app`).
- **Client Dependency Status:** Contains one client coupling point (`resolve_codex_binary()`), which must be decoupled into Tier 4.

### Tier 4: AI-Client-Specific Integration Infrastructure
- **Definition:** Manifests, configuration files, CLI wrappers, and hook scripts that tie the system to a specific AI developer tool.
- **Identified Components in Source Repositories:**

| Client | Component | Type | Specific Coupling Detail | Status for Antigravity Core |
| :--- | :--- | :--- | :--- | :--- |
| **Codex** | `scripts/doctor.py` | Python Script | Calls `shutil.which('codex.cmd')`, `codex --version`, `codex mcp list` | **Decouple** into optional client verification |
| **Codex** | `scripts/configure.py` | Python Script | Reads and modifies `.codex/config.toml` | **Decouple** into client config adapter |
| **Codex** | `scripts/editor_lifecycle.py` | Python Script | Inspects `.codex/config.toml` in `status` and `uninstall` | **Decouple** into client-agnostic config check |
| **Codex** | `scripts/install.py` | Python Script | Copies plugin to `.codex-plugins/unreal-codex`, modifies `.agents/plugins/marketplace.json` | **Replace** with Antigravity-native installer |
| **Codex** | `scripts/platform_adapter/base.py` | Python Script | Defines abstract method `resolve_codex_binary()` | **Refactor** to remove client method from base OS adapter |
| **Codex** | `.codex-plugin/plugin.json` | Manifest | Codex plugin packaging format | **Exclude** from runtime core |
| **Codex** | `.agents/plugins/marketplace.json`| Manifest | OpenAI local marketplace format | **Exclude** from runtime core |
| **Claude** | `hooks/hooks.json` | Manifest | Claude Code hook manifest registering `SessionStart` | **Refactor** to Antigravity hook schema |
| **Claude** | `hooks/unreal-context.sh` | Shell Script | Bash script outputting Claude-specific JSON (`hookSpecificOutput.additionalContext`) | **Replace** with cross-platform Python context provider |
| **Claude** | `.claude-plugin/plugin.json` | Manifest | Claude Code plugin packaging format | **Exclude** from runtime core |
| **Claude** | `unreal-mcp/references/setup.md` | Markdown | Recommends `ModelContextProtocol.GenerateClientConfig ClaudeCode` | **Neutralize** client references |

---

## 3. Network and Transport Assumptions

1. **Endpoint Binding:**
   - Default: `http://127.0.0.1:8000/mcp`
   - Path: `/mcp`
   - Protocol: Streamable HTTP POST + Server-Sent Events (SSE)
   - Message Framing: JSON-RPC 2.0 (`{"jsonrpc": "2.0", "id": ..., "method": ..., "params": ...}`)
2. **Loopback Boundaries:**
   - Both IPv4 loopback (`127.0.0.1`) and IPv6 loopback (`::1`, `localhost`) are supported.
   - Redirects to remote endpoints (`301`, `302`, `307`, `308`) are explicitly blocked by `scripts/bridge_mcp.py` to prevent DNS rebinding and SSRF attacks.
3. **Port Collisions:**
   - Port 8000 is common; lifecycle CLI and `configure.py` allow overriding the port (e.g., `8001-8010`), and `platform_adapter` inspects the port owner PID before connection.

---

## 4. Unreal Engine Version Assumptions

1. **Target Version:** Unreal Engine 5.8 (specifically tested against UE 5.8.4 CL 58902052).
2. **Required Engine Plugins:**
   - `ModelContextProtocol` (`Engine/Plugins/Experimental/ModelContextProtocol/ModelContextProtocol.uplugin`): Provides embedded HTTP server and JSON-RPC router.
   - `AllToolsets` (`Engine/Plugins/Experimental/Toolsets/AllToolsets/AllToolsets.uplugin`): Provides the 53 toolsets and 832 tools.
   - `ToolsetRegistry` (`Engine/Plugins/Experimental/ToolsetRegistry/ToolsetRegistry.uplugin`): Tool discovery subsystem.
3. **Future Compatibility (UE 5.9+):**
   - UE 5.9 introduces an internal "Unreal Assistant" with Agent Client Protocol (ACP) support. The Streamable HTTP/SSE MCP server remains backward-compatible across versions.

---

## 5. Decoupling and Isolation Plan

To eliminate runtime coupling to Codex and Claude:
1. **Remove `resolve_codex_binary` from `PlatformAdapter`:** The platform adapter's sole responsibility is OS abstraction (Windows/macOS/Linux). Client executable detection belongs to client integration layers.
2. **Decouple `configure.py`:** Retain engine and INI configuration in the core; place `.codex/config.toml` logic in a legacy Codex adapter or remove it from the default execution path.
3. **Decouple `doctor.py`:** Make system diagnostics return status for Unreal Engine and MCP ports; make client checks optional plugin modules.
4. **Replace `unreal-context.sh`:** Implement a pure Python project detector (`core/context.py`) that executes identically on Windows PowerShell, macOS, and Linux, outputting structured context without requiring bash.
5. **Neutralize Skills:** Remove hardcoded references like "OpenAI Codex" or "Claude Code" in `skills/unreal-mcp/SKILL.md`, `skills/create-toolset/SKILL.md`, and `skills/unreal-skill/SKILL.md`, standardizing them for Google Antigravity.
