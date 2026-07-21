"""Tests for bounded runtime performance measurements."""

import pytest

from mitsu.observability.metrics import JitterMeter, RollingMetric


def test_rolling_metric_reports_percentiles() -> None:
    metric = RollingMetric(maximum_samples=10)

    for value in (1.0, 2.0, 3.0, 4.0, 5.0):
        metric.record(value)

    summary = metric.summary()

    assert summary is not None
    assert summary.count == 5
    assert summary.minimum == 1.0
    assert summary.maximum == 5.0
    assert summary.p50 == 3.0
    assert summary.p95 == pytest.approx(4.8)


def test_jitter_meter_measures_spatial_dispersion() -> None:
    meter = JitterMeter(maximum_samples=10)

    meter.record(raw_x=0.0, raw_y=0.0, filtered_x=1.0, filtered_y=1.0)
    meter.record(raw_x=2.0, raw_y=0.0, filtered_x=1.0, filtered_y=1.0)

    assert meter.raw_standard_deviation() == pytest.approx(1.0)
    assert meter.filtered_standard_deviation() == pytest.approx(0.0)
