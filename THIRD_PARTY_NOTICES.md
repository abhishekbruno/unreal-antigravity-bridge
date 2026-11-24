# Third-Party Notices and Attribution

This project, **Unreal Engine for Antigravity** (`unreal-antigravity-bridge`), incorporates and consolidates components derived from upstream open-source projects licensed under the MIT License.

---

## 1. Unreal Codex Bridge

- **Original Project:** `unreal-codex-bridge` (`unreal-codex-bridge-main`)
- **Original Copyright:** Copyright (c) 2026 Epic Games, Inc.
- **License:** MIT License
- **License Text:**

```
MIT License

Copyright (c) 2026 Epic Games, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- **Derived Components:**
  - Transport and JSON-RPC 2.0 loopback communication (`scripts/bridge_mcp.py`, `core/transport.py`)
  - Unreal session management, process identity verification, and dynamic tool discovery (`scripts/unreal_session.py`, `core/session.py`)
  - Platform abstraction adapters for Windows and macOS (`scripts/platform_adapter/`, `adapters/platform/`)
  - Cross-platform editor lifecycle manager (`scripts/editor_lifecycle.py`, `adapters/unreal/lifecycle.py`)
  - Configuration manager and listener security preflight guards (`scripts/configure.py`)
  - Diagnostics and system verification engine (`scripts/doctor.py`)
  - Project introspection, asset scanning, and Blueprint AST extraction (`scripts/inspect_project.py`)
  - Asset dependency DAG builder, Tarjan's SCC cycle detector, and blast radius analyzer (`scripts/project_dependencies.py`)
  - SQLite persistent index engine with FTS5 and incremental tracking (`scripts/project_index.py`)
  - Multi-tier deterministic context retrieval engine (`scripts/query_project_index.py`)
  - Token-budgeted project digest generator (`scripts/generate_project_digest.py`)
  - S-expression tokenizer, recursive-descent AST parser, and cyclomatic complexity calculator (`scripts/blueprint_parser.py`)
  - Declarative Blueprint authoring DSL specification (`scripts/blueprint_spec.py`)
  - Blueprint code generator and AST mutation engine (`scripts/blueprint_codegen.py`, `scripts/blueprint_mutation.py`, `scripts/blueprint_verify.py`)
  - Play-In-Editor (PIE) test runner and runtime log harvester (`scripts/playtest.py`)
  - Five-Star collection game benchmark suite (`benchmarks/five_star_game/`)
  - Associated automated unit test suites (`tests/`)

---

## 2. Unreal Engine Skills for Claude Code Plugin

- **Original Project:** `unreal-engine-skills-for-claude-code-plugin` (`unreal-engine-skills-for-claude-code-plugin-main`)
- **Original Copyright:** Copyright (c) 2026 Epic Games, Inc.
- **License:** MIT License
- **License Text:**

```
MIT License

Copyright (c) 2026 Epic Games, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- **Derived Components:**
  - Comprehensive operational guidelines, recovery procedures, and console commands (`skills/unreal-mcp/references/operations.md`, `skills/unreal-mcp/references/setup.md`)
  - Detailed toolset discovery workflow and asset conventions (`skills/unreal-mcp/SKILL.md`)
  - Session startup context inspection heuristics and project marker detection (`hooks/unreal-context.sh`, refactored into client-independent Python context provider)
