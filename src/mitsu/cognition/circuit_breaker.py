from __future__ import annotations

import threading
from dataclasses import dataclass
from enum import StrEnum


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass(frozen=True)
class CircuitSnapshot:
    state: CircuitState
    consecutive_failures: int
    retry_after_seconds: float | None


class CircuitBreaker:
    """Fail closed after repeated cloud failures, then recover cautiously"""

    def __init__(
        self,
        *,
        failure_threshold: int,
        cooldown_seconds: float,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be at least one.")
        if cooldown_seconds <= 0.0:
            raise ValueError("cooldown_seconds must be positive")

        self._failure_threshold = failure_threshold
        self._cooldown_seconds = cooldown_seconds
        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._opened_at: float | None = None
        self._lock = threading.Lock()

    def allow_request(self, now_seconds: float) -> bool:
        with self._lock:
            if self._state is CircuitState.CLOSED:
                return True

            if self._state is CircuitState.HALF_OPEN:
                return True

            if self._opened_at is None:
                return False

            elapsed = now_seconds - self._opened_at
            if elapsed < self._cooldown_seconds:
                return False

            self._state = CircuitState.HALF_OPEN
            return True

    def record_success(self) -> None:
        with self._lock:
            self._state = CircuitState.CLOSED
            self._consecutive_failures = 0
            self._opened_at = None

    def record_failure(self, now_seconds: float) -> None:
        with self._lock:
            self._consecutive_failures += 1

            if self._state is CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
                self._opened_at = now_seconds
                return

            if self._consecutive_failures >= self._failure_threshold:
                self._state = CircuitState.OPEN
                self._opened_at = now_seconds

    def snapshot(self, now_seconds: float) -> CircuitSnapshot:
        with self._lock:
            retry_after_seconds: float | None = None

            if self._state is CircuitState.OPEN and self._opened_at is not None:
                elapsed = now_seconds - self._opened_at
                retry_after_seconds = max(0.0, self._cooldown_seconds - elapsed)

            return CircuitSnapshot(
                state=self._state,
                consecutive_failures=self._consecutive_failures,
                retry_after_seconds=retry_after_seconds,
            )
