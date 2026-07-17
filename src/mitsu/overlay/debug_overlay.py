"""Poppins-rendered OpenCV diagnostic overlay."""


from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from mitsu.control.coordinate_mapper import ScreenPoint
from mitsu.gestures.state_machine import GestureState
from mitsu.perception.hand_tracker import TrackedHand


class DebugOverlay:
    """Render Day-2 camera diagnostics without OpenCV Hershey text."""

    def __init__(self, font_path: Path) -> None:
        if not font_path.is_file():
            raise FileNotFoundError(f"Poppins font not found: {font_path}")
        self._font = ImageFont.truetype(str(font_path), size=18)

    def draw(
        self,
        frame: np.ndarray,
        hand: TrackedHand | None,
        state: GestureState,
        active_handle: int | None,
        hover_title: str | None,
        projected_point: ScreenPoint | None,
    ) -> np.ndarray:
        """Return a landmark and state annotated BGR frame."""

        output = frame.copy()
        height, width = output.shape[:2]

        if hand is not None:
            for point in hand.display_points:
                cv2.circle(
                    output,
                    (round(point.x * width), round(point.y * height)),
                    4,
                    (255, 190, 0),
                    -1,
                )

        rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        draw = ImageDraw.Draw(image)

        draw.rectangle((12, 12, 510, 132), fill=(16, 18, 22))
        draw.text(
            (24, 23),
            f"State: {state.name}",
            font=self._font,
            fill=(248, 248, 242),
        )
        target_text = "none" if active_handle is None else str(active_handle)
        draw.text(
            (24, 49),
            f"Target: {target_text}",
            font=self._font,
            fill=(0, 220, 180),
        )
        hover_text = "none" if hover_title is None else hover_title[:42]
        draw.text(
            (24, 75),
            f"Aim: {hover_text}",
            font=self._font,
            fill=(248, 248, 242),
        )
        point_text = (
            "unavailable"
            if projected_point is None
            else f"{projected_point.x}, {projected_point.y}"
        )
        draw.text(
            (24, 101),
            f"Screen point: {point_text}",
            font=self._font,
            fill=(0, 220, 180) if hover_title is not None else (248, 248, 242),
        )

        return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
