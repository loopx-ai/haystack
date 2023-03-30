from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG = {
    **LOGGING_CONFIG,
    "version": 1,
    "loggers": {
        "uvicorn": {"propagate": True},
        "uvicorn.error": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "haystack": {"propagate": True},
    },
}