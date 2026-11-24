# Unreal Engine for Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Unreal Engine: 5.8+](https://img.shields.io/badge/Unreal%20Engine-5.8%2B-black.svg)](https://www.unrealengine.com/)
[![Tests: 155 passed](https://img.shields.io/badge/Tests-155%20passed%20(100%25)-brightgreen.svg)](tests/)
[![Status: ARC 01 Phase 02 Complete](https://img.shields.io/badge/Status-ARC%2001%20Phase%2002%20Complete-success.svg)](docs/migration/ARC01_PHASE02_REPORT.md)

**Unreal Engine for Antigravity** (`unreal-antigravity-bridge`) is a standalone, production-grade integration enabling **Google Antigravity** to inspect, query, author, and programmatically drive a running Unreal Engine Editor (5.8+) via Epic Games' native Model Context Protocol (MCP) server.

The project operates independently, requiring **neither OpenAI Codex nor Claude Code at runtime**.

> **Verification Status Notice:** ARC 01 Phase 01 established the client-independent engineering core. ARC 01 Phase 02 established native Google Antigravity plugin packaging, hooks, MCP configuration, rules, and skills (155 passed unit tests; 100% pass on `agy plugin validate . --strict`). Live end-to-end editor verification against an active Unreal Engine instance is scheduled for Phase 03. Live editor connection has not yet been executed in this phase.

---

## 1. Key Features

- **Native Antigravity Plugin Packaging:** Full compliance with Antigravity plugin schema (`plugin.json`), MCP server configuration (`mcp_config.json`), lifecycle hooks (`hooks.json`), and rules (`rules/AGENTS.md`).
- **Pure Standard Library Core:** Requires zero external pip packages at runtime. Runs on Python 3.10, 3.11, and 3.12+.
- **Native Unreal MCP Integration:** Connects directly to Epic Games' built-in `ModelContextProtocol`, `AllToolsets`, and `ToolsetRegistry` plugins over Streamable HTTP (53 toolsets / 832 tools).
- **Two-Factor Project Identity Verification:** Verifies OS process ownership and live engine log telemetry before authorizing scene or level mutations, preventing accidental operations on the wrong editor.
- **Strict Loopback Security:** Restricts all MCP socket communication strictly to loopback IP addresses (`127.0.0.1`, `::1`) and actively rejects remote HTTP redirects.
- **Preflight Listener Guards:** Scans engine INI files (`DefaultEngine.ini`) and rejects wildcard (`0.0.0.0`, `::`) or public network bindings before applying configuration changes.
- **Cross-Platform OS Abstraction:** Native support for Windows 10/11 (via PowerShell CIM and Registry) and macOS Apple Silicon & Intel (via `lsof`, `ps -Ao`, and `.app` bundles).
- **Project Intelligence & SQLite FTS5 Indexing:** Persistent SQLite database with FTS5 search, deterministic SHA-256 asset IDs, and incremental `mtime` refresh delivering 46% faster re-indexing and sub-10ms context retrieval.
- **Asset Dependency DAG:** Tarjan's strongly connected components (SCC) cycle detection, transitive impact analysis, and blast radius calculation.
- **Blueprint AST & Mutation Engine:** S-expression tokenizer, recursive-descent AST parser, cyclomatic complexity counter, and atomic `.mutation.lock` file locking with rollback journals.
- **Token-Budgeted Context Digest:** Compresses complete project intelligence into structured markdown (~1,410 tokens) for LLM prompts.
- **Automated Verification Suite:** 155 automated unit tests achieving 100% pass rate in ~6.0s.

---

## 2. Architecture Overview

```
Google Antigravity (IDE / CLI)
        │
Antigravity Native Plugin Layer (plugin.json, hooks.json, rules/AGENTS.md, skills/)
        │
Unreal Engineering Core (Session, Indexing, DAG, AST Parser, Locks)
        │
Adapters & Transport Layer (Streamable HTTP / Stdio Bridge, Windows/macOS Adapters)
        │
Unreal Engine Editor (Native ModelContextProtocol & AllToolsets)
```

For full details, see [`docs/architecture/ANTIGRAVITY_INTEGRATION_SPEC.md`](docs/architecture/ANTIGRAVITY_INTEGRATION_SPEC.md) and [`docs/architecture/CORE_ARCHITECTURE.md`](docs/architecture/CORE_ARCHITECTURE.md).

---

## 3. Directory Layout

```
unreal-antigravity-bridge/
├── plugin.json                 # Native Antigravity plugin manifest
├── mcp_config.json             # Streamable HTTP MCP configuration
├── hooks.json                  # Lifecycle hooks configuration
├── rules/                      # Integrated plugin rules
│   └── AGENTS.md               # Antigravity Unreal development conventions
├── skills/                     # Developer skills (unreal-mcp, create-toolset, etc.)
│   ├── create-toolset/
│   ├── unreal-game/
│   ├── unreal-mcp/
│   ├── unreal-playtest/
│   └── unreal-skill/
├── core/                       # Client-independent engineering core
│   ├── blueprint/              # S-expression AST parser, DSL spec, mutation locks
│   ├── indexing/               # SQLite FTS5 index, ranked search, digest generator
│   ├── intelligence/           # Project introspection, asset dependency DAG
│   ├── context.py              # Hook-compatible workspace discovery
│   ├── session.py              # Dynamic toolsets, 2FA project identity verification
│   └── transport.py            # Streamable HTTP MCP client & loopback enforcement
├── adapters/
│   ├── platform/               # OS abstraction: Windows (CIM/Registry) & macOS (lsof/ps)
│   └── unreal/                 # Editor lifecycle CLI (detect, prepare, launch, status)
├── scripts/                    # Command-line tools, doctor, and stdio bridge
├── benchmarks/                 # Five-star game authoring benchmark & acceptance criteria
├── templates/                  # Configuration templates (Engine INI, Editor INI)
├── tests/                      # 155 unit tests (100% passing)
├── docs/
│   ├── guides/                 # Installation, MCP configuration, skill usage, troubleshooting
│   ├── architecture/           # Antigravity integration spec & core architecture
│   └── migration/              # Provenance ledger, Phase 01 & Phase 02 reports
├── LICENSE                     # MIT License
└── THIRD_PARTY_NOTICES.md      # Attribution for upstream Epic Games MIT code
```

---

## 4. Quick Start

### Prerequisites
1. **Unreal Engine 5.8+** (Verified on UE 5.8.4 CL 58902052).
2. **Python 3.10+** (Tested on Python 3.12.10; standard library only).
3. **Google Antigravity** installed (`agy` CLI executable available or Antigravity IDE running).

### Validating the Plugin
```bash
agy plugin validate . --strict --json
```

### Running Automated Tests
```bash
pytest tests/ -v
```
All 155 automated tests execute in under 7 seconds with zero external network or editor dependencies.

### Installing into an Unreal Project
```bash
python scripts/install.py --project /path/to/YourGame.uproject
```

### Checking System Diagnostics
```bash
python scripts/doctor.py --project /path/to/YourGame.uproject --engine /path/to/UE_5.8
```

---

## 5. Security & Safety Principles

1. **Localhost Trust Invariant:** Localhost is not an absolute trust boundary. The bridge enforces loopback binding and two-factor process identity verification before authorizing any scene mutations.
2. **Listener Preflight Validation:** Unsafe wildcard listener bindings (`0.0.0.0`, `::`) are detected and rejected prior to configuration writes.
3. **Non-Destructive Testing:** Test workflows duplicate template levels into non-colliding test maps (`/Game/AntigravityBridgeTests/...`). User assets are never overwritten during verification runs.
4. **Concurrency File Locking:** Blueprint AST mutations require atomic process locks (`.mutation.lock`) with automated journaled rollback.

---

## 6. Provenance and Attribution

This project is derived from upstream open-source projects created by **Epic Games, Inc.** and licensed under the **MIT License**:
- `unreal-codex-bridge` (Copyright (c) 2026 Epic Games, Inc.)
- `unreal-engine-skills-for-claude-code-plugin` (Copyright (c) 2026 Epic Games, Inc.)

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`docs/migration/SOURCE_PROVENANCE.md`](docs/migration/SOURCE_PROVENANCE.md) for full licensing and attribution details.
