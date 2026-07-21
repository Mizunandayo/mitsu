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
    release_debounce_frames: int = Field(default=8, ge=2, le=30)

    @model_validator(mode="after")
    def release_must_exceed_engage(self) -> PinchSettings:
        if self.release_ratio <= self.engage_ratio:
            raise ValueError("release_ratio must be greater than engage_ratio")
        return self


class VelocitySettings(BaseModel):
    """Velocity-sensitive movement settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    smoothing_alpha: float = Field(gt=0.0, le=1.0)
    activation_speed: float = Field(gt=0.0, le=20.0)
    maximum_gain_multiplier: float = Field(ge=1.0, le=5.0)


class FistSettings(BaseModel):
    """Whole-hand grip thresholds, normalized by palm size."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    engage_tip_distance_ratio: float = Field(default=1.10, gt=0.0, le=3.0)
    release_tip_distance_ratio: float = Field(default=1.35, gt=0.0, le=3.0)
    release_debounce_frames: int = Field(default=8, ge=2, le=30)

    @model_validator(mode="after")
    def release_must_exceed_engage(self) -> FistSettings:
        if self.release_tip_distance_ratio <= self.engage_tip_distance_ratio:
            raise ValueError(
                "release_tip_distance_ratio must exceed engage_tip_distance_ratio"
            )
        return self


class VSignSettings(BaseModel):
    """V-sign thresholds for opening the minimized-window shelf."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    extension_ratio: float = Field(default=1.25, gt=1.0, le=4.0)
    folded_finger_ratio: float = Field(default=1.20, gt=0.0, le=4.0)
    minimum_finger_gap_ratio: float = Field(default=0.45, gt=0.0, le=2.0)
    minimum_hold_frames: int = Field(default=4, ge=2, le=30)


class GestureSettings(BaseModel):
    """Hand gesture settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    movement_gain: float = Field(gt=0.0, le=10_000.0)
    minimum_delta_pixels: float = Field(ge=0.0, le=100.0)
    pinch: PinchSettings
    velocity: VelocitySettings
    fist: FistSettings = Field(default_factory=FistSettings)
    v_sign: VSignSettings = Field(default_factory=VSignSettings)


class FilterSettings(BaseModel):
    """One Euro Filter settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    minimum_cutoff_hz: float = Field(gt=0.0, le=100.0)
    beta: float = Field(ge=0.0, le=10.0)
    derivative_cutoff_hz: float = Field(gt=0.0, le=100.0)


class WindowSettings(BaseModel):
    """Window-control safety settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    single_monitor_only: bool
    require_monitor_consistency: bool


class PointerSettings(BaseModel):
    """Primary-monitor absolute-pointer calibration in normalized camera space."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    camera_left: float = Field(ge=0.0, lt=1.0)
    camera_top: float = Field(ge=0.0, lt=1.0)
    camera_right: float = Field(gt=0.0, le=1.0)
    camera_bottom: float = Field(gt=0.0, le=1.0)

    @model_validator(mode="after")
    def camera_bounds_must_be_ordered(self) -> PointerSettings:
        if self.camera_right <= self.camera_left:
            raise ValueError("camera_right must exceed camera_left")
        if self.camera_bottom <= self.camera_top:
            raise ValueError("camera_bottom must exceed camera_top")
        return self


class ClickSettings(BaseModel):
    """Index-middle pose with a deliberate downward finger press trigger."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = False
    pointer_extension_ratio: float = Field(gt=1.0, le=4.0)
    fingers_close_ratio: float = Field(gt=0.0, lt=1.0)
    fingers_release_ratio: float = Field(gt=0.0, lt=1.0)
    minimum_press_downward_ratio: float = Field(gt=0.0, le=4.0)
    minimum_click_pose_frames: int = Field(ge=2, le=30)
    ring_extension_ratio: float = Field(gt=1.0, le=4.0)
    minimum_forward_pose_frames: int = Field(ge=2, le=30)
    pinky_extension_ratio: float = Field(gt=1.0, le=4.0)
    minimum_back_pose_frames: int = Field(ge=2, le=30)

    @model_validator(mode="after")
    def release_must_exceed_close(self) -> ClickSettings:
        if self.fingers_release_ratio <= self.fingers_close_ratio:
            raise ValueError(
                "fingers_release_ratio must be greater than fingers_close_ratio"
            )
        return self


class MinimizeSettings(BaseModel):
    """Three-finger minimization and open-palm safety settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = False
    open_palm_extension_ratio: float = Field(gt=1.0, le=4.0)
    maximize_open_palm_extension_ratio: float = Field(gt=1.0, le=4.0)
    minimum_open_palm_frames: int = Field(ge=2, le=30)
    triad_close_ratio: float = Field(gt=0.0, le=2.0)
    triad_extension_ratio: float = Field(gt=1.0, le=4.0)
    folded_pinky_extension_ratio: float = Field(gt=0.0, le=4.0)
    minimum_thumb_index_ratio: float = Field(gt=0.0, le=4.0)
    minimum_pose_frames: int = Field(ge=2, le=30)
    minimum_downward_distance_ratio: float = Field(gt=0.0, le=2.0)
    downward_velocity_ratio_per_second: float = Field(gt=0.0, le=20.0)

    @model_validator(mode="after")
    def maximize_palm_must_be_wider_than_minimize_palm(self) -> MinimizeSettings:
        if self.maximize_open_palm_extension_ratio <= self.open_palm_extension_ratio:
            raise ValueError(
                "maximize_open_palm_extension_ratio must exceed "
                "open_palm_extension_ratio"
            )
        return self


class VoiceSettings(BaseModel):
    """Explicit cloud transcription settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    sample_rate_hz: int = Field(ge=8_000, le=48_000)
    maximum_recording_seconds: float = Field(gt=0.5, le=10.0)
    minimum_signal_rms: float = Field(default=0.003, gt=0.0, le=0.1)
    language: str = Field(pattern=r"^[a-z]{2}$")
    transcription_model: str = Field(min_length=1, max_length=100)
    transcription_prompt: str = Field(min_length=1, max_length=500)


class CloudSettings(BaseModel):
    """Bounded OpenAI reasoning configuration."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = False
    model: str = Field(default="gpt-5.6-terra", min_length=1, max_length=100)
    timeout_seconds: float = Field(default=1.5, gt=0.0, le=10.0)
    failure_threshold: int = Field(default=2, ge=1, le=10)
    cooldown_seconds: float = Field(default=30.0, gt=0.0, le=600.0)
    maximum_tool_rounds: int = Field(default=3, ge=1, le=5)
    allow_screen_capture: bool = False


class ObservabilitySettings(BaseModel):
    """Bounded in-memory runtime measurement configuration."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    maximum_samples: int = Field(default=300, ge=30, le=10_000)


class Settings(BaseModel):
    """Complete MITSU settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    gesture: GestureSettings
    filter: FilterSettings
    window: WindowSettings
    pointer: PointerSettings = Field(
        default_factory=lambda: PointerSettings(
            camera_left=0.0,
            camera_top=0.0,
            camera_right=1.0,
            camera_bottom=1.0,
        )
    )
    click: ClickSettings = Field(
        default_factory=lambda: ClickSettings(
            pointer_extension_ratio=1.35,
            fingers_close_ratio=0.50,
            fingers_release_ratio=0.65,
            minimum_press_downward_ratio=0.02,
            minimum_click_pose_frames=2,
            ring_extension_ratio=1.25,
            minimum_forward_pose_frames=3,
            pinky_extension_ratio=1.25,
            minimum_back_pose_frames=3,
        )
    )
    minimize: MinimizeSettings = Field(
        default_factory=lambda: MinimizeSettings(
            open_palm_extension_ratio=1.20,
            maximize_open_palm_extension_ratio=1.30,
            minimum_open_palm_frames=3,
            triad_close_ratio=0.70,
            triad_extension_ratio=1.20,
            folded_pinky_extension_ratio=1.20,
            minimum_thumb_index_ratio=0.45,
            minimum_pose_frames=3,
            minimum_downward_distance_ratio=0.14,
            downward_velocity_ratio_per_second=1.1,
        )
    )
    voice: VoiceSettings
    cloud: CloudSettings = Field(default_factory=CloudSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)


def load_settings(path: Path) -> Settings:
    """Load and validate a TOML configuration file."""

    with path.open("rb") as config_file:
        return Settings.model_validate(tomllib.load(config_file))
