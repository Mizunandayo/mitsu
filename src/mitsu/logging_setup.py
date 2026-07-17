"""Application logging with automatic secret redaction."""


from __future__ import annotations

import logging
import re


class SecretRedactionFilter(logging.Filter):
    """Redact common API-key and bearer-token patterns from log messages."""

    _PATTERNS = (
        re.compile(r"sk-[A-Za-z0-9_-]+"),
        re.compile(r"Bearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    )

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()

        for pattern in self._PATTERNS:
            message = pattern.sub("[REDACTED]", message)
        
        record.msg = message
        record.args = ()
        return True
    



def configure_logging() -> logging.Logger:
    """Configure safe console logging once."""

    logger = logging.getLogger("mitsu")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    handler.addFilter(SecretRedactionFilter())
    logger.addHandler(handler)
    return logger