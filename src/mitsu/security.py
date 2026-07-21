"""Process security and local model-integrity controls."""

from __future__ import annotations

import ctypes
import hashlib
import hmac
import re
from pathlib import Path

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4


def enable_per_monitor_dpi_awareness() -> None:
    """Enable PMv2 before any window, camera UI, or Win32 control call."""

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    set_awareness = user32.SetProcessDpiAwarenessContext
    set_awareness.argtypes = [ctypes.c_void_p]
    set_awareness.restype = ctypes.c_bool

    success = set_awareness(
        ctypes.c_void_p(_DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
    )
    if not success:
        error_code = ctypes.get_last_error()
        raise RuntimeError(
            "Could not enable per-monitor DPI awareness V2 before startup."
            f"Windows error: {error_code}"
        )


def verify_model_integrity(model_path: Path, pin_path: Path) -> None:
    """Verify the local model against its commited SHA-256 pin."""

    if not model_path.is_file():
        raise FileNotFoundError(f"Hand Landmarker model not found: {model_path}")
    if not pin_path.is_file():
        raise FileNotFoundError(
            f"Model hash pin not found: {pin_path}. "
            "Run scripts/bootstrap_hand_model.py first."
        )

    expected_hash = pin_path.read_text(encoding="ascii").strip().lower()
    if not _SHA256_PATTERN.fullmatch(expected_hash):
        raise ValueError(f"Invalid SHA-256 pin format: {pin_path}")

    actual_hash = _sha256_file(model_path)
    if not hmac.compare_digest(actual_hash, expected_hash):
        raise RuntimeError(
            "Hand Landmarker model integrity check failed."
            "Delete the model and bootstrap it again from the reviewed source."
        )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as model_file:
        while chunk := model_file.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()
