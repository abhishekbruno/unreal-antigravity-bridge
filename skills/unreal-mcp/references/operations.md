# Operations: Console Commands, Settings, Recovery

Read this document when troubleshooting MCP connectivity issues (missing tools, port collisions, stale tool registries, or proxy reconnects).

---

## 1. Unreal Editor Console Commands

Execute these commands from the Unreal Editor console (`~` key):

| Command | Description and Purpose |
| :--- | :--- |
| `ModelContextProtocol.StartServer [port]` | Start the embedded MCP HTTP listener. Pass an optional port argument to override default `8000`. |
| `ModelContextProtocol.StopServer` | Stop the MCP server. Useful to clear hung sockets or force a clean listener reboot. |
| `ModelContextProtocol.RefreshTools` | Force the `ToolsetRegistry` to re-scan and register all available toolsets. Run this after enabling new plugins. |
| `ModelContextProtocol.GenerateClientConfig <client>` | Regenerate per-client configuration. Supported arguments: `ClaudeCode`, `Cursor`, `VSCode`, `Gemini`, `Codex`, `All`. |

---

## 2. Tool-Search Mode Configuration

The MCP server supports two modes for `tools/list`, controlled by `bEnableToolSearch` on `UModelContextProtocolSettings`:

- **`True` (Default / Recommended):** `tools/list` returns only the meta-tools: `list_toolsets`, `describe_toolset`, and `call_tool`. Tools are dispatched dynamically. Context window overhead remains minimal and prompt caching stays stable.
- **`False`:** Every individual tool across all 53 toolsets is registered upfront at startup as a separate MCP tool. Useful for automated hash-mapping commandlets.

To configure in `DefaultEngine.ini` or `EditorPerProjectUserSettings.ini`:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bEnableToolSearch=True
```

---

## 3. Proxy Recovery & Lifecycle

When using Epic's optional `unreal_mcp_proxy` (`Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy`):
- The proxy maintains the client-side MCP session open even if the Unreal Editor restarts or crashes.
- `unreal_mcp_status` reports whether the proxy holds an active upstream session to Unreal.
- If Unreal crashes, the proxy exposes `unreal_mcp_status`. Once Unreal restarts, the proxy reconnects and emits `notifications/tools/list_changed`.
- A connected proxy does not prove that live editor calls will succeed. Always verify reachability with a read-only query (such as querying current level actors).

---

## 4. Multi-Editor Port & Identity Disambiguation

When running multiple editor instances:
1. Assign each instance a distinct port via console: `ModelContextProtocol.StartServer 8001` or command line argument: `-ModelContextProtocolPort=8001`.
2. Inspect editor process metadata in the `initialize` response under `_meta["com.epicgames.unrealengine/instance"]`:
   - `processId`
   - `projectName`
   - `projectFile`
   - `engineVersion`
3. Cross-reference the port owner PID using the platform adapter before authorizing scene mutations.
