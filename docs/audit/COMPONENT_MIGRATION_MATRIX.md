# Component Migration Matrix

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Audit Date:** 2026-11-24  

---

## 1. Migration Categories and Criteria

Every component from both source repositories is evaluated and assigned one of the following six classifications:

- **REUSE:** Reusable as-is or with trivial path adjustments. Preserves existing behavior, public API, and test coverage without regression risk.
- **MERGE:** Combines complementary capabilities from both repositories (e.g., merging Python implementation from Repo A with operational documentation and domain guidelines from Repo B).
- **REFACTOR:** Functionally sound but carries client-specific coupling (e.g., hardcoded `codex` binary checks, `.codex` folder paths, or bash-only scripts) that must be decoupled or generalized into client-agnostic interfaces.
- **REPLACE:** Architectural limitation or brittle implementation that should be superseded by a more robust, cross-platform alternative.
- **DEFER:** Valid future functionality that is intentionally paused, incomplete, or out of scope for ARC 01 Phase 01 (e.g., declarative graph code generation).
- **EXCLUDE:** Redundant manifests, deprecated duplicates, or client-specific proprietary artifacts that have no place in a client-independent core.

---

## 2. Component Migration Table

| Component Identifier | Original Source | Responsibility | Dependencies | Classification | Technical Justification | Target Location in New Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`bridge_mcp.py`** | Codex Bridge (`scripts/`) | Streamable HTTP and SSE MCP client, JSON-RPC 2.0 transport, loopback boundary enforcement | Python stdlib (`http.client`, `socket`, `json`, `ipaddress`, `urllib`) | **REUSE** | Self-contained, robust, and verified with 6 live-socket unit tests. Minimal client coupling in `clientInfo` can be generalized. | `core/transport.py` (aliased in `scripts/bridge_mcp.py` for test compat) |
| **`unreal_session.py`** | Codex Bridge (`scripts/`) | Session management, 2FA project identity verification, on-demand toolset loading, tool dispatch | Python stdlib, `bridge_mcp`, `platform_adapter` | **REUSE** | Core security and operational engine. Verifies project identity via OS process and engine logs. Completely client-independent. | `core/session.py` (aliased in `scripts/unreal_session.py`) |
| **`platform_adapter/base.py`** | Codex Bridge (`scripts/platform_adapter/`) | Abstract base class defining OS integration interface | Python stdlib (`abc`, `pathlib`, `typing`) | **REFACTOR** | Sound abstraction, but contains `resolve_codex_binary()` which tightly couples the OS adapter to Codex. Must decouple client binary checks into an optional client integration layer. | `adapters/platform/base.py` |
| **`platform_adapter/windows.py`** | Codex Bridge (`scripts/platform_adapter/`) | Windows OS adapter using PowerShell CIM and Registry | Python stdlib (`subprocess`, `winreg`, `os`) | **REFACTOR** | Excellent native Windows implementation. Needs decoupling of `codex.cmd` resolution. | `adapters/platform/windows.py` |
| **`platform_adapter/macos.py`** | Codex Bridge (`scripts/platform_adapter/`) | macOS adapter using `lsof`, `ps`, and `.app` bundles | Python stdlib (`subprocess`, `shutil`) | **REFACTOR** | Excellent native macOS implementation. Needs decoupling of `/usr/local/bin/codex` resolution. | `adapters/platform/macos.py` |
| **`platform_adapter/detect.py`** | Codex Bridge (`scripts/platform_adapter/`) | Factory function detecting host OS and returning adapter | `platform`, `base`, `windows`, `macos` | **REUSE** | Clean platform factory. Reusable as-is. | `adapters/platform/detect.py` |
| **`editor_lifecycle.py`** | Codex Bridge (`scripts/`) | Unified CLI lifecycle manager (`detect`, `prepare`, `launch`, `connect`, `doctor`, `status`) | Python stdlib, `platform_adapter`, `configure`, `doctor` | **REFACTOR** | Core lifecycle orchestration is production-ready. Status and uninstall subcommands contain checks for `.codex/config.toml` that should be made client-agnostic. | `adapters/unreal/lifecycle.py` & `scripts/editor_lifecycle.py` |
| **`configure.py`** | Codex Bridge (`scripts/`) | Backed-up configuration utility with listener preflight guards (`guard_listener_overrides`) | Python stdlib (`ipaddress`, `json`, `re`, `tomllib`) | **REFACTOR** | Critical security preflight guards prevent wildcard network exposure. The engine INI and `.uproject` configuration is reusable; the `.codex/config.toml` generator should be separated into a client-configurable adapter. | `core/configure.py` & `scripts/configure.py` |
| **`doctor.py`** | Codex Bridge (`scripts/`) | Diagnostic suite verifying OS, engine build, plugins, loopback, MCP handshake | Python stdlib, `platform_adapter`, `bridge_mcp`, `unreal_session` | **REFACTOR** | Diagnostic checks for Unreal Engine, ports, and identity are essential. Hardcoded `check_codex_binary` and `check_codex_config` checks must be made modular/optional. | `core/diagnostics.py` & `scripts/doctor.py` |
| **`inspect_project.py`** | Codex Bridge (`scripts/`) | Read-only project discovery, scene intelligence, asset inventory, Blueprint graph/var extraction | Python stdlib, `unreal_session`, `blueprint_parser` | **REUSE** | High-value project introspection engine. Produces structured JSON output. Completely client-independent. | `core/intelligence/inspect_project.py` & `scripts/inspect_project.py` |
| **`project_dependencies.py`** | Codex Bridge (`scripts/`) | Asset dependency DAG builder, Tarjan's SCC cycle detector, transitive impact / blast radius analyzer | Python stdlib (`collections`, `json`, `pathlib`) | **REUSE** | Pure algorithmic graph engine. Verified on real engine dumps (found 3 mannequin cycles). Completely client-independent. | `core/intelligence/project_dependencies.py` |
| **`project_index.py`** | Codex Bridge (`scripts/`) | Persistent SQLite project index engine with FTS5 search, SHA-256 IDs, incremental `mtime` refresh | Python stdlib (`sqlite3`, `hashlib`, `pathlib`) | **REUSE** | High-performance indexing engine providing 46% faster incremental indexing and sub-10ms retrieval. Completely client-independent. | `core/indexing/project_index.py` |
| **`query_project_index.py`** | Codex Bridge (`scripts/`) | Multi-tier context retrieval engine scoring exact path, name, function, variable, and FTS5 ranking | Python stdlib (`sqlite3`, `json`, `pathlib`) | **REUSE** | Deterministic ranked search engine. Reusable as-is. | `core/indexing/query_project_index.py` |
| **`generate_project_digest.py`** | Codex Bridge (`scripts/`) | Compact project context digest generator reducing token overhead by 92.4% (~1,410 tokens) | Python stdlib (`json`, `pathlib`) | **REUSE** | Excellent context compression utility for LLM prompt budgets. Reusable as-is. | `core/indexing/generate_project_digest.py` |
| **`blueprint_parser.py`** | Codex Bridge (`scripts/`) | Epic S-expression tokenizer, recursive-descent AST visitor, cyclomatic complexity calculator | Python stdlib (`re`, `json`, `typing`) | **REUSE** | Production-grade AST parser for Unreal Blueprint graph S-expressions. Completely client-independent. | `core/blueprint/blueprint_parser.py` |
| **`blueprint_spec.py`** | Codex Bridge (`scripts/`) | Declarative Blueprint authoring DSL specification and validation engine | Python stdlib (`json`, `pathlib`) | **REUSE** | Formal grammar and schema validation for Blueprint nodes, pins, directions, and connections. Reusable as-is. | `core/blueprint/blueprint_spec.py` |
| **`blueprint_mutation.py`** | Codex Bridge (`scripts/`) | Safe Blueprint mutation transaction manager with `.mutation.lock` file locking and journaled rollback | Python stdlib (`time`, `json`, `pathlib`) | **REUSE** | Essential safety guard against concurrent AST mutations and state corruption. Completely client-independent. | `core/blueprint/blueprint_mutation.py` |
| **`blueprint_verify.py`** | Codex Bridge (`scripts/`) | Post-mutation graph verification against live compiler results and AST structures | Python stdlib, `blueprint_parser` | **REUSE** | Compiler verification guard. Reusable as-is. | `core/blueprint/blueprint_verify.py` |
| **`blueprint_codegen.py`** | Codex Bridge (`scripts/`) | Blueprint Python code generator for autonomous graph generation | Python stdlib | **DEFER** | Autonomous generation is paused under ARC 02 Phase 3. Retain foundation in codebase but defer active expansion until ARC 02. | `core/blueprint/blueprint_codegen.py` |
| **`playtest.py`** | Codex Bridge (`scripts/`) | Cross-platform Play-In-Editor (PIE) test runner and runtime log telemetry harvester | Python stdlib, `unreal_session`, `platform_adapter` | **REUSE** | Robust PIE automation and error detection. Reusable as-is. | `scripts/playtest.py` |
| **`live_test.py`** | Codex Bridge (`scripts/`) | End-to-end live testing script for verifying level duplication, actor spawning, and persistence | Python stdlib, `unreal_session`, `bridge_mcp` | **REUSE** | Safe live verification workflow. Updates test map paths to non-colliding Antigravity test namespace (`/Game/AntigravityBridgeTests/...`). | `scripts/live_test.py` |
| **`install.py`** | Codex Bridge (`scripts/`) | Codex project installer registering skills, marketplace catalog, and config | Python stdlib | **REPLACE** | Tightly coupled to `.codex-plugins`, `.codex/config.toml`, and Codex marketplace. Must be replaced with a client-agnostic project installer supporting Antigravity plugin structure. | `scripts/install.py` (refactored) |
| **`hooks/unreal-context.sh`** | Claude Plugin (`hooks/`) | SessionStart hook detecting `.uproject` and injecting project context into chat session | Bash, `pwd`, `basename`, `dirname` | **REPLACE** | Bash script fails on Windows PowerShell and outputs Claude-specific JSON. Replace with a native Python context detector (`core/context.py`) and cross-platform Antigravity hook. | `core/context.py` & `hooks/` |
| **`skills/unreal-mcp/`** | Merged (Codex + Claude) | Live Unreal Editor MCP operational guidance, tool search workflows, and console commands | Markdown | **MERGE** | Claude version provides superior operational depth, tool search rules (`list_toolsets` -> `describe_toolset` -> `call_tool`), and proxy recovery; Codex version provides concise flow. Merge best elements, neutralizing branding for Antigravity. | `skills/unreal-mcp/` |
| **`skills/create-toolset/`** | Merged (Codex + Claude) | C++ Toolset authoring guide for extending Unreal MCP with custom tools | Markdown | **MERGE** | Identical content across both repositories. Standardize for Antigravity. | `skills/create-toolset/` |
| **`skills/unreal-skill/`** | Merged (Codex + Claude) | In-editor Agent Skill authoring guide | Markdown | **MERGE** | Identical content across both repositories. Standardize for Antigravity. | `skills/unreal-skill/` |
| **`skills/unreal-game/`** | Codex Bridge (`skills/`) | Game authoring workflow from natural language prompts | Markdown | **REUSE** | Comprehensive multi-step workflow for creating levels, spawning assets, and lighting scenes. Preserve intact. | `skills/unreal-game/` |
| **`skills/unreal-playtest/`** | Codex Bridge (`skills/`) | Play-In-Editor testing and runtime log telemetry workflow | Markdown | **REUSE** | Specialized playtesting and telemetry analysis instructions. Preserve intact. | `skills/unreal-playtest/` |
| **`benchmarks/five_star_game/`** | Codex Bridge (`benchmarks/`) | 5-Star collection game benchmark and acceptance criteria | JSON, Markdown | **REUSE** | Standardized benchmark for validating autonomous Unreal game creation. | `benchmarks/five_star_game/` |
| **Plugin Manifests (`.codex-plugin`, `.claude-plugin`)** | Both Repositories | Proprietary plugin manifests for Codex and Claude Code | JSON | **EXCLUDE** | Neither Codex nor Claude plugin formats are required at runtime. Replaced with client-agnostic core and Antigravity-compatible configuration. | Excluded from runtime |
| **Duplicate Manifests (`mcp.json`, `plugin.json`, `AGENTS.md`)** | Codex Bridge (root) | Redundant duplicate root files | JSON, Markdown | **EXCLUDE** | Duplicate copies created during prior development sprints. Pruned to maintain clean repository hygiene. | Excluded |
| **Automated Tests (`tests/`)** | Codex Bridge (`tests/`) | 142 unit tests covering transport, session, platform, indexing, parsing, mutations, security | Python `unittest`, `pytest` | **REUSE & ADAPT** | Complete baseline test suite migrated to verify engineering core in the new repository. | `tests/` |

---

## 3. Migration Summary by Category

| Category | Count | Percentage | Primary Components |
| :--- | :--- | :--- | :--- |
| **REUSE** | 16 | 51.6% | Transport, session, indexing, dependency graph, S-expression parser, mutation engine, verification, playtest, benchmarks, tests |
| **MERGE** | 3 | 9.7% | `unreal-mcp` skill, `create-toolset` skill, `unreal-skill` skill |
| **REFACTOR** | 6 | 19.4% | Platform adapters (Windows, macOS, base), editor lifecycle, configure preflight guards, doctor diagnostics |
| **REPLACE** | 2 | 6.5% | Bash session hook (`unreal-context.sh`), Codex installer (`install.py`) |
| **DEFER** | 1 | 3.2% | Autonomous Blueprint code generation (`blueprint_codegen.py`) |
| **EXCLUDE** | 3 | 9.7% | Client proprietary manifests (`.codex-plugin`, `.claude-plugin`), duplicate root JSONs (`plugin.json`, `mcp.json`) |
| **Total** | **31** | **100.0%** | Comprehensive component coverage |
