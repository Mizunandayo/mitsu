from mitsu.cognition.circuit_breaker import CircuitBreaker, CircuitState


def test_breaker_opens_after_failure_threshold() -> None:
    breaker = CircuitBreaker(failure_threshold=2, cooldown_seconds=30.0)

    breaker.record_failure(10.0)
    assert breaker.snapshot(10.0).state is CircuitState.CLOSED

    breaker.record_failure(11.0)
    assert breaker.snapshot(11.0).state is CircuitState.OPEN
    assert not breaker.allow_request(20.0)


def test_breaker_allows_one_probe_after_cooldown() -> None:
    breaker = CircuitBreaker(failure_threshold=1, cooldown_seconds=30.0)
    breaker.record_failure(10.0)

    assert not breaker.allow_request(39.9)
    assert breaker.allow_request(40.0)
    assert breaker.snapshot(40.0).state is CircuitState.HALF_OPEN


def test_success_closes_breaker_and_resets_failures() -> None:
    breaker = CircuitBreaker(failure_threshold=1, cooldown_seconds=30.0)
    breaker.record_failure(1.0)
    breaker.allow_request(31.0)

    breaker.record_success()

    snapshot = breaker.snapshot(31.0)
    assert snapshot.state is CircuitState.CLOSED
    assert snapshot.consecutive_failures == 0
