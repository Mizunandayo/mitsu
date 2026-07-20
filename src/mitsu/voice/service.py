"""Single-worker voice transcription service."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from queue import Empty, SimpleQueue

from mitsu.voice.asr import OpenAITranscriber
from mitsu.voice.intent import parse_command
from mitsu.voice.types import AudioClip, VoiceResult


class VoiceService:
    """Keep transcription off the camera and gesture loop."""
    def __init__(self, transcriber: OpenAITranscriber) -> None:
        self._transcriber = transcriber
        self._executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="mitsu-voice",
        )
        self._results: SimpleQueue[VoiceResult] = SimpleQueue()
        self._pending: Future[None] | None = None

    def submit(self, clip: AudioClip) -> bool:
        """Submit one clip unless another command is still in progress."""

        if self._pending is not None and not self._pending.done():
            return False

        self._pending = self._executor.submit(self._transcribe, clip)
        return True

    def poll(self) -> VoiceResult | None:
        """Return one completed result without blocking the gesture loop."""

        try:
            return self._results.get_nowait()
        except Empty:
            return None

    def close(self) -> None:
        """Cancel pending work during shutdown."""

        self._executor.shutdown(wait=False, cancel_futures=True)

    def _transcribe(self, clip: AudioClip) -> None:
        try:
            transcription = self._transcriber.transcribe(clip)
            self._results.put(
                VoiceResult(
                    transcription=transcription,
                    intent=parse_command(transcription.text),
                    error_message=None,
                )
            )
        except Exception as error:
            self._results.put(
                VoiceResult(
                    transcription=None,
                    intent=None,
                    error_message=type(error).__name__,
                )
            )