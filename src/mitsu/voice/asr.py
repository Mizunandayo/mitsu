"""OpenAI transcription adapter with ephemeral WAV handling."""

from __future__ import annotations

import os
import tempfile
import time
import wave
from pathlib import Path

import numpy as np
from openai import OpenAI

from mitsu.voice.types import AudioClip, Transcription


class OpenAITranscriber:
    """Send an explicit push-to-talk clip to OpenAI for transcription."""

    def __init__(
        self,
        api_key: str,
        model: str,
        language: str,
        prompt: str,
    ) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for voice transcription")

        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._language = language
        self._prompt = prompt

    @classmethod
    def from_environment(
        cls,
        model: str,
        language: str,
        prompt: str,
    ) -> OpenAITranscriber:
        """Create from the process environment without logging the API key."""

        return cls(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            model=model,
            language=language,
            prompt=prompt,
        )

    def transcribe(self, clip: AudioClip) -> Transcription:
        """Upload one temporary WAV and securely remove it after the request."""

        temporary_path = self._write_temporary_wav(clip)
        started = time.perf_counter()

        try:
            with temporary_path.open("rb") as audio_file:
                response = self._client.audio.transcriptions.create(
                    file=audio_file,
                    model=self._model,
                    language=self._language,
                    prompt=self._prompt,
                    response_format="json",
                )
        finally:
            temporary_path.unlink(missing_ok=True)

        return Transcription(
            text=response.text.strip(),
            latency_ms=(time.perf_counter() - started) * 1000,
        )

    @staticmethod
    def _write_temporary_wav(clip: AudioClip) -> Path:
        samples = np.clip(clip.samples, -1.0, 1.0)
        pcm_samples = (samples * np.iinfo(np.int16).max).astype(np.int16)

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temporary_file:
            path = Path(temporary_file.name)

        with wave.open(str(path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(clip.sample_rate_hz)
            wav_file.writeframes(pcm_samples.tobytes())

        return path