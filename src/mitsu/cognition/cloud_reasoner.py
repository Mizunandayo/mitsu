from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Protocol

from openai import OpenAI

from mitsu.cognition.circuit_breaker import CircuitBreaker, CircuitState
from mitsu.cognition.tool_registry import ToolRegistry
from mitsu.cognition.tool_schemas import SYSTEM_INSTRUCTIONS, TOOLS
from mitsu.config import CloudSettings


@dataclass(frozen=True)
class ReasoningResult:
    available: bool
    message: str
    used_cloud: bool = False


class Reasoner(Protocol):
    def resolve(self, command: str) -> ReasoningResult:
        """Resolve one explicit, out-of-grammar command."""


class DisabledReasoner:
    """Offline-safe replacement. It never creates a network client."""

    def resolve(self, command: str) -> ReasoningResult:
        del command
        return ReasoningResult(
            available=False,
            message="Cloud reasoning is unavailable. Use a supported command.",
        )


class OpenAIReasoner:
    def __init__(
        self,
        *,
        settings: CloudSettings,
        tool_registry: ToolRegistry,
        api_key: str,
    ) -> None:
        self._settings = settings
        self._tool_registry = tool_registry
        self._client = OpenAI(
            api_key=api_key,
            timeout=settings.timeout_seconds,
            max_retries=0,
        )
        self._breaker = CircuitBreaker(
            failure_threshold=settings.failure_threshold,
            cooldown_seconds=settings.cooldown_seconds,
        )

    @classmethod
    def from_environment(
        cls,
        *,
        settings: CloudSettings,
        tool_registry: ToolRegistry,
    ) -> Reasoner:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()

        if not settings.enabled or not api_key:
            return DisabledReasoner()

        return cls(
            settings=settings,
            tool_registry=tool_registry,
            api_key=api_key,
        )

    def resolve(self, command: str) -> ReasoningResult:
        now = time.monotonic()

        if not self._breaker.allow_request(now):
            snapshot = self._breaker.snapshot(now)
            return ReasoningResult(
                available=False,
                message=(
                    "Cloud reasoning is cooling down "
                    f"({snapshot.retry_after_seconds:.0f}s remaining)."
                ),
            )

        try:
            response = self._client.responses.create(
                model=self._settings.model,
                store=False,
                instructions=SYSTEM_INSTRUCTIONS,
                input=command,
                tools=TOOLS,
                tool_choice="auto",
            )

            tool_rounds = 0
            input_items: list[object] = list(response.output)

            while True:
                function_calls = [
                    item
                    for item in response.output
                    if getattr(item, "type", None) == "function_call"
                ]

                if not function_calls:
                    break

                tool_rounds += 1
                if tool_rounds > self._settings.maximum_tool_rounds:
                    raise RuntimeError("Maximum tool rounds exceeded.")

                for call in function_calls:
                    output = self._tool_registry.execute(
                        name=call.name,
                        arguments_json=call.arguments,
                    )
                    input_items.append(
                        {
                            "type": "function_call_output",
                            "call_id": call.call_id,
                            "output": output,
                        }
                    )

                response = self._client.responses.create(
                    model=self._settings.model,
                    store=False,
                    instructions=SYSTEM_INSTRUCTIONS,
                    input=input_items,
                    tools=TOOLS,
                    tool_choice="auto",
                )
                input_items.extend(response.output)

        except Exception:
            self._breaker.record_failure(time.monotonic())
            return ReasoningResult(
                available=False,
                message="Cloud reasoning failed; local controls remain active.",
            )

        self._breaker.record_success()
        return ReasoningResult(
            available=True,
            message=response.output_text or "Command completed.",
            used_cloud=True,
        )

    def circuit_state(self) -> CircuitState:
        return self._breaker.snapshot(time.monotonic()).state
