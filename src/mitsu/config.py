"""Typed, validated application configuration."""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PinchSettings(BaseModel):
    """Scale-invariant pinch thresholds."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    engage_ratio: float = Field(gt=0.0, lt=1.0)
    release_ratio: float = Field(gt=0.0, lt=1.0)

    @model_validator(mode="after")
    def release_must_exceed_engage(self) -> PinchSettings:
        if self.release_ratio <= self.engage_ratio:
            raise ValueError("release_ratio must be greater than engage_ratio")
        return self


class VelocitySettings(BaseModel):
    """Settings for velocity-sensitive relative movement."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    smoothing_alpha: float = Field(gt=0.0, le=1.0)
    activation_speed: float = Field(gt=0.0, le=20.0)
    maximum_gain_multiplier: float = Field(ge=1.0, le=5.0)


class GestureSettings(BaseModel):
    """Settings for relative hand-to-window movement."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    movement_gain: float = Field(gt=0.0, le=10_000.0)
    minimum_delta_pixels: float = Field(ge=0.0, le=100.0)
    pinch: PinchSettings
    velocity: VelocitySettings


class FilterSettings(BaseModel):
    """One Euro Filter parameters."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    minimum_cutoff_hz: float = Field(gt=0.0, le=100.0)
    beta: float = Field(ge=0.0, le=10.0)
    derivative_cutoff_hz: float = Field(gt=0.0, le=100.0)


class WindowSettings(BaseModel):
    """Window-control scope restrictions."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    single_monitor_only: bool
    require_monitor_consistency: bool


class Settings(BaseModel):
    """Complete application settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    gesture: GestureSettings
    filter: FilterSettings
    window: WindowSettings


def load_settings(path: Path) -> Settings:
    """Load and validate a TOML configuration file."""

    with path.open("rb") as config_file:
        raw_config = tomllib.load(config_file)
    return Settings.model_validate(raw_config)
