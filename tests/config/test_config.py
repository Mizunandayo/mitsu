from __future__ import annotations

import pytest
from pydantic import ValidationError

from mitsu.config import Settings


def test_valid_day_two_configuration_is_accepted() -> None:
    settings = Settings.model_validate(
        {
            "gesture": {
                "movement_gain": 1800.0,
                "minimum_delta_pixels": 1.0,
                "pinch": {
                    "engage_ratio": 0.34,
                    "release_ratio": 0.46,
                },
                "velocity": {
                    "smoothing_alpha": 0.25,
                    "activation_speed": 0.35,
                    "maximum_gain_multiplier": 2.5,
                },
            },
            "filter": {
                "minimum_cutoff_hz": 1.2,
                "beta": 0.015,
                "derivative_cutoff_hz": 1.0,
            },
            "window": {
                "single_monitor_only": False,
                "require_monitor_consistency": True,
            },
        }
    )

    assert settings.window.single_monitor_only is False


def test_unknown_config_keys_fail_closed() -> None:
    with pytest.raises(ValidationError, match="extra_forbidden"):
        Settings.model_validate(
            {
                "gesture": {
                    "movement_gain": 1800.0,
                    "minimum_delta_pixels": 1.0,
                    "unexpected_key": True,
                    "pinch": {
                        "engage_ratio": 0.34,
                        "release_ratio": 0.46,
                    },
                    "velocity": {
                        "smoothing_alpha": 0.25,
                        "activation_speed": 0.35,
                        "maximum_gain_multiplier": 2.5,
                    },
                },
                "filter": {
                    "minimum_cutoff_hz": 1.2,
                    "beta": 0.015,
                    "derivative_cutoff_hz": 1.0,
                },
                "window": {
                    "single_monitor_only": False,
                    "require_monitor_consistency": True,
                },
            }
        )