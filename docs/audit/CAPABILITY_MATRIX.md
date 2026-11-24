# Capability Matrix

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Audit Date:** 2026-11-24  

---

## 1. Overview

This matrix provides a component-level capability comparison between the two source repositories:
- **Repo A:** `unreal-codex-bridge-main` (Engineering foundation)
- **Repo B:** `unreal-engine-skills-for-claude-code-plugin-main` (Claude Code plugin)

The comparison evaluates functionality, implementation depth, test verification, cross-platform support, and client coupling.

---

## 2. Comparative Capability Matrix

| Capability Domain | Sub-Capability / Component | Repo A (`unreal-codex-bridge`) | Repo B (`claude-skills-plugin`) | Evaluation & Comparative Analysis | Preferred Implementation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Transport & Protocol** | Streamable HTTP Transport | Implemented (Python `http.client`, JSON-RPC 2.0) | Delegated to Claude Code MCP client | Repo A provides a self-contained, fully auditable client with session header management. | **Repo A** |
| | Server-Sent Events (SSE) | Implemented (chunked HTTP streamer) | Delegated to Claude Code MCP client | Repo A provides verified streaming parser tested against mock and live loopback sockets. | **Repo A** |
| | Loopback IP Enforcement | Implemented (`127.0.0.1`, `::1` only; rejects redirects) | Documented guidance only | Repo A enforces loopback boundaries in code; Repo B only documents it. | **Repo A** |
| **Session & Tool Discovery** | Two-Factor Project Identity Verification | Implemented (Process owner + `LogsToolset` telemetry) | Absent | Repo A prevents accidental mutation of unintended running Unreal instances. Critical safety layer. | **Repo A** |
| | Dynamic Toolset Discovery | Implemented (`list_toolsets`, `describe_toolset`, on-demand cache) | Documented (`list_toolsets`, `describe_toolset`, `call_tool`) | Both understand the same native UE protocol; Repo A has Python client implementation; Repo B has richer prompt guidelines. | **Merge** (Repo A code + Repo B prompt guidelines) |
| | Input Schema Validation | Implemented (JSON schema type and required check) | Delegated to client | Repo A validates tool arguments prior to network dispatch. | **Repo A** |
| **Platform Abstraction** | Windows Integration | Implemented (PowerShell CIM, Registry engine discovery) | Documented via Git Bash / WSL | Repo A runs natively on Windows PowerShell without external bash dependencies. | **Repo A** |
| | macOS Integration | Implemented (`lsof`, `ps -Ao`, `.app` bundle inspection) | Native bash support | Repo A provides Python abstraction; Repo B relies on shell scripts. | **Repo A** |
| | Linux / Container Support | Base interface prepared, detection stubbed | Native bash support | Both require future Linux adapter completion in ARC 02. | **Repo A Base** |
| **Editor Lifecycle** | Engine Auto-Detection | Implemented (Registry, default paths, `.uproject`) | Manual path specification | Repo A discovers installed engines (5.8+) automatically. | **Repo A** |
| | Project Preparation & Backup | Implemented (Auto-backup `.uproject` and INI) | Manual instructions | Repo A automates plugin activation and loopback binding with rollback backups. | **Repo A** |
| | Editor Launch & Status | Implemented (`cmd_launch`, `cmd_status` CLI) | Documented manual launch | Repo A provides scriptable CLI orchestration. | **Repo A** |
| **Security & Safety** | Listener Override Guards | Implemented (`guard_listener_overrides` in `configure.py`) | Absent | Repo A actively blocks wildcard (`0.0.0.0`) and WAN exposure in INI files. | **Repo A** |
| | Mutation Safety & File Locking | Implemented (`.mutation.lock` and journal rollbacks) | Documented source-control hygiene | Repo A provides programmatic file locking to avoid concurrent AST mutations. | **Repo A** |
| | Safe Map Duplication | Implemented (Duplicates templates to non-colliding test levels) | Documented | Repo A guarantees existing levels and assets are never overwritten during tests. | **Repo A** |
| **Project Intelligence** | Project Inspection & Asset Scan | Implemented (`inspect_project.py`, structured JSON output) | Absent | Repo A introspects actors, components, Blueprint graphs, variables, functions. | **Repo A** |
| | Asset Dependency DAG | Implemented (Tarjan's SCC cycles, blast radius) | Absent | Repo A builds complete project dependency graph and detects circular references. | **Repo A** |
| | SQLite Persistent Index | Implemented (FTS5 search, SHA-256 IDs, incremental `mtime`) | Absent | Repo A delivers sub-10ms context retrieval and 46% faster re-indexing. | **Repo A** |
| | Context Retrieval Engine | Implemented (`query_project_index.py` multi-tier scoring) | Absent | Repo A provides ranked search for names, classes, functions, variables, FTS. | **Repo A** |
| | Token-Budgeted Digest | Implemented (`generate_project_digest.py`, ~1,410 tokens) | Absent | Repo A compresses project context by 92.4% for agent prompt injection. | **Repo A** |
| **Blueprint Automation** | S-Expression AST Parser | Implemented (Tokenizer, AST visitor, cyclomatic complexity) | Absent | Repo A parses native Unreal Blueprint graph expressions into traversable AST. | **Repo A** |
| | Declarative Blueprint Spec | Implemented (DSL specification and validation) | Absent | Repo A defines declarative blueprint schema and pin connection rules. | **Repo A** |
| | Mutation & Compile Verify | Implemented (Atomic mutation runner with compile verification) | Absent | Repo A validates mutation transactions and compiler diagnostics. | **Repo A** |
| | Autonomous Graph Generation | Paused (Foundation laid in `blueprint_codegen.py`) | Absent | Paused per project roadmap; core foundation preserved for future phases. | **Repo A** |
| **Testing & Telemetry** | Play-In-Editor (PIE) Automation | Implemented (`playtest.py`, log telemetry harvester) | Absent | Repo A automates PIE runs and parses runtime error logs. | **Repo A** |
| | Unit Test Suite | Implemented (142 unit tests across 20 test modules) | 0 tests | Repo A provides verified baseline test suite (100% pass). | **Repo A** |
| | Benchmark Suite | Implemented (`benchmarks/five_star_game/`) | Absent | Repo A provides end-to-end game authoring benchmark with acceptance criteria. | **Repo A** |
| **Agent Skills & Workflows** | Live Editor MCP Skill (`unreal-mcp`) | Implemented (Streamlined for Codex) | Implemented (Comprehensive, rich instructions, recovery) | Repo B contains superior operational rules, toolset search guidance, domain mappings, and proxy recovery procedures. | **Repo B** |
| | Toolset Authoring (`create-toolset`) | Implemented (C++ Toolset guide) | Implemented (C++ Toolset guide) | Content is virtually identical; both explain ToolsetRegistry C++ authoring. | **Consolidate** |
| | In-Editor Agent Skill (`unreal-skill`) | Implemented (Unreal Agent Skill guide) | Implemented (Unreal Agent Skill guide) | Content is virtually identical; both explain in-editor agent skills. | **Consolidate** |
| | Game Authoring (`unreal-game`) | Implemented (NL game authoring workflow) | Absent | Repo A provides complete workflow for authoring playable games from prompts. | **Repo A** |
| | Playtesting (`unreal-playtest`) | Implemented (PIE state inspection and error triage) | Absent | Repo A provides dedicated playtesting workflow. | **Repo A** |
| **Lifecycle Integration** | Session Startup Context Injection | Absent (Implicit in agent guidance) | Implemented (`hooks/unreal-context.sh` via Claude hooks) | Repo B detects project root and injects context at session start. However, bash-only implementation is fragile on Windows. | **Refactor** (Convert bash logic to cross-platform Python) |
| **Packaging & Manifests** | Client Plugin Packaging | Codex plugin manifest (`.codex-plugin/plugin.json`, `marketplace.json`) | Claude plugin manifest (`.claude-plugin/plugin.json`) | Both are client-specific. Antigravity plugin manifest structure will be established for the unified project. | **Client-Agnostic Core** |

---

## 3. Capability Analysis Summary

1. **Engineering Core:** `unreal-codex-bridge-main` is overwhelmingly superior in technical depth, containing the entire Python execution chain, MCP transport, security preflights, AST parsing, SQLite indexing, dependency analysis, and automated tests.
2. **Operational Guidance & Workflows:** `unreal-engine-skills-for-claude-code-plugin-main` provides superior operational documentation for `unreal-mcp`, including recovery procedures, console commands, proxy management, and asset conventions.
3. **Session Discovery Concept:** Claude's `SessionStart` hook demonstrates an effective UX pattern for auto-detecting Unreal projects, which should be elevated from a fragile bash script into a robust cross-platform Python module in `unreal-antigravity-bridge`.
