import logging.config

log_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(levelname)s %(asctime)s thread_id:%(thread)d %(message)s"
                     }, 
        "verbose": {"format": "%(lineno)d in %(filename)s at %(asctime)s: %(message)s"}
        },
    "handlers": {
        "console": {"class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": "DEBUG"
                    }
        },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    }
}