import logging.config

log_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "thread": {"format": "%(levelname)s %(asctime)s %(funcName)s thread_id:%(thread)d - %(message)s"},
        "verbose": {"format": "%(lineno)d in %(filename)s at %(asctime)s: %(message)s"},
        "general": {"format": "%(levelname)s %(asctime)s - %(message)s"}
        },
    "handlers": {
        "thread": {"class": "logging.StreamHandler",
                   "formatter": "thread",
                   "level": "DEBUG"
                   },
        "general": {"class": "logging.StreamHandler",
                    "formatter": "general",
                    "level": "DEBUG"
                    }
        },
    "loggers": {
        "thread": {
            "handlers": ["thread"],
            "level": "DEBUG",
        },
        "general": {
            "handlers": ["general"],
            "level": "DEBUG",
        }
    }
}