# Source Provenance and Attribution Ledger

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Audit Date:** 2026-11-24  

---

## 1. Upstream Source Repositories

This project integrates source code, algorithms, workflows, and documentation from two primary upstream open-source repositories:

1. **Unreal Codex Bridge (`unreal-codex-bridge-main`)**
   - **Original Author/Copyright:** Copyright (c) 2026 Epic Games, Inc.
   - **Upstream License:** MIT License
   - **Primary Role:** Engineering foundation, Python core modules, platform adapters, SQLite indexer, AST parser, test suites, benchmarks.
2. **Unreal Engine Skills for Claude Code Plugin (`unreal-engine-skills-for-claude-code-plugin-main`)**
   - **Original Author/Copyright:** Copyright (c) 2026 Epic Games, Inc.
   - **Upstream License:** MIT License
   - **Primary Role:** Operational documentation, toolset discovery rules, proxy recovery guidelines, session start context heuristics.

---

## 2. Component Provenance Ledger

| Target Path in `unreal-antigravity-bridge` | Upstream Source Repository | Original Upstream Path | Original Lines | Attribution & Modifications Applied |
| :--- | :--- | :--- | :---: | :--- |
| `core/transport.py` | `unreal-codex-bridge-main` | `scripts/bridge_mcp.py` | 152 | Copyright (c) 2026 Epic Games, Inc. Added `client_name` and `client_version` parameterization; aliased `MCPClient = Client`. |
| `core/session.py` | `unreal-codex-bridge-main` | `scripts/unreal_session.py` | 212 | Copyright (c) 2026 Epic Games, Inc. Clean extraction of toolset discovery, schema validator, and two-factor project identity engine. |
| `core/context.py` | `unreal-engine-skills-for-claude-code-plugin-main` | `hooks/unreal-context.sh` | 85 | Copyright (c) 2026 Epic Games, Inc. Complete architectural reimplementation from fragile bash script into cross-platform Python standard library module. |
| `core/configure.py` | `unreal-codex-bridge-main` | `scripts/configure.py` | 258 | Copyright (c) 2026 Epic Games, Inc. Preserved `guard_listener_overrides` and INI parser. |
| `core/diagnostics.py` | `unreal-codex-bridge-main` | `scripts/doctor.py` | 134 | Copyright (c) 2026 Epic Games, Inc. Preserved Unreal Engine build, loopback, and identity verification checks. |
| `core/intelligence/inspect_project.py` | `unreal-codex-bridge-main` | `scripts/inspect_project.py` | 338 | Copyright (c) 2026 Epic Games, Inc. Preserved project introspection and actor hierarchy extraction. |
| `core/intelligence/project_dependencies.py`| `unreal-codex-bridge-main` | `scripts/project_dependencies.py` | 344 | Copyright (c) 2026 Epic Games, Inc. Preserved asset DAG builder, Tarjan's SCC cycle detector, and blast radius calculator. |
| `core/indexing/project_index.py` | `unreal-codex-bridge-main` | `scripts/project_index.py` | 510 | Copyright (c) 2026 Epic Games, Inc. Preserved SQLite FTS5 database schema, SHA-256 asset IDs, and incremental `mtime` cache. |
| `core/indexing/query_project_index.py` | `unreal-codex-bridge-main` | `scripts/query_project_index.py` | 342 | Copyright (c) 2026 Epic Games, Inc. Preserved multi-tier ranked search engine. |
| `core/indexing/generate_project_digest.py`| `unreal-codex-bridge-main` | `scripts/generate_project_digest.py`| 240 | Copyright (c) 2026 Epic Games, Inc. Preserved token-budgeted markdown context digest generator. |
| `core/blueprint/blueprint_parser.py` | `unreal-codex-bridge-main` | `scripts/blueprint_parser.py` | 248 | Copyright (c) 2026 Epic Games, Inc. Preserved S-expression tokenizer, AST parser, and cyclomatic complexity calculator. |
| `core/blueprint/blueprint_spec.py` | `unreal-codex-bridge-main` | `scripts/blueprint_spec.py` | 132 | Copyright (c) 2026 Epic Games, Inc. Preserved declarative Blueprint graph DSL grammar and pin connection validator. |
| `core/blueprint/blueprint_mutation.py` | `unreal-codex-bridge-main` | `scripts/blueprint_mutation.py` | 196 | Copyright (c) 2026 Epic Games, Inc. Preserved `.mutation.lock` file locking and journaled rollback engine. |
| `core/blueprint/blueprint_verify.py` | `unreal-codex-bridge-main` | `scripts/blueprint_verify.py` | 82 | Copyright (c) 2026 Epic Games, Inc. Preserved post-mutation graph compiler verification. |
| `core/blueprint/blueprint_codegen.py` | `unreal-codex-bridge-main` | `scripts/blueprint_codegen.py` | 32 | Copyright (c) 2026 Epic Games, Inc. Preserved Python script generator foundation (deferred expansion). |
| `adapters/platform/base.py` | `unreal-codex-bridge-main` | `scripts/platform_adapter/base.py` | 137 | Copyright (c) 2026 Epic Games, Inc. Preserved `PlatformAdapter` ABC. |
| `adapters/platform/windows.py` | `unreal-codex-bridge-main` | `scripts/platform_adapter/windows.py` | 215 | Copyright (c) 2026 Epic Games, Inc. Preserved PowerShell CIM and Windows Registry engine discovery. |
| `adapters/platform/macos.py` | `unreal-codex-bridge-main` | `scripts/platform_adapter/macos.py` | 231 | Copyright (c) 2026 Epic Games, Inc. Preserved `lsof`, `ps`, and macOS `.app` bundle inspection. |
| `adapters/platform/detect.py` | `unreal-codex-bridge-main` | `scripts/platform_adapter/detect.py` | 36 | Copyright (c) 2026 Epic Games, Inc. Preserved platform factory. |
| `adapters/unreal/lifecycle.py` | `unreal-codex-bridge-main` | `scripts/editor_lifecycle.py` | 269 | Copyright (c) 2026 Epic Games, Inc. Preserved lifecycle CLI and automation orchestration. |
| `scripts/playtest.py` | `unreal-codex-bridge-main` | `scripts/playtest.py` | 139 | Copyright (c) 2026 Epic Games, Inc. Preserved PIE test execution and log error harvesting. |
| `scripts/live_test.py` | `unreal-codex-bridge-main` | `scripts/live_test.py` | 208 | Copyright (c) 2026 Epic Games, Inc. Preserved safe template duplication and live test verification. |
| `benchmarks/five_star_game/` | `unreal-codex-bridge-main` | `benchmarks/five_star_game/` | 140 | Copyright (c) 2026 Epic Games, Inc. Preserved five-star game benchmark specification and acceptance criteria. |
| `skills/unreal-mcp/` | Merged (`unreal-codex-bridge-main` + `claude-skills-plugin`) | `skills/unreal-mcp/` | 262 | Merged Claude operational depth and proxy recovery with Codex concise flow; branded for Antigravity. |
| `skills/create-toolset/` | Merged | `skills/create-toolset/` | 421 | Merged C++ Toolset authoring guide; neutralized AI client branding for Antigravity. |
| `skills/unreal-skill/` | Merged | `skills/unreal-skill/` | 113 | Merged in-editor Agent Skill authoring guide; neutralized branding for Antigravity. |
| `skills/unreal-game/` | `unreal-codex-bridge-main` | `skills/unreal-game/` | 95 | Copyright (c) 2026 Epic Games, Inc. Natural language game creation workflow; neutralized branding for Antigravity. |
| `skills/unreal-playtest/` | `unreal-codex-bridge-main` | `skills/unreal-playtest/` | 98 | Copyright (c) 2026 Epic Games, Inc. Automated PIE testing workflow; neutralized branding for Antigravity. |
| `tests/` | `unreal-codex-bridge-main` | `tests/` | 1,842 | Migrated all 20 test modules (142 unit tests) intact. |
| `tests/test_core_architecture.py` | Newly Authored | N/A | 95 | Authored new unit tests validating pure standard library imports, client independence, and context detection. |

---

## 3. Compliance and License Verification

- All components copied or derived from the upstream repositories remain subject to the **MIT License**.
- The copyright notice `Copyright (c) 2026 Epic Games, Inc.` is preserved in `LICENSE`, `THIRD_PARTY_NOTICES.md`, and this provenance ledger.
- No confidential, proprietary, or machine-specific credentials were transferred.
