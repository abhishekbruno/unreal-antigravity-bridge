"""Unreal Engine for Antigravity — Core Engineering Architecture.

Provides AI-client-independent Unreal Engine 5.8+ session management,
Model Context Protocol (MCP) streamable HTTP/SSE transport, project context
discovery, asset dependency analysis, SQLite persistent indexing, and Blueprint AST mutation.
"""

from core.transport import Client, MCPClient, MCPError, validate_endpoint, content
from core.session import UnrealSession, parse_toolsets, validate_inputs, verify_process_identity, listener_identity
from core.context import find_project_root, inspect_project_context, format_context_prompt

__all__ = [
    "Client",
    "MCPClient",
    "MCPError",
    "validate_endpoint",
    "content",
    "UnrealSession",
    "parse_toolsets",
    "validate_inputs",
    "verify_process_identity",
    "listener_identity",
    "find_project_root",
    "inspect_project_context",
    "format_context_prompt",
]

__version__ = "0.1.0"
