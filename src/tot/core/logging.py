import logging
from rich.logging import RichHandler

def setup_logging(level: str) -> None:
    # map custom 'trace' and 'quiet'
    if level == "trace":
        lvl = 5
        logging.addLevelName(5, "TRACE")
    elif level == "quiet":
        lvl = logging.CRITICAL + 10
    else:
        lvl = getattr(logging, level.upper(), logging.INFO)

    handlers = [RichHandler(rich_tracebacks=True, markup=True)]
    logging.basicConfig(level=lvl, handlers=handlers, format="%(message)s")
