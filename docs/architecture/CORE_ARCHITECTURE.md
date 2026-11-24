# Core Architecture Specification

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Document Version:** 1.0.0  
**Date:** 2026-11-24  

---

## 1. Architectural Vision

The primary mission of **Unreal Engine for Antigravity** (`unreal-antigravity-bridge`) is to deliver a standalone, production-grade integration between **Google Antigravity** and **Unreal Engine 5.8+** via Epic Games' native `ModelContextProtocol` and `AllToolsets` engine plugins.

The architecture strictly decouples the AI client integration layer from the underlying Unreal engineering core. The engineering core operates independently, requiring neither OpenAI Codex nor Claude Code at runtime.

---

## 2. Layered Architecture

```
+--------------------------------------------------------------------------+
|                            Google Antigravity                            |
|             (Antigravity Assistant / Workflow Orchestrator)              |
+------------------------------------+-------------------------------------+
                                     |
+------------------------------------v-------------------------------------+
|                      Antigravity Integration Layer                       |
|  - Native Antigravity Plugin Manifests                                   |
|  - Skill Declarations & Activation Rules (unreal-mcp, unreal-game, etc.) |
|  - Agent System Prompt Heuristics & Context Hook Integration             |
|  - Client MCP Registry & Endpoint Binding (.mcp.json)                    |
+------------------------------------+-------------------------------------+
                                     |
+------------------------------------v-------------------------------------+
|                        Unreal Engineering Core                           |
|  - Session State & On-Demand Toolset Catalog Manager (core/session.py)   |
|  - Two-Factor Project Identity Verification Engine                       |
|  - S-Expression Blueprint AST Parser & Cyclomatic Counter                |
|  - Declarative Blueprint DSL Specification & Validator                   |
|  - Atomic Blueprint Mutation Engine with File Locking (.mutation.lock)   |
|  - Asset Dependency DAG Builder & Tarjan's SCC Cycle Detection           |
|  - SQLite Persistent Index Engine with FTS5 & Incremental mtime Refresh  |
|  - Sub-10ms Multi-Tier Context Retrieval Engine                          |
|  - Token-Budgeted Project Context Digest Generator (~1,410 tokens)       |
|  - Pure Python Project Root & Context Discovery (core/context.py)        |
|  - Preflight Listener Security Guards (guard_listener_overrides)         |
+------------------------------------+-------------------------------------+
                                     |
+------------------------------------v-------------------------------------+
|                     Adapters & Transport Layer                           |
|  - Streamable HTTP & SSE MCP Client (core/transport.py)                  |
|  - Strict Loopback Network Boundary Enforcement (127.0.0.1, ::1)         |
|  - Platform Adapters: Windows (CIM/Registry) & macOS (lsof/ps/bundles)   |
|  - Unreal Editor Lifecycle Orchestrator (adapters/unreal/lifecycle.py)   |
+------------------------------------+-------------------------------------+
                                     |
                         Loopback JSON-RPC 2.0
                       (http://127.0.0.1:8000/mcp)
                                     |
+------------------------------------v-------------------------------------+
|                    Unreal Engine Editor (5.8+)                           |
|  - Native ModelContextProtocol Plugin (Embedded HTTP Server & SSE)       |
|  - Native ToolsetRegistry Subsystem (53 Toolsets / 832 Tools)            |
|  - Native Engine Plugins: AllToolsets, LogsToolset, ActorTools, etc.    |
+--------------------------------------------------------------------------+
```

---

## 3. Subsystem Responsibilities

### 3.1 Unreal Engineering Core
The engineering core owns all engine interactions, session state, safety boundaries, and semantic intelligence:

1. **Session & Tool Discovery (`core/session.py`):**
   - Dispatches dynamic `list_toolsets` and `describe_toolset` requests.
   - Maintains an in-memory cached toolset catalog, fetching toolset schemas on demand.
   - Enforces two-factor project identity verification to prevent accidental execution against incorrect editor instances.
2. **Project Intelligence & Indexing (`core/indexing/` & `core/intelligence/`):**
   - **Persistent SQLite Database:** Caches asset metadata, actor hierarchies, and Blueprint structures with FTS5 full-text indexing.
   - **Incremental Refresh:** Tracks filesystem `mtime` and content hashes, skipping unchanged assets for sub-second re-indexing.
   - **Multi-Tier Search:** Scores queries across exact asset paths, actor names, classes, functions, and variables.
   - **Context Digest:** Synthesizes structured markdown summaries within tight token budgets (~1,400 tokens) for agent prompts.
3. **Asset Dependency Graph (`core/intelligence/project_dependencies.py`):**
   - Constructs directed graphs of project asset relationships.
   - Executes Tarjan's strongly connected components (SCC) algorithm to detect circular dependencies.
   - Calculates transitive closure and blast radius for asset modification or deletion.
4. **Blueprint AST & Mutation Engine (`core/blueprint/`):**
   - Tokenizes and parses Epic's native Blueprint graph S-expressions into AST hierarchies.
   - Calculates node cyclomatic complexity to identify refactoring targets.
   - Executes atomic mutation transactions guarded by `.mutation.lock` files, maintaining recovery journals and verifying post-mutation compiler state.
5. **Security & Preflight Guards (`core/configure.py`):**
   - Evaluates engine configuration before disk writes.
   - Rejects wildcard (`0.0.0.0`, `::`) and public IP bindings in `DefaultEngine.ini`.
   - Generates non-colliding test map namespaces (`/Game/AntigravityBridgeTests/...`) to protect user levels.

### 3.2 Adapters & Transport Layer
1. **MCP Transport (`core/transport.py`):**
   - Implements sequential JSON-RPC 2.0 over Streamable HTTP POST and Server-Sent Events (SSE).
   - Enforces strict loopback constraints: only `127.0.0.1` and `::1` are accepted. Redirects to remote endpoints are blocked.
   - Manages session headers (`Mcp-Session-Id`) and protocol version negotiation.
2. **Platform Abstraction (`adapters/platform/`):**
   - Isolates operating-system commands behind the `PlatformAdapter` ABC.
   - Windows Adapter: Uses PowerShell CIM (`Get-CimInstance Win32_Process`) and Windows Registry for engine discovery.
   - macOS Adapter: Uses `lsof`, `ps`, and macOS application bundle conventions.
3. **Editor Lifecycle (`adapters/unreal/lifecycle.py`):**
   - Orchestrates editor discovery, project preparation, process launch, and status monitoring.

### 3.3 Antigravity Integration Layer (Phased Delivery)
- Responsible for native Antigravity plugin manifest registration, skill catalog declarations, slash command integration, and prompt hook execution.
- Isolated from core code to ensure the core remains portable and clean.

---

## 4. Key Architectural Invariants

1. **Zero Runtime AI-Client Dependency:** No module in `core/` or `adapters/` may import or require an external AI client library (`codex`, `claude`, `openai`, `anthropic`).
2. **Python Standard Library Baseline:** All core modules run on Python 3.10+ standard library without requiring third-party pip packages.
3. **Strict Loopback Trust Boundary:** All socket connections and HTTP endpoints are strictly bound to local loopback interfaces.
4. **Safe Live Mutation Isolation:** Operations that alter level or actor state must verify project identity and use non-colliding namespaces during automated tests.
5. **Atomic Blueprint Mutations:** AST mutations must acquire process locks and preserve rollback journals.
