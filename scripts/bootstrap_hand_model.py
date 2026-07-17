"""Download and explicitly trust-on-first-use the MediaPipe hand model."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
MAX_MODEL_BYTES = 50 * 1024 * 1024




def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trust-on-first-use",
        action="store_true",
        help="Download the official model and create its local SHA-256 pin.",
    )
    arguments = parser.parse_args()

    if not arguments.trust_on_first_use:
        parser.error("Refusing download without --trust-on-first-use.")

    project_root = Path(__file__).resolve().parents[1]
    models_directory = project_root / "models"
    model_path = models_directory / "hand_landmarker.task"
    pin_path = models_directory / "hand_landmarker.task.sha256"

    if model_path.exists() or pin_path.exists():
        raise FileExistsError(
            "Model or hash pin already exists. Refusing to overwrite trust state."
        )

    models_directory.mkdir(parents=True, exist_ok=True)
    request = Request(MODEL_URL, headers={"User-Agent": "MITSU/0.1"})

    with urlopen(request, timeout=30) as response:
        content_length = response.headers.get("Content-Length")
        if content_length is not None and int(content_length) > MAX_MODEL_BYTES:
            raise ValueError("Model download exceeds the configured size limit.")

        with tempfile.NamedTemporaryFile(
            mode="wb",
            delete=False,
            dir=models_directory,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            digest = hashlib.sha256()
            total_bytes = 0

            while chunk := response.read(1024 * 1024):
                total_bytes += len(chunk)
                if total_bytes > MAX_MODEL_BYTES:
                    temporary_path.unlink(missing_ok=True)
                    raise ValueError("Model download exceeds the configured size limit.")

                digest.update(chunk)
                temporary_file.write(chunk)

    temporary_path.replace(model_path)
    pin_path.write_text(f"{digest.hexdigest()}\n", encoding="ascii")

    print(f"Model saved: {model_path}")
    print(f"SHA-256 pin saved: {pin_path}")
    print("Review and commit the .sha256 pin, never the model file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())