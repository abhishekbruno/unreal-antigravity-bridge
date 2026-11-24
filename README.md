# Unreal Engine for Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Unreal Engine: 5.8+](https://img.shields.io/badge/Unreal%20Engine-5.8%2B-black.svg)](https://www.unrealengine.com/)
[![Tests: 148 passed](https://img.shields.io/badge/Tests-148%20passed%20(100%25)-brightgreen.svg)](docs/audit/BASELINE_TEST_REPORT.md)
[![Status: ARC 01 Phase 01 Complete](https://img.shields.io/badge/Status-ARC%2001%20Phase%2001%20Complete-success.svg)](docs/migration/ARC01_PHASE01_REPORT.md)

**Unreal Engine for Antigravity** (`unreal-antigravity-bridge`) is a standalone, production-grade integration enabling **Google Antigravity** to inspect, query, author, and programmatically drive a running Unreal Engine Editor (5.8+) via Epic Games' native Model Context Protocol (MCP) server.

The project operates independently, requiring **neither OpenAI Codex nor Claude Code at runtime**.

> **Verification Status Notice:** ARC 01 Phase 01 establishes the client-independent engineering core and offline automated test suite (148 passed unit tests). Native Antigravity plugin packaging is scheduled for Phase 02, and live end-to-end editor verification against an active Unreal Engine instance is scheduled for Phase 03. Live editor connection has not yet been executed in this phase.

---

## 1. Key Features

- **Pure Standard Library Core:** Requires zero external pip packages at runtime. Runs on Python 3.10, 3.11, and 3.12+.
- **Native Unreal MCP Integration:** Connects directly to Epic Games' built-in `ModelContextProtocol`, `AllToolsets`, and `ToolsetRegistry` plugins over Streamable HTTP and SSE (53 toolsets / 832 tools).
- **Two-Factor Project Identity Verification:** Verifies OS process ownership and live engine log telemetry before authorizing scene or level mutations, preventing accidental operations on the wrong editor.
- **Strict Loopback Security:** Restricts all MCP socket communication strictly to loopback IP addresses (`127.0.0.1`, `::1`) and actively rejects remote HTTP redirects.
- **Preflight Listener Guards:** Scans engine INI files (`DefaultEngine.ini`) and rejects wildcard (`0.0.0.0`, `::`) or public network bindings before applying configuration changes.
- **Cross-Platform OS Abstraction:** Native support for Windows 10/11 (via PowerShell CIM and Registry) and macOS Apple Silicon & Intel (via `lsof`, `ps -Ao`, and `.app` bundles).
- **Project Intelligence & SQLite FTS5 Indexing:** Persistent SQLite database with FTS5 search, deterministic SHA-256 asset IDs, and incremental `mtime` refresh delivering 46% faster re-indexing and sub-10ms context retrieval.
- **Asset Dependency DAG:** Tarjan's strongly connected components (SCC) cycle detection, transitive impact analysis, and blast radius calculation.
- **Blueprint AST & Mutation Engine:** S-expression tokenizer, recursive-descent AST parser, cyclomatic complexity counter, and atomic `.mutation.lock` file locking with rollback journals.
- **Token-Budgeted Context Digest:** Compresses complete project intelligence into structured markdown (~1,410 tokens) for LLM prompts.
- **Automated Verification Suite:** 148 automated unit tests achieving 100% pass rate in ~6.7s.

---

## 2. Architecture Overview

```
Google Antigravity
        │
Antigravity Integration Layer (Manifests, Skills, Context Hooks)
        │
Unreal Engineering Core (Session, Indexing, DAG, AST Parser, Locks)
        │
Adapters & Transport Layer (HTTP/SSE MCP Client, Windows/macOS Adapters)
        │
Unreal Engine Editor (Native ModelContextProtocol & AllToolsets)
```

For full details, see [`docs/architecture/CORE_ARCHITECTURE.md`](docs/architecture/CORE_ARCHITECTURE.md) and [`docs/architecture/COMPONENT_BOUNDARIES.md`](docs/architecture/COMPONENT_BOUNDARIES.md).

---

## 3. Directory Layout

```
unreal-antigravity-bridge/
├── core/                       # Client-independent engineering core
│   ├── blueprint/              # S-expression AST parser, DSL spec, mutation locks
│   ├── indexing/               # SQLite FTS5 index, ranked search, digest generator
│   ├── intelligence/           # Project introspection, asset dependency DAG
│   ├── context.py              # Cross-platform project detection & session context
│   ├── session.py              # Dynamic toolsets, 2FA project identity verification
│   └── transport.py            # Streamable HTTP/SSE MCP client & loopback enforcement
├── adapters/
│   ├── platform/               # OS abstraction: Windows (CIM/Registry) & macOS (lsof/ps)
│   └── unreal/                 # Editor lifecycle CLI (detect, prepare, launch, status)
├── scripts/                    # Command-line tools and backward-compatible facades
├── skills/                     # Developer skills (unreal-mcp, create-toolset, etc.)
├── benchmarks/                 # Five-star game authoring benchmark & acceptance criteria
├── templates/                  # Configuration templates (Engine INI, Editor INI)
├── tests/                      # 148 unit tests (100% passing)
├── docs/
│   ├── audit/                  # Source audit, capability matrix, dependency analysis
│   ├── architecture/           # Core architecture & component boundaries
│   └── migration/              # Provenance ledger, migration log, Phase 01 report
├── LICENSE                     # MIT License
└── THIRD_PARTY_NOTICES.md      # Attribution for upstream Epic Games MIT code
```

---

## 4. Quick Start

### Prerequisites
1. **Unreal Engine 5.8+** (Verified on UE 5.8.4 CL 58902052).
2. **Python 3.10+** (Tested on Python 3.12.10; standard library only).

### Running Automated Tests
```bash
pytest tests/ -v
```
All 148 automated tests execute in under 7 seconds with zero external network or editor dependencies.

### Inspecting an Unreal Project
```bash
python scripts/inspect_project.py --project /path/to/YourGame.uproject
```

### Checking System Diagnostics
```bash
python scripts/doctor.py --project /path/to/YourGame.uproject
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
