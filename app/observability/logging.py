import logging


def configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s level=%(levelname)s logger=%(name)s message=%(message)s",
        force=True,
    )
