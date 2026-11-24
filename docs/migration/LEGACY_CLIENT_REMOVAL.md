# Legacy Client Removal Audit

**Milestone:** ARC 01 — Phase 02: Native Antigravity Packaging  
**Date:** November 2026  
**Status:** COMPLETE & CERTIFIED  

---

## 1. Executive Summary

In ARC 01 Phase 02, all runtime dependencies, packaging manifests, configuration artifacts, and legacy conventions tied specifically to OpenAI Codex or Anthropic Claude Code have been eliminated from the standalone repository `unreal-antigravity-bridge`.

The bridge now runs as a native Google Antigravity plugin with zero external AI client dependencies.

---

## 2. Inventory of Removed Legacy Artifacts

| Item / Directory | Previous Purpose | Removal Action | Antigravity Replacement |
| :--- | :--- | :--- | :--- |
| `.codex-plugin/` | Codex packaging directory containing `plugin.json` | **Deleted completely** | Native root `plugin.json` adhering to Antigravity schema |
| `.agents/plugins/marketplace.json` | Codex marketplace catalog definition | **Deleted completely** | Native Antigravity plugin loader and CLI |
| `AGENTS.unreal-codex.md` | Codex prompt injection file | **Deleted completely** | `rules/AGENTS.md` native plugin rules |
| `.mcp.json` / `mcp.json` (root) | Duplicate OpenAI-style MCP configuration | **Deleted completely** | `mcp_config.json` native Antigravity Streamable HTTP |
| `hooks/hooks.json` | Claude Code hook directory | **Standardized** | `hooks.json` directly at plugin root |
| `hookSpecificOutput` | Claude Code JSON output schema | **Replaced** | Antigravity `injectSteps` with `systemMessage` |
| `resolve_codex_binary` | Hardcoded Codex CLI resolution | **Refactored** | `resolve_client_binary("agy")` / `resolve_agy_binary()` |
| `.codex/config.toml` | Codex MCP registration format | **Deprecated & Replaced** | `mcp_config.json` |

---

## 3. Core Architecture Purity Verification

As verified by `tests/test_core_architecture.py`:
- `core/` modules have **zero imports** of `codex`, `claude`, `openai`, or `anthropic`.
- All core operations rely strictly on the Python standard library (`json`, `urllib`, `pathlib`, `socket`, `subprocess`).
- `core.transport.MCPClient` identifies as `unreal-antigravity-bridge` (version `0.1.0-alpha.2`).

---

## 4. Test Suite Certification

`tests/test_plugin_packaging.py` asserts the complete absence of legacy artifacts:
- Confirms `.codex-plugin` does not exist.
- Confirms `.agents/plugins/marketplace.json` does not exist.
- Confirms `AGENTS.unreal-codex.md` does not exist.
- Confirms legacy `mcp.json` and `.mcp.json` do not exist.
- Confirms `agy plugin validate . --strict` passes with 0 errors and 0 warnings.
