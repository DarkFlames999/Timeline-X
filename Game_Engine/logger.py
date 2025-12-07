from pathlib import Path
import colorlog
import colorama
import logging


LogConfig = {
    "FORMAT": {
        "LOG": "f\"{log_color}[{style}{levelname}]{reset} %(cyan)s{asctime}{reset} %(light_cyan)s{pathname}{reset} %(white)s-{reset} {style}{log_color}{message}{reset}\"",
        "DATE": "f\"{Day}-{Month}-{Year} {Hour}:{Minute}:{Second}\""
    },
    "COLORS": {
        "DEBUG": "light_green",
        "INFO":  "light_green",
        "WARNING": "light_yellow",
        "ERROR": "red",
        "CRITICAL": "light_red",
        "SUPER-CRITICAL": "light_red"
    },
    "STYLES": {
        "DEBUG": "BOLD",
        "SUPER-CRITICAL": "BOLD"
    },
    "CUSTOM LEVELS": {
        "SUPER-CRITICAL": 60
    },
    "PARSED FORMAT": {
        "log_color": "%(log_color)s",
        "style": "%(style)s",
        "levelname": "%(levelname)-0s",
        "reset": "%(reset)s",
        "asctime": "%(asctime)s",
        "message": "%(message)s",
        "pathname": "%(pathname)-0s",
        "Day": "%d",
        "Month": "%m",
        "Year": "%Y",
        "Hour": "%H",
        "Minute": "%M",
        "Second": "%S"
    }
}

for name, _level in LogConfig["CUSTOM LEVELS"].items():
    logging.addLevelName(_level, name)


class Formatter(colorlog.ColoredFormatter):
    def format(self, record):
        record.log_color = LogConfig["COLORS"].get(record.levelname, 'white')

        match LogConfig["STYLES"].get(record.levelname, colorama.Style.NORMAL):
            case "BOLD":
                record.style = colorama.Style.BRIGHT
            case _:
                record.style = colorama.Style.NORMAL

        record.pathname = getattr(record, 'overridePath', record.pathname)
        record.pathname = (
            str(Path(record.pathname)).replace(
                str(Path.cwd()), "").removeprefix("\\")
        )

        if record.levelname == "SUPER-CRITICAL":
            record.QUIT = True

        return super().format(record)


__formatParser = lambda log: eval(LogConfig["FORMAT"][log], globals=LogConfig["PARSED FORMAT"], locals={})
__ConsoleHandler = logging.StreamHandler()
__Formatter = Formatter(__formatParser("LOG"), datefmt=__formatParser("DATE"), log_colors=LogConfig["COLORS"])
__ConsoleHandler.setFormatter(__Formatter)

logging.root.setLevel(logging.DEBUG)
logging.root.addHandler(__ConsoleHandler)


def log(level, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
    logging.log(level, msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
    if level == 60:
        quit()

debug = logging.debug
info = logging.info
warning = logging.warning
error = logging.error
critical = logging.critical

setLevel = logging.root.setLevel