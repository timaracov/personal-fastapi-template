from os.path import join
from logging import getLogger, Formatter, StreamHandler, FileHandler

from colorama import Fore, Style
from .base import ConfigBase
from .api import API_CONFIG


class LoggingConfig(ConfigBase):
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = join(API_CONFIG.PROJECT_PATH, "__project_name__.log")
    LOG_FORMAT: str = "json"


LOGGING_CONFIG = LoggingConfig()


def configure_logging():
    root_logger = getLogger()
    root_logger.setLevel(LOGGING_CONFIG.LOG_LEVEL)

    basic_formatter = Formatter(
        "[%(levelname)s]:"
        "[%(name)s]:"
        "[%(pathname)s/%(funcName)s:%(lineno)s]:"
        "[%(asctime)s]:"
        "[pid:%(process)d|tid:%(thread)d]"
        ":: %(message)s"
    )

    std_colored_formatter = Formatter(
        Fore.CYAN+Style.BRIGHT
        +"[%(levelname)s]:"
        +Fore.YELLOW+Style.BRIGHT
        +"[%(name)s]:"
        +Fore.GREEN+Style.BRIGHT
        +"[%(pathname)s/%(funcName)s:%(lineno)s]:"
        +Fore.BLUE+Style.BRIGHT
        +"[%(asctime)s]:"
        +Style.RESET_ALL
        + "["
        +Fore.GREEN+Style.BRIGHT
        +"pid:%(process)d"
        +Style.RESET_ALL
        + "|"
        +Fore.YELLOW+Style.BRIGHT
        + "]:: %(message)s"
    )

    json_formatter = Formatter(
        "{"
        '"level": "%(levelname)s",'
        '"logger": "%(name)s",'
        '"file": "%(pathname)s",'
        '"function": "%(funcName)s",'
        '"line": "%(lineno)s",'
        '"time": "%(asctime)s",'
        '"process_id": %(process)d,'
        '"thread_id": %(thread)d,'
        '"message": "%(message)s"'
        "}"
    )

    console_log = StreamHandler()
    console_log.setFormatter(std_colored_formatter)
    root_logger.addHandler(console_log)

    if LOGGING_CONFIG.LOG_FILE:
        file_log = FileHandler(LOGGING_CONFIG.LOG_FILE)
        if LOGGING_CONFIG.LOG_FORMAT.lower() == "json":
            file_log.setFormatter(json_formatter)
        else:
            file_log.setFormatter(basic_formatter)
        root_logger.addHandler(file_log)

configure_logging()
