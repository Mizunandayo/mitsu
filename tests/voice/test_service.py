from __future__ import annotations

import time

import numpy as np

from mitsu.voice.service import VoiceService
from mitsu.voice.types import AudioClip, Transcription


class FakeTranscriber:
    def transcribe(self, _clip: AudioClip) -> Transcription:
        return Transcription(text="show Discord", latency_ms=12.0)


def test_service_returns_a_parsed_voice_intent() -> None:
    service = VoiceService(FakeTranscriber())  # type: ignore[arg-type]
    clip = AudioClip(
        samples=np.zeros(16_000, dtype=np.float32),
        sample_rate_hz=16_000,
    )

    assert service.submit(clip) is True

    deadline = time.monotonic() + 1.0
    result = None

    while time.monotonic() < deadline:
        result = service.poll()
        if result is not None:
            break
        time.sleep(0.01)

    assert result is not None
    assert result.intent is not None
    assert result.intent.app_name == "Discord"

    service.close()