# Baseline Test and Verification Report

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Phase:** ARC 01 — Phase 01: Repository Audit and Core Consolidation  
**Audit Date:** 2026-11-24  
**Test Environment:**
- **OS:** Windows 11 Enterprise (win32)
- **Python Version:** 3.12.10 (Standard Library only)
- **Test Runner:** pytest 8.4.2 (Pluggy 1.6.0)
- **Execution Mode:** Isolated execution; zero modifications to source repositories; cache and JUnit XML isolated in scratch directory.

---

## 1. Executive Summary

Prior to performing any refactoring or code consolidation, a rigorous baseline test run was executed on both source repositories.

- **`unreal-codex-bridge-main`:** Contained 20 automated unit test modules comprising **142 individual test cases**. The entire test suite was executed in an isolated environment, achieving a **100% pass rate** (**142 passed, 0 failed, 0 errors, 0 skipped**) with a recorded execution time of **7.13 seconds wall clock** (6.556 seconds cumulative test duration). Zero pre-existing failures were detected.
- **`unreal-engine-skills-for-claude-code-plugin-main`:** Contained **0 automated tests**. No test execution could be conducted for this repository.

---

## 2. Test Environment Requirements

### 2.1 Python Runtime
- **Supported Runtime:** Python 3.10, 3.11, 3.12+
- **Host Runtime Verified:** Python 3.12.10 (`C:\Users\zone\AppData\Local\Programs\Python\Python312\python.exe`)
- **Runtime Dependencies:** **Zero external packages required.** All core modules rely strictly on Python's built-in standard library (`http.client`, `socket`, `sqlite3`, `json`, `hashlib`, `ipaddress`, `tomllib`, `pathlib`, `unittest`).
- **Test Dependencies:** `pytest` (standard test runner; tests are authored using standard `unittest.TestCase`).

---

## 3. Baseline Test Execution Results

### 3.1 Summary Metrics

| Metric | Result |
| :--- | :--- |
| **Total Test Suites** | 20 test files (21 test classes) |
| **Total Test Cases Collected** | 142 |
| **Tests Passed** | **142 (100.0%)** |
| **Tests Failed** | **0 (0.0%)** |
| **Tests Errored** | **0 (0.0%)** |
| **Tests Skipped** | **0 (0.0%)** |
| **Cumulative Test Duration (XML)** | **6.556 seconds** |
| **Total Test Run Wall-Clock Time** | **7.13 seconds** |
| **Pre-existing Failures** | **None** |

---

### 3.2 Per-Module Execution Breakdown

Data extracted directly from the verified baseline JUnit XML run:

| Test Module | Test Class | Tests | Passed | Failed | Skipped | Duration | Primary Verification Scope |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `test_blueprint_authoring.py` | `SpecTests` | 18 | 18 | 0 | 0 | 0.022s | Declarative DSL validation, pins, cycles, connections, syntax |
| `test_blueprint_mutation.py` | `SafetyTests` | 4 | 4 | 0 | 0 | 0.011s | Mutation safety, dry runs, file lock checks |
| `test_blueprint_mutation.py` | `GraphVerificationTests` | 10 | 10 | 0 | 0 | 0.552s | Mutation journaling, backlink checks, rollback, compile errors |
| `test_blueprint_parser.py` | `TestBlueprintParser` | 5 | 5 | 0 | 0 | 0.005s | S-expression tokenizer, AST parsing, cyclomatic complexity |
| `test_bridge.py` | `ProtocolTests` | 8 | 8 | 0 | 0 | 0.007s | MCP JSON-RPC 2.0 protocol, error codes, URL normalization |
| `test_configure.py` | `ConfigurationTests` | 8 | 8 | 0 | 0 | 0.123s | Listener security preflights, wildcard rejection, INI parser |
| `test_dependencies.py` | `TestAssetDependencyGraph`| 8 | 8 | 0 | 0 | 0.009s | Asset DAG builder, Tarjan's SCC cycles, blast radius impact |
| `test_diagnostics.py` | `DiagnosticTests` | 9 | 9 | 0 | 0 | 0.090s | Exit codes, engine build check, dynamic toolset loading, schemas |
| `test_digest.py` | `TestProjectDigest` | 4 | 4 | 0 | 0 | 0.355s | Token-budgeted project digest generator and markdown formatting |
| `test_editor_lifecycle.py` | `EditorLifecycleTests` | 5 | 5 | 0 | 0 | 0.042s | Cross-platform lifecycle CLI (detect, prepare, launch, status) |
| `test_inspect_project.py` | `TestInspectProject` | 7 | 7 | 0 | 0 | 0.009s | Scene inspection, actor/component extraction, Blueprint variables |
| `test_install.py` | `InstallerTests` | 4 | 4 | 0 | 0 | 0.149s | Installer plugin backup, marketplace entry, INI autostart |
| `test_live_guards.py` | `LiveGuardTests` | 3 | 3 | 0 | 0 | 0.003s | Level duplication guards, non-colliding test map naming |
| `test_macos_adapter.py` | `MacOSAdapterTests` | 7 | 7 | 0 | 0 | 0.067s | macOS `lsof` listener detection, `ps` inspection, bundle resolution |
| `test_platform_detect.py` | `PlatformDetectTests` | 6 | 6 | 0 | 0 | 0.006s | Platform detection factory, OS identification, unsupported OS |
| `test_playtest.py` | `PlaytestTests` | 3 | 3 | 0 | 0 | 0.041s | PIE test flow, project log file discovery, error harvesting |
| `test_plugin_packaging.py` | `PluginPackagingTests` | 4 | 4 | 0 | 0 | 0.010s | Plugin manifests, marketplace schemas, skill YAML frontmatter |
| `test_project_index.py` | `TestProjectIndexDB` | 7 | 7 | 0 | 0 | 0.426s | Persistent SQLite index, FTS5 full-text search, schema, mtime |
| `test_query_index.py` | `TestProjectIndexQuery` | 9 | 9 | 0 | 0 | 0.682s | Multi-tier context retrieval, ranking, search by class/var/func |
| `test_transport.py` | `TransportTests` | 6 | 6 | 0 | 0 | 3.858s | Real loopback HTTP & SSE sockets, session headers, redirect block |
| `test_windows_adapter.py` | `WindowsAdapterTests` | 7 | 7 | 0 | 0 | 0.089s | Windows CIM process inspection, Registry discovery, executable check |
| **Total** | | **142** | **142** | **0** | **0** | **6.556s** | **100.0% Pass Rate** |

---

## 4. Test Harness and Dependency Characterization

### 4.1 Mocked vs. Real Integration Tests
An automated AST and harness inspection of all 20 test modules revealed the following breakdown:
- **Pure Algorithmic & Unit Tests (No Mocks, No I/O):**
  - `test_blueprint_authoring.py`, `test_blueprint_parser.py`, `test_dependencies.py`, `test_bridge.py`, `test_live_guards.py`.
  - Execute in memory in under 0.05s total.
- **Real Integration Tests (Real I/O, Real Sockets, Real Databases):**
  - `test_transport.py`: Spawns **real local TCP loopback servers** using standard library `http.server.ThreadingHTTPServer` on ephemeral ports. Validates live HTTP POST, SSE streaming, header pagination, and rejection of 302 redirects to remote endpoints.
  - `test_project_index.py` & `test_query_index.py`: Instantiates **real SQLite databases with FTS5** in temporary files, testing real SQL transactions, triggers, full-text tokenizers, and schema migrations.
  - `test_configure.py`: Writes and parses real INI files and JSON files in temporary test directories.
- **Mocked System Tests:**
  - `test_windows_adapter.py`, `test_macos_adapter.py`, `test_editor_lifecycle.py`, `test_diagnostics.py`: Mock host subprocess calls (e.g. `lsof`, `Get-CimInstance`, `UnrealEditor.exe`) allowing Windows adapter tests to pass on macOS and macOS adapter tests to pass on Windows without live OS dependencies.

### 4.2 External Software Requirements
- **Live Unreal Editor Requirement:** **0 of the 142 tests require a running Unreal Editor.** All live editor interactions are isolated in the separate script `scripts/live_test.py` for manual/CI end-to-end verification.
- **External AI Client Requirement:** **0 of the 142 tests require an external Codex or Claude binary to actually run.** Tests that verify binary resolution use mocked PATH lookups.

---

## 5. Verification Conclusion

The baseline established by `unreal-codex-bridge-main` is exceptionally stable:
- 142 passing tests with 0 failures or errors.
- Fast execution (~7s).
- Zero external runtime package dependencies.
- Clear separation between unit logic and live editor integration.

This verified baseline serves as the gold standard for regression verification during our core consolidation in Stage F and Stage H.
