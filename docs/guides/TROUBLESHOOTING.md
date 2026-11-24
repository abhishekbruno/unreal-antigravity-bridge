# Troubleshooting Guide: Unreal Engine for Antigravity

This guide covers common diagnostic procedures and remedies for issues encountered when integrating Google Antigravity with Unreal Engine 5.8+.

---

## 1. Diagnostics with `scripts/doctor.py`

Always start diagnosis with the preflight doctor tool:

```bash
python scripts/doctor.py --project "/path/to/MyGame.uproject" --engine "/path/to/UE_5.8"
```

The tool performs 7 key health checks:
1. `python`: Python version compatibility (>= 3.10).
2. `antigravity_cli`: Google Antigravity CLI executable availability.
3. `project_and_plugins`: Target `.uproject` validity and enabled plugins (`ModelContextProtocol`, `AllToolsets`).
4. `engine`: Unreal Engine 5.8 version and executable presence.
5. `mcp_configuration`: Valid `mcp_config.json` endpoint registration.
6. `loopback_endpoint`: Loopback IP security compliance.
7. `tcp`: Port 8000 socket reachability.

---

## 2. Common Issues and Resolutions

### Issue 1: "No process listening on port 8000"
- **Cause:** Unreal Editor is not running or auto-start is disabled.
- **Remedy:**
  1. Open Unreal Editor with your project.
  2. Press the tilde (`~`) key in the editor to open the console.
  3. Run: `ModelContextProtocol.StartServer 8000`.
  4. To make permanent, run `python scripts/install.py --project "/path/to/MyGame.uproject"`.

### Issue 2: "Process on port 8000 does not match target project"
- **Cause:** Another Unreal project or stale editor process is bound to port 8000.
- **Remedy:**
  1. Check running processes: `python scripts/editor_lifecycle.py status --port 8000`.
  2. Close the other editor instance or assign a distinct port in the active editor console: `ModelContextProtocol.StartServer 8001`.
  3. Update `mcp_config.json` to target port 8001.

### Issue 3: Antigravity reports "Server unreal-mcp unreachable"
- **Cause:** Antigravity cannot connect to `http://127.0.0.1:8000/mcp`.
- **Remedy:**
  1. Test socket reachability using PowerShell: `Test-NetConnection -ComputerName 127.0.0.1 -Port 8000`.
  2. Check editor Output Log for `LogModelContextProtocol: Display: MCP Server started on http://127.0.0.1:8000/mcp`.
  3. Verify `DefaultEngine.ini` has `DefaultBindAddress=127.0.0.1`.

### Issue 4: Tools not found in global tool list
- **Cause:** Normal behavior. Unreal Engine 5.8 uses dynamic Tool Search (`bEnableToolSearch=True`).
- **Remedy:**
  - Antigravity queries `list_toolsets` and `describe_toolset` dynamically. Do not expect 800+ tools to appear upfront.

### Issue 5: Hook injection not appearing in conversation
- **Cause:** Working directory or workspace path was not recognized as an Unreal project.
- **Remedy:**
  - Verify that `MyGame.uproject` is present in the workspace root or parent directory.
  - Test hook manually: `echo '{"workspacePaths": ["/path/to/project"]}' | python core/context.py --hook`.
