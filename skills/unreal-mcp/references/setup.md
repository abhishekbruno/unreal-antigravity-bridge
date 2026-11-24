# First-Time MCP Server Setup

Follow these steps to configure Unreal Engine 5.8+ to communicate via Model Context Protocol (MCP).

---

## 1. Enable Required Plugins in `.uproject`

Unreal Engine requires two native plugins to enable MCP tooling:
1. `ModelContextProtocol`: The embedded HTTP server and JSON-RPC 2.0 router.
2. `AllToolsets`: The aggregator exposing all 53 editor toolsets and 832 tools.

Open your project's `.uproject` file in a text editor. Add or update the `Plugins` array:

```json
{
  "FileVersion": 3,
  "EngineAssociation": "5.8",
  "Plugins": [
    {
      "Name": "ModelContextProtocol",
      "Enabled": true
    },
    {
      "Name": "AllToolsets",
      "Enabled": true
    }
  ]
}
```

*Note:* `AllToolsets` is disabled by default in engine builds and must be explicitly enabled.

---

## 2. Enable Server Auto-Start on Launch

By default, the MCP server does not start automatically. To ensure the server starts whenever the editor launches:

Add the following block to:
`<ProjectRoot>/Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini`
(Or `<ProjectRoot>/Config/DefaultEngine.ini` for project-wide defaults):

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
ServerPortNumber=8000
```

---

## 3. Strict Loopback Binding Configuration

To prevent exposing the unauthenticated editor port to local network interfaces, ensure loopback binding is set in `Config/DefaultEngine.ini`:

```ini
[HTTPServer.Listeners]
DefaultBindAddress=127.0.0.1
+ListenerOverrides=(Port=8000,BindAddress="127.0.0.1")
```

The preflight security guards in `unreal-antigravity-bridge` (`guard_listener_overrides`) will reject wildcard (`0.0.0.0`, `::`) or public network bindings.

---

## 4. Verification

1. Launch Unreal Editor with your project.
2. In the Output Log (`Window > Developer Tools > Output Log`), verify:
   ```
   LogModelContextProtocol: Display: MCP Server started on http://127.0.0.1:8000/mcp
   ```
3. Test connectivity with the diagnostic tool:
   ```bash
   python scripts/doctor.py --project /path/to/YourProject.uproject
   ```
