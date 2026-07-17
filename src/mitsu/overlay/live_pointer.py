"""Transparent on-desktop pointer feedback for calibrated hand coordinates."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QFont, QFontDatabase, QPainter, QPen
from PySide6.QtWidgets import QWidget

from mitsu.control.coordinate_mapper import ScreenPoint


class LivePointerOverlay(QWidget):
    """A click-through pointer that never captures focus or mouse input."""

    _RING_CENTER = QPoint(18, 18)

    def __init__(self, font_path: Path) -> None:
        super().__init__()

        if not font_path.is_file():
            raise FileNotFoundError(f"Poppins font not found: {font_path}")

        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id < 0:
            raise RuntimeError(f"Could not load Poppins font: {font_path}")

        families = QFontDatabase.applicationFontFamilies(font_id)
        if not families:
            raise RuntimeError(f"Poppins font has no usable family: {font_path}")

        self._font = QFont(families[0], 14)
        self._label = ""
        self.setFixedSize(260, 46)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    def show_at(self, point: ScreenPoint, target_title: str | None) -> None:
        """Place the pointer ring at a physical desktop coordinate."""

        self._label = (
            f"{point.x}, {point.y}"
            if target_title is None
            else f"{target_title[:22]}  {point.x}, {point.y}"
        )
        self.move(point.x - self._RING_CENTER.x(), point.y - self._RING_CENTER.y())
        self.show()
        self.update()

    def paintEvent(self, _event: object) -> None:  # noqa: N802 - Qt override.
        """Paint a crisp live marker and readable coordinate label."""

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        accent = QColor("#00dcb4")
        painter.setPen(QPen(accent, 2.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(self._RING_CENTER, 10, 10)
        painter.drawLine(18, 2, 18, 34)
        painter.drawLine(2, 18, 34, 18)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(16, 18, 22, 232))
        painter.drawRoundedRect(42, 4, 212, 34, 6, 6)

        painter.setFont(self._font)
        painter.setPen(QColor("#f8f8f2"))
        painter.drawText(52, 26, self._label)
        painter.end()
