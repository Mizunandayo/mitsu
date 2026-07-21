"""Native microphone selector for MITSU's explicit push-to-talk capture."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from mitsu.voice.audio_capture import AudioInputDevice


class MicrophoneSelector(QDialog):
    """Choose one input device without recording or retaining any audio."""

    def __init__(self, font_path: Path) -> None:
        super().__init__()
        if not font_path.is_file():
            raise FileNotFoundError(f"Poppins font not found: {font_path}")

        font_id = QFontDatabase.addApplicationFont(str(font_path))
        families = QFontDatabase.applicationFontFamilies(font_id)
        if font_id < 0 or not families:
            raise RuntimeError("Could not load the bundled Poppins font")

        self._font = QFont(families[0], 16)
        self._pending_device_index: int | None = None
        self._selection_ready = False
        self.setWindowTitle("MITSU Microphone")
        self.setModal(False)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setMinimumWidth(460)
        self.setStyleSheet(
            "QDialog { background: #101216; color: #f8f8f2; }"
            "QLabel { color: #f8f8f2; font-size: 16px; }"
            "QComboBox { background: #1c2228; color: #f8f8f2;"
            " border: 1px solid #00dcb4; padding: 8px; min-height: 28px; }"
            "QComboBox:hover { background: #242d34; }"
            "QPushButton { background: #1c2228; color: #f8f8f2;"
            " border: 1px solid #00dcb4; padding: 8px 14px; min-height: 28px; }"
            "QPushButton:hover { background: #243f3d; }"
            "QPushButton:pressed { background: #007f6a; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        title = QLabel("Microphone input", self)
        title.setFont(QFont(families[0], 18, QFont.Weight.DemiBold))
        layout.addWidget(title)
        self._detail = QLabel("Choose the device used by push-to-talk.", self)
        self._detail.setFont(self._font)
        layout.addWidget(self._detail)
        self._devices = QComboBox(self)
        self._devices.setFont(self._font)
        self._devices.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self._devices)

        actions = QHBoxLayout()
        actions.addStretch()
        cancel = QPushButton("Cancel", self)
        cancel.setFont(self._font)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.hide)
        apply = QPushButton("Use microphone", self)
        apply.setFont(self._font)
        apply.setCursor(Qt.CursorShape.PointingHandCursor)
        apply.clicked.connect(self._commit_selection)
        actions.addWidget(cancel)
        actions.addWidget(apply)
        layout.addLayout(actions)

    def present(
        self,
        devices: tuple[AudioInputDevice, ...],
        selected_device_index: int | None,
    ) -> None:
        """Show a fresh device list and preselect the active input."""

        self._selection_ready = False
        self._devices.clear()
        self._devices.addItem("Windows default microphone", None)
        for device in devices:
            self._devices.addItem(device.name, device.index)
        selected_index = self._devices.findData(selected_device_index)
        self._devices.setCurrentIndex(max(selected_index, 0))
        self.show()
        self.raise_()
        self.activateWindow()

    def take_selection(self) -> tuple[bool, int | None]:
        """Return whether a choice was made and its device index."""

        if not self._selection_ready:
            return False, None
        self._selection_ready = False
        return True, self._pending_device_index

    def _commit_selection(self) -> None:
        selected = self._devices.currentData()
        self._pending_device_index = None if selected is None else int(selected)
        self._selection_ready = True
        self.hide()
