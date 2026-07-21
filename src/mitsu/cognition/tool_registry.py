from __future__ import annotations

import json
from collections.abc import Callable

from pydantic import BaseModel, Field, ValidationError

from mitsu.control.window_manager import WindowManager


class FindWindowArguments(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class RestoreWindowArguments(BaseModel):
    handle: int = Field(gt=0)


class MoveWindowArguments(BaseModel):
    handle: int = Field(gt=0)
    destination: str = Field(pattern="^(left|right|up|down)$")


MoveToDestination = Callable[[int, str], bool]


class ToolRegistry:
    """Validates model tool calls before reaching OS window control."""

    def __init__(
        self,
        *,
        window_manager: WindowManager,
        move_to_destination: MoveToDestination,
    ) -> None:
        self._window_manager = window_manager
        self._move_to_destination = move_to_destination

    def execute(self, *, name: str, arguments_json: str) -> str:
        try:
            arguments = json.loads(arguments_json)
        except json.JSONDecodeError:
            return self._result(ok=False, message="Invalid tool arguments.")

        try:
            if name == "find_window":
                return self._find_window(FindWindowArguments.model_validate(arguments))

            if name == "restore_window":
                return self._restore_window(
                    RestoreWindowArguments.model_validate(arguments)
                )

            if name == "move_window":
                return self._move_window(MoveWindowArguments.model_validate(arguments))
        except ValidationError:
            return self._result(ok=False, message="Tool arguments failed validation.")

        return self._result(ok=False, message="Tool is not permitted.")

    def _find_window(self, arguments: FindWindowArguments) -> str:
        target = self._window_manager.find_window(arguments.name)

        if target is None:
            return self._result(ok=False, message="No eligible window found.")

        return self._result(
            ok=True,
            handle=target.handle,
            title=target.title,
        )

    def _restore_window(self, arguments: RestoreWindowArguments) -> str:
        target = self._window_manager.find_window_by_handle(arguments.handle)

        if target is None:
            return self._result(ok=False, message="Window is not eligible.")

        restored = self._window_manager.restore_and_focus(target.handle)
        return self._result(ok=True, handle=restored.handle, title=restored.title)

    def _move_window(self, arguments: MoveWindowArguments) -> str:
        target = self._window_manager.find_window_by_handle(arguments.handle)

        if target is None:
            return self._result(ok=False, message="Window is not eligible.")

        moved = self._move_to_destination(target.handle, arguments.destination)
        if not moved:
            return self._result(ok=False, message="Destination move was rejected.")

        return self._result(
            ok=True,
            handle=target.handle,
            destination=arguments.destination,
        )

    @staticmethod
    def _result(**payload: object) -> str:
        return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
