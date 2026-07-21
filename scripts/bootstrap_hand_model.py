"""Download and explicitly trust-on-first-use the MediaPipe hand model."""

from __future__ import annotations

import argparse
import hashlib
import tempfile
from http.client import HTTPSConnection
from pathlib import Path

MODEL_HOST = "storage.googleapis.com"
MODEL_PATH = (
    "/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/"
    "hand_landmarker.task"
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

    if model_path.exists():
        raise FileExistsError(
            "Model already exists. Refusing to overwrite local model state."
        )

    expected_digest = (
        pin_path.read_text(encoding="ascii").strip().casefold()
        if pin_path.exists()
        else None
    )

    models_directory.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        # HTTPSConnection verifies TLS certificates by default. The host and path
        # are constants, so this downloader cannot be redirected to an arbitrary URL.
        with HTTPSConnection(MODEL_HOST, timeout=30) as connection:
            connection.request("GET", MODEL_PATH, headers={"User-Agent": "MITSU/0.1"})
            response = connection.getresponse()

            if response.status != 200:
                raise RuntimeError(
                    f"Model download failed with HTTP status {response.status}."
                )

            content_length = response.getheader("Content-Length")
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
                        raise ValueError(
                            "Model download exceeds the configured size limit."
                        )

                    digest.update(chunk)
                    temporary_file.write(chunk)

        actual_digest = digest.hexdigest()
        if expected_digest is not None and actual_digest.casefold() != expected_digest:
            raise ValueError(
                "Downloaded model does not match the committed SHA-256 pin."
            )

        temporary_path.replace(model_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise

    if expected_digest is None:
        pin_path.write_text(f"{actual_digest}\n", encoding="ascii")

    print(f"Model saved: {model_path}")
    if expected_digest is None:
        print(f"SHA-256 pin saved: {pin_path}")
        print("Review and commit the .sha256 pin, never the model file.")
    else:
        print(f"SHA-256 pin verified: {pin_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
