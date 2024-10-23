import logging
import json
from contextvars import ContextVar
from logging import config

request_id_ctx_var: ContextVar[str] = ContextVar("request_id")


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        log_record.request_id = request_id_ctx_var.get(None)
        return True


class JsonFormatter(logging.Formatter):
    ADDITIONAL_FIELDS = (
        "request_id",
    )

    def format(self, record: logging.LogRecord):
        recording = {
            "level": record.levelname,
            "asctime": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
        }
        for field in self.ADDITIONAL_FIELDS:
            if (
                hasattr(record, field) and (_req := getattr(record, field)) is not None  # noqa
            ):
                recording.update(**{field: _req})
        return json.dumps(recording, ensure_ascii=False)


LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "contextual": {
            "()": ContextualFilter,
        },
    },
    "formatters": {
        "json": {
            "()": JsonFormatter,
            "format": "%(asctime) %(levelname) %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filters": ["contextual"],
        },
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': 'app.log',
        #     'level': 'DEBUG',
        #     'formatter': 'json',
        #     'filters': ['contextual'],
        # },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],  # 'file'
            "level": "DEBUG",
            "propagate": False,
        },
        "cli": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "asyncio": {
            "level": "WARNING",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
        ],  # 'file'
    },
}


config.dictConfig(LOGGER_CONFIG)

app_logger = logging.getLogger("app")
