"""Short-lived target retention for stable pinch-to-grip transitions."""

from __future__ import annotations

from typing import Generic, TypeVar

Target = TypeVar("Target")


class TargetLatch(Generic[Target]):
    """Retain the last valid target briefly while a pinch closes."""

    def __init__(self, grace_period_seconds: float) -> None:
        if grace_period_seconds <= 0.0:
            raise ValueError("grace_period_seconds must be positive")

        self._grace_period_seconds = grace_period_seconds
        self.clear()

    def resolve(
        self,
        live_target: Target | None,
        is_pinched: bool,
        timestamp_seconds: float,
    ) -> Target | None:
        """Return the live target or a fresh target retained during a pinch."""

        if live_target is not None:
            self._target = live_target
            self._timestamp_seconds = timestamp_seconds
            return live_target

        if (
            is_pinched
            and self._target is not None
            and self._timestamp_seconds is not None
            and timestamp_seconds - self._timestamp_seconds
            <= self._grace_period_seconds
        ):
            return self._target

        return None

    def clear(self) -> None:
        """Discard the retained target after grip completion or tracking loss."""

        self._target: Target | None = None
        self._timestamp_seconds: float | None = None
