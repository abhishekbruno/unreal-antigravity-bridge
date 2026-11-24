# Unreal Engine Development Rules for Google Antigravity

When working within an Unreal Engine workspace or communicating with an active Unreal Editor instance:

## 1. Toolset Usage and Discovery
- Unreal Engine 5.8+ uses dynamic Tool Search. The MCP server advertises meta-tools: `list_toolsets`, `describe_toolset`, and `call_tool`.
- Do not guess or fabricate tool names or arguments. Always discover toolsets via `list_toolsets` and inspect parameter schemas using `describe_toolset`.
- Dispatch operations via `call_tool` specifying `toolset_name`, `tool_name`, and validated arguments.
- Refer to the `unreal-mcp` skill for comprehensive execution guidance.

## 2. Operational Safety
- Verify project identity before issuing mutations. Confirm that the listening editor process belongs to the designated `.uproject`.
- Save assets promptly using `AssetTools.save_asset` after modifications.
- Never modify engine files under `/Engine/`. Confine all authoring to the project's `/Game/` directory.
- Avoid modifying assets or level actors while Play-In-Editor (PIE) is running.

## 3. C++ and Blueprint Conventions
- Adhere to Unreal Engine naming conventions: prefix `A` for Actors, `U` for UObjects, `F` for structs, `E` for enums, `I` for interfaces.
- Prefer Unreal Engine reflection macros (`UPROPERTY`, `UFUNCTION`, `UCLASS`, `USTRUCT`).
- When compiling code, use `LiveCodingToolset.CompileLiveCoding` and await completion before issuing further mutations.
