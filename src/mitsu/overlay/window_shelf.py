"""A compact, click-through shelf for choosing minimized windows by hand."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pywintypes
import win32gui
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QFont, QFontDatabase, QPainter, QPen
from PySide6.QtWidgets import QWidget

from mitsu.control.coordinate_mapper import ScreenBounds, ScreenPoint
from mitsu.control.window_manager import WindowTarget


@dataclass(frozen=True, slots=True)
class ShelfItem:
    """One visible minimized-window target and its paint and screen bounds."""

    handle: int
    title: str
    bounds: QRect
    screen_bounds: QRect


class WindowShelf(QWidget):
    """Show minimized windows and resolve a hand-coordinate selection."""

    _MAX_ITEMS = 6
    _PANEL_WIDTH = 620
    _ROW_HEIGHT = 54
    _PADDING = 18

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

        self._font = QFont(families[0], 16)
        self._items: tuple[ShelfItem, ...] = ()
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

    @property
    def active(self) -> bool:
        """Return whether the shelf currently has selectable items."""

        return bool(self._items) and self.isVisible()

    def present(
        self,
        windows: tuple[WindowTarget, ...],
        monitor_bounds: ScreenBounds,
    ) -> None:
        """Display up to six minimized windows centered on the primary monitor."""

        visible_windows = windows[: self._MAX_ITEMS]
        if not visible_windows:
            self.dismiss()
            return

        panel_height = self._PADDING * 2 + len(visible_windows) * self._ROW_HEIGHT
        panel_left = (
            monitor_bounds.left + (monitor_bounds.width - self._PANEL_WIDTH) // 2
        )
        panel_top = monitor_bounds.top + max(
            80, (monitor_bounds.height - panel_height) // 3
        )
        self.setGeometry(panel_left, panel_top, self._PANEL_WIDTH, panel_height)
        self.show()
        self.raise_()
        physical_panel = self._physical_panel_bounds(
            fallback=QRect(
                panel_left,
                panel_top,
                self._PANEL_WIDTH,
                panel_height,
            )
        )
        horizontal_scale = physical_panel.width() / self._PANEL_WIDTH
        vertical_scale = physical_panel.height() / panel_height
        screen_padding_x = round(self._PADDING * horizontal_scale)
        screen_padding_y = round(self._PADDING * vertical_scale)
        screen_row_height = round(self._ROW_HEIGHT * vertical_scale)
        self._items = tuple(
            ShelfItem(
                handle=window.handle,
                title=window.title,
                bounds=QRect(
                    self._PADDING,
                    self._PADDING + index * self._ROW_HEIGHT,
                    self._PANEL_WIDTH - self._PADDING * 2,
                    self._ROW_HEIGHT - 6,
                ),
                screen_bounds=QRect(
                    physical_panel.left() + screen_padding_x,
                    physical_panel.top() + screen_padding_y + index * screen_row_height,
                    physical_panel.width() - screen_padding_x * 2,
                    screen_row_height - round(6 * vertical_scale),
                ),
            )
            for index, window in enumerate(visible_windows)
        )
        self.update()

    def dismiss(self) -> None:
        """Hide and clear all selectable targets."""

        self._items = ()
        self.hide()

    def selection_at(self, point: ScreenPoint) -> int | None:
        """Return the selected window handle for a hand-controlled point."""

        for item in self._items:
            if item.screen_bounds.contains(point.x, point.y):
                return item.handle
        return None

    def _physical_panel_bounds(self, fallback: QRect) -> QRect:
        """Get the native physical rectangle after Qt's DPI scaling is applied."""

        try:
            left, top, right, bottom = win32gui.GetWindowRect(int(self.winId()))
        except pywintypes.error:
            return fallback
        return QRect(left, top, right - left, bottom - top)

    def paintEvent(self, _event: object) -> None:  # noqa: N802 - Qt override.
        """Paint the compact dark shelf without intercepting input."""

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(16, 18, 22, 242))
        painter.drawRoundedRect(self.rect(), 8, 8)

        painter.setFont(self._font)
        for item in self._items:
            local = item.bounds
            painter.setBrush(QColor(28, 34, 40))
            painter.drawRoundedRect(local, 5, 5)
            painter.setPen(QPen(QColor("#00dcb4"), 1.5))
            painter.drawRect(local)
            painter.setPen(QColor("#f8f8f2"))
            painter.drawText(
                local.adjusted(16, 0, -16, 0),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                item.title[:58],
            )
        painter.end()
