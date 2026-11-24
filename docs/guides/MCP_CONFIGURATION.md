# MCP Configuration Guide: Unreal Engine 5.8+

This guide describes how to configure, secure, and inspect Model Context Protocol (MCP) communication between Google Antigravity and Unreal Engine 5.8+.

---

## 1. Embedded MCP Server in Unreal Engine 5.8+

Unreal Engine 5.8 includes native support for MCP via two built-in plugins:
1. `ModelContextProtocol`: The embedded HTTP server and JSON-RPC router.
2. `AllToolsets`: The aggregator that registers 53 editor toolsets with the `ToolsetRegistry`.

### Enabling Plugins in `.uproject`
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

---

## 2. Server Auto-Start and Port Configuration

By default, the embedded MCP server does not start when the editor launches. Configure auto-start in `Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini` (per-user) or `Config/DefaultEngine.ini` (project-wide):

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
ServerPortNumber=8000
ServerUrlPath=/mcp
bEnableToolSearch=True
```

### Tool Search Setting (`bEnableToolSearch`)
- **`True` (Default & Strongly Recommended):** Exposes only meta-tools (`list_toolsets`, `describe_toolset`, `call_tool`). Dynamic tool search prevents flooding the LLM context window with 800+ tool signatures and maintains fast prompt caching.
- **`False`:** Flattens all 832 tools into global `tools/list`. Use only for automated schema generators.

---

## 3. Strict Loopback Binding Security

To prevent exposing unauthenticated editor RPC interfaces over local networks, enforce loopback binding in `Config/DefaultEngine.ini`:

```ini
[HTTPServer.Listeners]
DefaultBindAddress=127.0.0.1
+ListenerOverrides=(Port=8000,BindAddress="127.0.0.1")
```

The preflight guards in `core.configure.guard_listener_overrides` actively scan configuration files and reject wildcard bindings (`0.0.0.0`, `::`).

---

## 4. Antigravity MCP Client Configuration (`mcp_config.json`)

Antigravity discovers and connects to the server using the root `mcp_config.json`:

```json
{
  "mcpServers": {
    "unreal-mcp": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

### Stdio Forwarding Bridge (Optional)
If your environment requires standard I/O (Stdio) transport rather than direct HTTP sockets, use the included stdio forwarder:

```json
{
  "mcpServers": {
    "unreal-mcp-stdio": {
      "command": "python",
      "args": ["scripts/mcp_stdio_bridge.py", "http://127.0.0.1:8000/mcp"]
    }
  }
}
```

---

## 5. Multi-Editor Port and Identity Disambiguation

When running multiple editor instances concurrently:
1. Assign distinct ports per editor (e.g., `-ModelContextProtocolPort=8001`).
2. Update the corresponding `mcp_config.json` with the matching port.
3. The bridge performs two-factor project verification (`adapters.platform.verify_project_identity`) to ensure commands only target the intended project.
