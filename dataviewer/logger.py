import logging

try:
    import colorlog

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)-4s] [%(filename)s:%(lineno)d] %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )
except ImportError:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)-4s] [%(filename)s:%(lineno)d] %(message)s"
        )
    )

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(handler)
