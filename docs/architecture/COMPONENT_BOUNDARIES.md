# Component Boundaries and Interface Contracts

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Document Version:** 1.0.0  
**Date:** 2026-11-24  

---

## 1. Overview

This document specifies the interface contracts, data models, error propagation mechanisms, and boundary invariants separating the subsystems within **Unreal Engine for Antigravity**.

---

## 2. Layer Contracts and Interfaces

### 2.1 MCP Transport Interface (`core/transport.py`)

The transport layer provides low-level JSON-RPC 2.0 framing over Streamable HTTP and SSE.

```python
class MCPClient:
    def __init__(self, endpoint: str = "http://127.0.0.1:8000/mcp", timeout: int = 30, client_name: str = "unreal-antigravity-bridge", client_version: str = "0.1.0"): ...
    def request(self, method: str, params: dict | None = None, notification: bool = False) -> dict | None: ...
    def initialize(self) -> dict: ...
    def tools(self) -> list[dict]: ...
    def call(self, name: str, arguments: dict) -> dict: ...
```

**Boundary Invariants:**
- **URL Validation:** `validate_endpoint` enforces that the URL scheme is strictly `http`, has no user/pass/query/fragment, has an explicit path, and resolves to a loopback IP address (`127.0.0.1` or `::1`).
- **Redirect Refusal:** Any 3xx HTTP redirect raised by the server triggers an immediate `MCPError` to prevent SSRF and endpoint hijacking.
- **Error Propagation:** All network failures, timeout errors, or malformed JSON payloads are wrapped and raised as `MCPError`.

---

### 2.2 Unreal Session Interface (`core/session.py`)

The session layer manages toolset discovery, schema caching, and two-factor project verification.

```python
class UnrealSession:
    def __init__(self, endpoint: str = "http://127.0.0.1:8000/mcp", project: Path | str | None = None, engine: Path | str | None = None, auto_connect: bool = False): ...
    def connect(self) -> UnrealSession: ...
    def load_toolset(self, toolset_name: str) -> dict: ...
    def tool(self, toolset_name: str, tool_name: str) -> tuple[dict, dict]: ...
    def invoke(self, toolset_name: str, tool_name: str, arguments: dict | None = None) -> Any: ...
```

**Boundary Invariants:**
- **Two-Factor Identity Verification:** Before any mutating call is authorized, the session verifies:
  1. Operating system process check: the listener on the target TCP port is an authentic `UnrealEditor` binary launched with the target `.uproject`.
  2. Telemetry verification: queries `LogsToolset.GetLogEntries` via MCP to verify the running project name matches.
- **Dynamic Toolset Loading:** In tool-search mode, calling `tool()` or `invoke()` automatically checks if the toolset is cached; if not, it queries `describe_toolset` on demand.
- **Argument Validation:** All arguments are checked against the tool's JSON schema (`type`, `required`, `properties`, `enum`) prior to network dispatch.

---

### 2.3 Platform Adapter Interface (`adapters/platform/base.py`)

The platform adapter decouples operating system differences from the engineering core.

```python
class PlatformAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def detect_os(self) -> dict: ...
    @abstractmethod
    def detect_architecture(self) -> str: ...
    @abstractmethod
    def discover_engine_installations(self) -> list[dict]: ...
    @abstractmethod
    def resolve_engine_root(self, explicit_engine: Path | None = None, project_path: Path | None = None) -> Path: ...
    @abstractmethod
    def resolve_editor_executable(self, engine_root: Path) -> Path: ...
    @abstractmethod
    def inspect_port_owner(self, port: int) -> int | None: ...
    @abstractmethod
    def find_running_editor_processes(self) -> list[dict]: ...
    @abstractmethod
    def verify_project_identity(self, port: int, project: Path, engine: Path | None = None) -> bool: ...
```

**Boundary Invariants:**
- Adapters must never execute commands with `shell=True`.
- On Windows, process inspection uses PowerShell CIM (`Get-CimInstance Win32_Process`) or `Get-Process`.
- On macOS, process inspection uses `lsof` and `ps -Ao`.

---

### 2.4 Context Discovery Interface (`core/context.py`)

Provides client-independent project marker detection, replacing legacy bash hooks.

```python
def is_project_root(directory: Path) -> bool: ...
def find_project_root(start_path: Path | str | None = None) -> Path | None: ...
def inspect_project_context(start_path: Path | str | None = None) -> dict: ...
def format_context_prompt(context: dict) -> str: ...
```

**Boundary Invariants:**
- Traverses upward from `$PWD` until a definitive marker (`.uproject`, `GenerateProjectFiles.*`) is encountered or the filesystem root is reached.
- Pure Python standard library implementation with zero shell dependencies.

---

### 2.5 Indexing and Retrieval Subsystem (`core/indexing/`)

1. **`ProjectIndexDB` (`core/indexing/project_index.py`):**
   - SQLite persistent database with FTS5 virtual tables (`fts_assets`, `fts_blueprint_elements`).
   - Tracks file modification times (`mtime`) and content SHA-256 hashes to enable sub-second incremental re-indexing.
2. **`ProjectIndexQuery` (`core/indexing/query_project_index.py`):**
   - Multi-tier retrieval engine executing scored queries: exact path match (weight 100) -> exact name match (weight 80) -> class/variable/function match (weight 60) -> FTS5 BM25 match.
3. **`generate_project_digest` (`core/indexing/generate_project_digest.py`):**
   - Compresses the project index into structured markdown within a strict token budget (~1,410 tokens).

---

### 2.6 Blueprint AST & Mutation Subsystem (`core/blueprint/`)

1. **`BlueprintParser` (`core/blueprint/blueprint_parser.py`):**
   - Tokenizes and parses Epic's S-expression Blueprint graph grammar into traversable AST nodes.
   - Calculates cyclomatic complexity based on conditional decision points (Branches, Switches, Loops).
2. **`BlueprintMutationRunner` (`core/blueprint/blueprint_mutation.py`):**
   - Guards mutations with atomic `.mutation.lock` files to prevent concurrent access.
   - Writes journaled backup files prior to mutation and provides automatic rollback upon failure.
3. **`BlueprintVerify` (`core/blueprint/blueprint_verify.py`):**
   - Verifies AST integrity and compiler status post-mutation.

---

## 3. Error Handling and Diagnostics Contract

| Exception Class | Originating Layer | Cause | Handling Policy |
| :--- | :--- | :--- | :--- |
| **`MCPError`** | `core/transport.py`, `core/session.py` | Network error, loopback violation, protocol failure, tool execution error | Raised to caller with structured diagnostic context |
| **`ValueError`** | `core/configure.py`, `adapters/platform/` | Unsafe listener override (0.0.0.0), invalid port, unsupported OS | Abort operation immediately before file writes |
| **`FileNotFoundError`** | `adapters/platform/`, `core/session.py` | Missing `.uproject`, absent engine executable | Report exact missing path and engine search roots |
| **`TimeoutError`** | `core/transport.py`, `adapters/unreal/lifecycle.py` | Editor launch or tool call exceeded timeout | Graceful abort; check editor process state |

---

## 4. Antigravity Integration Layer Boundary

The Antigravity Integration Layer will interact exclusively with the public interfaces of `core` and `adapters`.
- It **must not** bypass `core/session.py` to issue raw, unvalidated socket writes.
- It **must not** bypass `guard_listener_overrides` when configuring projects.
- It translates Antigravity slash commands and skill invocations into high-level calls on `UnrealSession`, `editor_lifecycle`, and `ProjectIndexQuery`.
