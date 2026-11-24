# Source Repository Audit

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Audit Date:** 2026-11-24  
**Auditor:** Principal Software Architect & Core Engineering Team  
**Audit Target Repositories:**
1. `unreal-codex-bridge-main` (Primary Engineering Foundation)
2. `unreal-engine-skills-for-claude-code-plugin-main` (Supplementary Skills & Workflows)

---

## 1. Executive Summary

A comprehensive, recursive static and dynamic audit was conducted on both source repositories provided in the workspace. The audit evaluated source tree composition, runtime dependencies, execution chains, platform adapters, automated test suites, security boundaries, and licensing requirements.

### Key Audit Findings:
1. **Primary Engineering Foundation (`unreal-codex-bridge-main`):**
   - Implements a production-grade Python engineering core communicating with Unreal Engine 5.8+ via Epic Games' native `ModelContextProtocol` and `AllToolsets` plugins.
   - Contains **43 Python files** (19 core/tooling scripts, 4 platform adapter modules, 20 test modules) and **40 Markdown documents/reports**.
   - Backed by **142 automated unit tests** achieving a **100% pass rate** in ~7.13s wall-clock time with zero pre-existing failures.
   - Pure Python standard library implementation (**Python 3.10+/3.12 verified**); requires **zero external pip dependencies** at runtime.
   - Fully cross-platform platform abstraction layer supporting **Windows (Win10/11 x64)** and **macOS (Apple Silicon arm64 & Intel x86_64)**.
   - Coupling to OpenAI Codex is confined to CLI discovery in `scripts/doctor.py`, config management in `scripts/configure.py`, package installer in `scripts/install.py`, and plugin manifests (`.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`). The underlying Unreal communication, AST parser, dependency graph, SQLite indexer, and session verification are already AI-client independent.

2. **Supplementary Repository (`unreal-engine-skills-for-claude-code-plugin-main`):**
   - Operates as a Claude Code plugin distribution package containing **12 total files**, 0 Python scripts, and 0 automated unit tests.
   - Contains high-value operational documentation, tool search guidelines, console command references, proxy recovery workflows, and asset naming conventions.
   - Contains a bash-only `SessionStart` hook (`hooks/unreal-context.sh`) that inspects `$PWD` for Unreal project markers (`.uproject`, `GenerateProjectFiles.*`) and injects contextual prompt guidance, but is hardcoded to Claude Code and fails on native Windows PowerShell without Git Bash.

---

## 2. Quantitative Inventory

| Metric | `unreal-codex-bridge-main` | `unreal-engine-skills-for-claude-code-plugin-main` | Consolidated Evaluation |
| :--- | :--- | :--- | :--- |
| **Total Files** | 140 (including caches) / 96 source files | 12 source files | 108 total source assets |
| **Python Files (`.py`)** | 43 | 0 | 43 Python modules |
| **Shell Scripts (`.sh`)** | 0 | 1 (`hooks/unreal-context.sh`) | 1 shell script |
| **JSON Manifests & Data** | 10 | 2 | 12 JSON files |
| **Markdown Documentation** | 40 | 6 | 46 Markdown files |
| **Configuration Templates** | 3 (`.ini`, `.toml`) | 0 | 3 templates |
| **Automated Tests** | 142 unit tests (20 test suites) | 0 | 142 baseline tests |
| **Test Pass Rate** | **100% (142/142 passed)** | N/A | Verified baseline |
| **Runtime Dependencies** | Python 3.10+ Standard Library only | Bash shell on PATH | Zero third-party packages |
| **License** | MIT License (Epic Games, Inc. 2026) | MIT License (Epic Games, Inc. 2026) | Compatible MIT |

---

## 3. Directory Structures

### 3.1 `unreal-codex-bridge-main` Structure

```
unreal-codex-bridge-main/
├── .agents/
│   └── plugins/
│       └── marketplace.json            # Local Codex plugin marketplace catalog
├── .codex-plugin/
│   └── plugin.json                     # Codex plugin manifest (skills & MCP definitions)
├── benchmarks/
│   └── five_star_game/
│       ├── acceptance.json             # 5-star game benchmark specification
│       └── README.md                   # Benchmark instructions and metrics
├── docs/                               # 28 architectural, security, and audit documents
│   ├── audits/                         # Feature matrix, test coverage, functional audit
│   ├── integration/                    # Cross-platform setup, troubleshooting, macOS/Win
│   ├── plans/                          # Development plans
│   ├── research/                       # Blueprint research, competitor analysis
│   ├── ARC01_STABILIZATION_REPORT.md   # ARC 01.5 stabilization report
│   ├── ARC02_API_CAPABILITIES.md       # Toolset and API capability mapping
│   ├── ARC02_BLUEPRINT_INTELLIGENCE.md # Blueprint AST intelligence
│   ├── ARC02_BLUEPRINT_TOOL_SCHEMAS.json # 164KB JSON schema of all 832 tools
│   ├── ARC02_DEPENDENCY_GRAPH.md       # Asset DAG and Tarjan's SCC analysis
│   ├── ARC02_PROJECT_INDEX.md          # SQLite indexer architecture
│   ├── ARC02_PROJECT_INTELLIGENCE.md   # Scene inspection and actor intelligence
│   ├── ARC_STATUS.md                   # Project status and milestone history
│   └── SECURITY.md                     # Security boundaries and loopback policies
├── reports/
│   ├── asset_dependencies.json         # Real project asset dependency dump (185 nodes)
│   ├── project_digest.md               # Generated project context digest markdown
│   └── project_intelligence.json       # Real project scene and asset inventory dump
├── scripts/                            # Core engineering and CLI tools
│   ├── platform_adapter/               # Cross-platform OS abstraction package
│   │   ├── __init__.py
│   │   ├── base.py                     # PlatformAdapter abstract base class
│   │   ├── detect.py                   # Platform factory and OS detection
│   │   ├── macos.py                    # macOS adapter (lsof, ps, bundles)
│   │   └── windows.py                  # Windows adapter (CIM, PowerShell, registry)
│   ├── blueprint_codegen.py            # Python script generator for Blueprint construction
│   ├── blueprint_mutation.py           # Safe Blueprint AST mutator with file locking
│   ├── blueprint_parser.py             # S-expression tokenizer, AST parser, cyclomatic complexity
│   ├── blueprint_spec.py               # Declarative Blueprint authoring DSL spec
│   ├── blueprint_verify.py             # Blueprint compile and graph verification
│   ├── bridge_mcp.py                   # Streamable HTTP/SSE MCP client & loopback transport
│   ├── configure.py                    # INI, .uproject, and config manager with preflight guards
│   ├── doctor.py                       # Diagnostics and system verification suite
│   ├── editor_lifecycle.py             # Unified CLI manager (detect, prepare, launch, status)
│   ├── generate_project_digest.py      # Token-budgeted project digest generator
│   ├── inspect_project.py              # Project introspection, scene assets, Blueprint graphs
│   ├── install.py                      # Codex project installer utility
│   ├── live_test.py                    # Safe live editor integration verification script
│   ├── playtest.py                     # PIE runner and runtime log harvester
│   ├── project_dependencies.py         # Asset dependency DAG, Tarjan's SCC, blast radius
│   ├── project_index.py                # Persistent SQLite FTS5 index engine
│   ├── query_project_index.py          # Multi-tier ranked context retrieval engine
│   └── unreal_session.py               # Session manager, 2FA project identity, dynamic toolsets
├── skills/                             # Codex skills
│   ├── create-toolset/SKILL.md         # C++ Toolset authoring guide
│   ├── unreal-game/SKILL.md            # Game development workflow
│   ├── unreal-mcp/                     # MCP operational instructions
│   │   ├── references/operations.md
│   │   ├── references/setup.md
│   │   └── SKILL.md
│   ├── unreal-playtest/SKILL.md        # Play-In-Editor testing skill
│   └── unreal-skill/SKILL.md           # Unreal Agent Skill authoring guide
├── templates/                          # Configuration templates
│   ├── config.toml.example
│   ├── DefaultEditorPerProjectUserSettings.ini.example
│   └── DefaultEngine.ini.example
├── tests/                              # Automated unit tests
│   ├── fixtures/
│   │   └── phase3-native-graph.json    # Verified native Blueprint graph fixture
│   └── test_*.py                       # 20 test modules (142 unit tests)
├── .gitignore
├── .mcp.json                           # Root MCP config
├── mcp.json                            # Duplicate MCP config
├── plugin.json                         # Duplicate root plugin manifest
├── AGENTS.md                           # Project instructions
├── AGENTS.unreal-codex.md              # Duplicate project instructions
├── LICENSE                             # MIT License (Epic Games, Inc. 2026)
└── README.md                           # Project overview and documentation
```

### 3.2 `unreal-engine-skills-for-claude-code-plugin-main` Structure

```
unreal-engine-skills-for-claude-code-plugin-main/
├── .claude-plugin/
│   └── plugin.json                     # Claude Code plugin manifest
├── hooks/
│   ├── hooks.json                      # Hook registration (SessionStart matcher)
│   └── unreal-context.sh               # Bash session-start project context injector
├── skills/
│   ├── create-toolset/
│   │   └── SKILL.md                    # C++ Toolset authoring guide
│   ├── unreal-mcp/
│   │   ├── references/
│   │   │   ├── operations.md           # Console commands & proxy recovery
│   │   │   └── setup.md                # MCP setup & proxy configuration
│   │   └── SKILL.md                    # Rich MCP workflow, tool search, domain rules
│   └── unreal-skill/
│       └── SKILL.md                    # In-editor Agent Skill authoring guide
├── .gitignore
├── CODEOWNERS
├── LICENSE                             # MIT License (Epic Games, Inc. 2026)
└── README.md                           # Claude Code plugin documentation
```

---

## 4. Component-by-Component Assessment

### 4.1 MCP Transport & Protocol
- **Source:** `unreal-codex-bridge-main/scripts/bridge_mcp.py`
- **Implementation Status:** Fully implemented, verified with real loopback server tests.
- **Capabilities:** JSON-RPC 2.0 framing, Streamable HTTP POST transport, Server-Sent Events (SSE) listener, session headers (`MCP-Session-Id`), pagination, strict loopback IP validation (`127.0.0.1`, `::1`), redirect refusal to remote hosts.
- **Client Coupling:** Minimal (`clientInfo` field in `initialize` set to `'unreal-codex-bridge'`).
- **Verdict:** **REUSE & MERGE** into `core/transport.py`.

### 4.2 Unreal Session & Identity Verification
- **Source:** `unreal-codex-bridge-main/scripts/unreal_session.py`
- **Implementation Status:** Fully implemented, verified against UE 5.8.4.
- **Capabilities:**
  - Dynamic toolset loading on demand (`load_toolset`), supporting all 53 toolsets and 832 tools.
  - Two-Factor Project Identity Verification:
    1. Process Verification: queries OS platform adapter to confirm the port listener is `UnrealEditor.exe` launched with the target `.uproject`.
    2. Telemetry Verification: queries `LogsToolset.GetLogEntries` via MCP to verify active log telemetry matches project name and engine build.
  - Argument validation against tool JSON schemas (`validate_inputs`).
- **Client Coupling:** Completely AI-client independent.
- **Verdict:** **REUSE** into `core/session.py`.

### 4.3 Platform Adapters
- **Source:** `unreal-codex-bridge-main/scripts/platform_adapter/`
- **Implementation Status:** Fully implemented across Windows and macOS.
- **Capabilities:**
  - `base.py`: Defines `PlatformAdapter` ABC.
  - `windows.py`: PowerShell CIM/WMI process inspection, registry engine discovery, executable resolution.
  - `macos.py`: `lsof -iTCP` listener detection, `ps -Ao` process inspection, macOS app bundle detection (`/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app`).
  - `detect.py`: Platform detection and adapter factory.
- **Client Coupling:** Contains `resolve_codex_binary()` in `base.py`, `windows.py`, and `macos.py`.
- **Verdict:** **REFACTOR & REUSE** into `adapters/platform/`. Remove client-specific methods from the base platform adapter; introduce a generic client resolution method or isolate client checks in integration adapters.

### 4.4 Editor Lifecycle Management
- **Source:** `unreal-codex-bridge-main/scripts/editor_lifecycle.py`
- **Implementation Status:** Fully implemented.
- **Capabilities:** CLI commands for `detect`, `prepare`, `launch`, `connect`, `doctor`, `status`, and `uninstall`. Manages automated backup of `.uproject` and INI settings.
- **Client Coupling:** Checks `.codex/config.toml` in `cmd_status` and `cmd_uninstall`.
- **Verdict:** **REFACTOR & REUSE** into `adapters/unreal/lifecycle.py` and `scripts/editor_lifecycle.py`. Make config status client-agnostic.

### 4.5 Configuration Management & Listener Preflight Guards
- **Source:** `unreal-codex-bridge-main/scripts/configure.py`
- **Implementation Status:** Fully implemented, verified with 8 comprehensive security tests.
- **Capabilities:**
  - `guard_listener_overrides`: Rejects wildcard bindings (`0.0.0.0`, `::`, `*`) and public IPs before modifying files.
  - Enables `ModelContextProtocol` and `AllToolsets` in `.uproject` with byte-preserving backups.
  - Configures `DefaultEngine.ini` loopback bindings safely.
  - Manages `.codex/config.toml` MCP server registration.
- **Client Coupling:** `codex_content()` and `configure_codex()` are Codex-specific.
- **Verdict:** **REFACTOR & REUSE** into `core/configure.py` and `scripts/configure.py`. Retain all engine and INI safety guards; extract client config generation into an extensible client adapter interface.

### 4.6 System Diagnostics & Doctor
- **Source:** `unreal-codex-bridge-main/scripts/doctor.py`
- **Implementation Status:** Fully implemented.
- **Capabilities:** 11 system diagnostic checks verifying OS, architecture, engine build, required plugins, loopback reachability, MCP handshake, and project identity.
- **Client Coupling:** `check_codex_binary()`, `check_codex_config()`, and `check_codex_mcp_list()`.
- **Verdict:** **REFACTOR & REUSE** into `core/diagnostics.py` and `scripts/doctor.py`. Maintain core Unreal diagnostics; decouple client CLI verification so Antigravity or other clients can register verification hooks.

### 4.7 Project Intelligence, Asset Dependencies & Indexing
- **Source:** `unreal-codex-bridge-main/scripts/`
  - `inspect_project.py`
  - `project_dependencies.py`
  - `project_index.py`
  - `query_project_index.py`
  - `generate_project_digest.py`
- **Implementation Status:** Fully implemented and verified.
- **Capabilities:**
  - Asset Dependency DAG with Tarjan's SCC cycle detection, transitive impact analysis, and blast radius calculation.
  - Persistent SQLite project database with FTS5 full-text indexing, deterministic SHA-256 IDs, and incremental `mtime` refresh (46% faster re-indexing).
  - Sub-10ms ranked multi-tier search query engine.
  - Token-budgeted project digest markdown generator reducing context overhead by 92.4%.
- **Client Coupling:** Completely AI-client independent.
- **Verdict:** **REUSE** into `core/intelligence/` and `core/indexing/`.

### 4.8 Blueprint Intelligence & AST Mutations
- **Source:** `unreal-codex-bridge-main/scripts/`
  - `blueprint_parser.py`
  - `blueprint_spec.py`
  - `blueprint_codegen.py`
  - `blueprint_mutation.py`
  - `blueprint_verify.py`
- **Implementation Status:**
  - Parser & AST Visitor: **Implemented & verified** (tokenizes Epic S-expressions, builds AST, calculates cyclomatic complexity).
  - DSL Spec: **Implemented & verified** (validates nodes, pins, directions, connections).
  - Mutation Engine: **Implemented & verified** (atomic file locks, journaled rollback, compile verification).
  - Code Generation: **Partially implemented** (basic templates; full declarative generation was paused for Integration Sprint 01).
- **Client Coupling:** Completely AI-client independent.
- **Verdict:** **REUSE & CONSOLIDATE** into `core/blueprint/`.

### 4.9 Play-In-Editor (PIE) & Live Testing
- **Source:** `unreal-codex-bridge-main/scripts/playtest.py`, `live_test.py`
- **Implementation Status:** Fully implemented.
- **Capabilities:** Automated PIE session initiation, log monitoring, error harvesting, test level duplication (`/Engine/Maps/Templates/Template_Default` to non-colliding test maps), actor spawning, transform verification.
- **Client Coupling:** Completely AI-client independent.
- **Verdict:** **REUSE** into `core/playtest.py` and `scripts/`.

### 4.10 Developer Skills & Documentation
- **Sources:**
  - `unreal-codex-bridge-main/skills/` (`create-toolset`, `unreal-game`, `unreal-mcp`, `unreal-playtest`, `unreal-skill`)
  - `unreal-engine-skills-for-claude-code-plugin-main/skills/` (`create-toolset`, `unreal-mcp`, `unreal-skill`)
- **Comparison & Analysis:**
  - `unreal-mcp`: The Claude version contains substantially more operational detail, comprehensive domain guidelines, tool search workflows (`list_toolsets` -> `describe_toolset` -> `call_tool`), asset naming conventions, and proxy recovery instructions. The Codex version has a more condensed format.
  - `unreal-game` & `unreal-playtest`: Present only in Codex bridge; essential for autonomous game authoring and verification.
  - `create-toolset` & `unreal-skill`: Both versions are conceptually identical, differing only in client branding mentions.
- **Verdict:** **MERGE & REFACTOR** into `skills/`. Merge the best operational depth from Claude's `unreal-mcp` with the workflows of Codex's `unreal-game` and `unreal-playtest`, neutralizing all client branding in favor of standard Antigravity skill structure.

### 4.11 Lifecycle Hooks
- **Source:** `unreal-engine-skills-for-claude-code-plugin-main/hooks/`
- **Implementation Status:** Functional bash script on POSIX; completely broken on native Windows PowerShell without Git Bash. Hardcoded to Claude Code output format and `GenerateClientConfig ClaudeCode`.
- **Verdict:** **REPLACE & REFACTOR**. Replace the bash-only hook with a client-independent Python context provider (`core/context.py` and cross-platform hooks) that runs natively on Windows, macOS, and Linux without external shell requirements.

---

## 5. Security Mechanisms Audit

1. **Loopback-Only Transport Security:**
   - Both repositories emphasize that localhost is not an absolute trust boundary.
   - `scripts/bridge_mcp.py` strictly restricts client HTTP/SSE connections to `127.0.0.1` and `::1`. Remote IP addresses and host redirects are unconditionally rejected.
2. **Listener Preflight Guards:**
   - `scripts/configure.py` parses `DefaultEngine.ini` and rejects wildcard (`0.0.0.0`, `::`, `*`) or external IP listener bindings before permitting any configuration modification.
3. **Two-Factor Project Identity Verification:**
   - Prevents an agent from sending destructive commands to the wrong editor when multiple Unreal instances are running.
   - Cross-checks the OS process listening on port 8000 against the expected `.uproject` path, and queries in-engine log telemetry.
4. **Safe Mutation Guards:**
   - `scripts/blueprint_mutation.py` uses `.mutation.lock` file locks to prevent race conditions during AST mutations and maintains journaled recovery files.
   - Test workflows duplicate clean template levels rather than modifying user levels.

---

## 6. Deprecated and Duplicate Components Identified

1. **Duplicate Manifests in `unreal-codex-bridge-main`:**
   - `.codex-plugin/plugin.json` vs `plugin.json` at root: Redundant definitions with minor schema differences.
   - `.mcp.json` vs `mcp.json` at root: Duplicate MCP server registrations.
   - `AGENTS.md` vs `AGENTS.unreal-codex.md`: Identical content duplicated.
2. **Duplicate Skills Content:**
   - `create-toolset/SKILL.md` and `unreal-skill/SKILL.md` duplicated between both repositories with only minor text changes ("Codex" vs "Claude").
3. **Client-Specific Installer:**
   - `scripts/install.py` is hardcoded to `.codex-plugins` and `.codex/config.toml`. Should be replaced with a client-agnostic project installer.

---

## 7. Audit Conclusion & Readiness

- **`unreal-codex-bridge-main`** provides a mature, robust, 100% test-verified engineering core with zero runtime third-party dependencies.
- **`unreal-engine-skills-for-claude-code-plugin-main`** provides superior MCP operational instructions, recovery documentation, and context-injection concepts.
- Consolidating the two repositories into **`unreal-antigravity-bridge`** by preserving the Codex engineering core, merging Claude's operational instructions, and decoupling AI-client-specific glue establishes an independent, production-grade foundation for Google Antigravity.
