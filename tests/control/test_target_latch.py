from __future__ import annotations

from mitsu.control.target_latch import TargetLatch


def test_live_target_is_returned_and_retained() -> None:
    latch = TargetLatch[str](grace_period_seconds=0.18)

    target = latch.resolve("VS Code", is_pinched=False, timestamp_seconds=1.0)

    assert target == "VS Code"


def test_recent_target_is_available_only_while_pinched() -> None:
    latch = TargetLatch[str](grace_period_seconds=0.18)
    latch.resolve("VS Code", is_pinched=False, timestamp_seconds=1.0)

    assert latch.resolve(None, is_pinched=True, timestamp_seconds=1.1) == "VS Code"
    assert latch.resolve(None, is_pinched=False, timestamp_seconds=1.1) is None


def test_expired_target_is_not_reused() -> None:
    latch = TargetLatch[str](grace_period_seconds=0.18)
    latch.resolve("VS Code", is_pinched=False, timestamp_seconds=1.0)

    assert latch.resolve(None, is_pinched=True, timestamp_seconds=1.19) is None


def test_clear_discards_target_immediately() -> None:
    latch = TargetLatch[str](grace_period_seconds=0.18)
    latch.resolve("VS Code", is_pinched=False, timestamp_seconds=1.0)
    latch.clear()

    assert latch.resolve(None, is_pinched=True, timestamp_seconds=1.01) is None
