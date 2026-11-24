# Project Roadmap — Unreal Engine for Antigravity

**Project:** Unreal Engine for Antigravity (`unreal-antigravity-bridge`)  
**Current Milestone:** **ARC 01 — Phase 02: Native Antigravity Packaging and Skill Activation (COMPLETE)**  
**Target Engine Target:** Unreal Engine 5.8+ (Verified against UE 5.8.4 CL 58902052)  
**Primary AI Client:** Google Antigravity  

---

## Roadmap Progression Overview

```
[ARC 01: Stabilization & Core]
  ├── Phase 01: Repository Audit and Core Consolidation       [COMPLETE]
  ├── Phase 02: Antigravity Native Packaging & Skills         [COMPLETE]
  └── Phase 03: Live Handshake & PIE Verification             [NEXT / PLANNED]

[ARC 02: Project Intelligence & Blueprint Engine]
  ├── Phase 01: Linux Platform Adapter & Headless CI         [ROADMAP]
  ├── Phase 02: Advanced Asset Graph Traversal & Refactoring  [ROADMAP]
  └── Phase 03: Declarative Blueprint AST Codegen (Resumed)   [PAUSED / ROADMAP]

[ARC 03: Multi-Agent Production & Benchmarks]
  ├── Phase 01: Five-Star Game Autonomous Production Pipeline [PLANNED]
  └── Phase 02: Real-time Assistant Integration (UE 5.9+ ACP) [FUTURE]
```

---

## Milestone Details

### ARC 01 — Foundation and Antigravity Enablement

#### Phase 01: Repository Audit and Core Consolidation
- **Status:** **COMPLETE** (2026-11-24)
- **Tag:** `v0.1.0-alpha.1`
- **Deliverables:**
  - Full static and dynamic audit of `unreal-codex-bridge-main` and `unreal-engine-skills-for-claude-code-plugin-main`.
  - Established standalone repository `unreal-antigravity-bridge` with MIT licensing and source attribution.
  - Extracted client-independent core (`core/transport.py`, `core/session.py`, `core/context.py`, `core/indexing/`, `core/intelligence/`, `core/blueprint/`).
  - Completed audit, architecture, and migration documentation suites.
  - 148 automated unit tests (100% passing).

#### Phase 02: Antigravity Native Packaging and Skill Activation
- **Status:** **COMPLETE** (2026-11-24)
- **Deliverables:**
  - Native Antigravity plugin manifest (`plugin.json`), vector logo (`assets/logo.svg`), and suggested prompts.
  - Native Streamable HTTP MCP configuration (`mcp_config.json`) and Stdio forwarder (`scripts/mcp_stdio_bridge.py`).
  - Native lifecycle hooks (`hooks.json`) executing `core/context.py --hook` with `SessionStart` context injection.
  - Antigravity developer rules in `rules/AGENTS.md`.
  - Elimination of all legacy Codex/Claude manifests and directories (`.codex-plugin/`, `.agents/plugins/marketplace.json`, `AGENTS.unreal-codex.md`, `mcp.json`, `.mcp.json`).
  - Antigravity CLI plugin validation passing strictly (`agy plugin validate . --strict`).
  - Expanded test suite from 148 to **155 automated unit tests (100% passing)**.
  - Comprehensive user guides: Installation, MCP Configuration, Skill Usage, Troubleshooting.

#### Phase 03: Live Handshake and PIE Verification
- **Status:** **NEXT / PLANNED**
- **Objectives:**
  - Validate live loopback connection to active Unreal Engine 5.8.4 editor from Antigravity.
  - Execute end-to-end safe level duplication, actor spawning, and persistence tests.
  - Execute automated Play-In-Editor (PIE) test runs with runtime log harvesting.

---

### ARC 02 — Project Intelligence and Blueprint Engine

#### Phase 01: Linux Platform Adapter & Headless CI
- **Objectives:** Implement Linux `/proc` and `ss` process inspection in `adapters/platform/linux.py`. Enable headless containerized verification.

#### Phase 02: Advanced Asset Graph Traversal & Refactoring
- **Objectives:** Expand `project_dependencies.py` to support automated asset rename impact calculations and dependency breaking prevention.

#### Phase 03: Declarative Blueprint AST Codegen
- **Objectives:** Resume development on autonomous Blueprint graph generation from declarative DSL specs, compiling graphs directly via editor MCP tools.

---

### ARC 03 — Multi-Agent Production & Benchmarks

#### Phase 01: Five-Star Game Autonomous Production Pipeline
- **Objectives:** Run the Five-Star Game Benchmark end-to-end using Google Antigravity agents, evaluating against `acceptance.json` criteria.

#### Phase 02: Real-time Assistant Integration (UE 5.9+ ACP)
- **Objectives:** Adapt core tools to interface with Unreal Assistant in UE 5.9 via Agent Client Protocol (ACP).
