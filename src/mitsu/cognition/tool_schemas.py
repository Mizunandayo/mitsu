from __future__ import annotations

from typing import Final

SYSTEM_INSTRUCTIONS: Final = """
You are MITSU's bounded desktop reasoning layer.

You may only use the supplied window-management tools.
Never claim an action succeeded unless a tool result confirms it.
Never ask for or reveal secrets, API keys, file contents, clipboard contents,
network credentials, or private data.
Do not invoke read_screen unless the user's current request explicitly asks
to read, describe, or reason about visible screen content.
Prefer find_window before restore_window or move_window.
""".strip()


TOOLS: Final[list[dict[str, object]]] = [
    {
        "type": "function",
        "name": "find_window",
        "description": "Find one eligible top-level application window by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Application name or visible window-title fragment.",
                    "minLength": 1,
                    "maxLength": 100,
                }
            },
            "required": ["name"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "restore_window",
        "description": "Restore and focus a previously found application window.",
        "parameters": {
            "type": "object",
            "properties": {
                "handle": {
                    "type": "integer",
                    "minimum": 1,
                }
            },
            "required": ["handle"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "move_window",
        "description": "Move a window to the requested physical monitor direction.",
        "parameters": {
            "type": "object",
            "properties": {
                "handle": {
                    "type": "integer",
                    "minimum": 1,
                },
                "destination": {
                    "type": "string",
                    "enum": ["left", "right", "up", "down"],
                },
            },
            "required": ["handle", "destination"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]
