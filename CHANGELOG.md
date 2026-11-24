# Changelog

All notable changes to **Unreal Engine for Antigravity** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha.2] - 2026-11-24

### Added
- Native Google Antigravity plugin packaging (`plugin.json`) with vector logo (`assets/logo.svg`) and interactive suggested prompts.
- Native Streamable HTTP MCP configuration (`mcp_config.json`) targeting `http://127.0.0.1:8000/mcp`.
- Native lifecycle hooks (`hooks.json`) implementing the Antigravity `SessionStart` contract with `injectSteps` and `systemMessage`.
- Antigravity developer rules in `rules/AGENTS.md`.
- Stdio MCP bridge (`scripts/mcp_stdio_bridge.py`) for environments requiring stdio child process transport.
- Antigravity CLI detection (`resolve_client_binary("agy")` / `resolve_agy_binary()`) in Windows and macOS platform adapters.
- Comprehensive user guides: `docs/guides/INSTALLATION.md`, `docs/guides/MCP_CONFIGURATION.md`, `docs/guides/SKILL_USAGE.md`, and `docs/guides/TROUBLESHOOTING.md`.
- Integration specification (`docs/architecture/ANTIGRAVITY_INTEGRATION_SPEC.md`).
- Automated tests for `agy plugin validate . --strict`, hook execution, stdio bridge error handling, and Antigravity binary resolution (expanded suite to 155 unit tests).

### Changed
- Refactored `scripts/install.py` to be a native Antigravity plugin installer with `--global` and local workspace support.
- Modernized `scripts/doctor.py` to prioritize Google Antigravity CLI and validate native `mcp_config.json` registrations.
- Updated `core/context.py` to support `--hook` execution mode reading JSON metadata on stdin.

### Removed
- Removed legacy OpenAI Codex packaging directory `.codex-plugin/`.
- Removed legacy marketplace catalog `.agents/plugins/marketplace.json`.
- Removed legacy prompt file `AGENTS.unreal-codex.md`.
- Removed duplicate legacy manifests `.mcp.json` and `mcp.json`.
- Removed required runtime dependencies on OpenAI Codex or Claude Code.

## [0.1.0-alpha.1] - 2026-11-24

### Added
- Initial standalone repository `unreal-antigravity-bridge`.
- Client-independent Unreal Engineering Core (`core/session.py`, `core/transport.py`, `core/context.py`, `core/indexing/`, `core/intelligence/`, `core/blueprint/`).
- Automated unit test suite with 148 passing tests.
- Comprehensive source repository audit and capability matrix.
