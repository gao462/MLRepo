# Import typing.
from typing import Any
from typing import Tuple as MultiReturn

# Import dependencies.
import sys
import os
import logging

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.

# Import dependencies.


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Define Logging Utilities >>
# 1, Create default logger.
# 2, Universal logger.
# 3, Update universal logger by given logger.
# 4, Check message format.
# 5, Output multiple-line message.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# Different levels as integers.
DEBUG   = 10
INFO1   = 20
INFO2   = 25
FOCUS   = 30
WARNING = 40
ERROR   = 50


def default_logger(*args, **kargs) -> logging.Logger:
    r"""
    Create default logger.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------
    - logger
        Default logger.

    """
    # Allocate logger.
    logger = logging.getLogger('default_logger')
    logger.setLevel(level=DEBUG)

    # Define logging line format.
    formatter = logging.Formatter("%(message)s")

    # Define console streaming.
    console_stream = logging.StreamHandler()
    console_stream.setLevel(level=DEBUG)
    console_stream.setFormatter(formatter)

    # Add stream to logger.
    logger.addHandler(console_stream)
    return logger


# Univeral logger and maximum number of characters.
UNIVERSAL_LOGGER = default_logger()
MAX = 79


def update_universal_logger(*args, logger: logging.Logger, **kargs) -> None:
    r"""
    Update universal logger by given logger.

    Args
    ----
    - *args
    - logger
        New logger.
    - **kargs

    Returns
    -------

    """
    # Replace directly.
    global UNIVERSAL_LOGGER
    UNIVERSAL_LOGGER = logger


def update_max(*args, val: int, **kargs) -> None:
    r"""
    Update maximum number of characters.

    Args
    ----
    - *args
    - val
        Maximum.
    - **kargs

    Returns
    -------

    """
    # Replace directly.
    global MAX
    MAX = val


# Colorful ASCII code on ConEmu palette.
CLR_BLACK  = "30"
CLR_ORANGE = "31"
CLR_TEAL   = "32"
CLR_OLIVE  = "33"
CLR_CADET  = "34"
CLR_PURPLE = "35"
CLR_NAVY   = "36"
CLR_PALE   = "37"
CLR_GRAY   = "30;1"
CLR_RED    = "31;1"
CLR_GREEN  = "32;1"
CLR_YELLOW = "33;1"
CLR_BLUE   = "34;1"
CLR_PINK   = "35;1"
CLR_CYAN   = "36;1"
CLR_WHITE  = "37;1"


# Colorful fix-length level.
CLRFIX = {}
CLRFIX[DEBUG]   = "\033[{:s}mDEBUG   \033[0m".format(CLR_YELLOW)
CLRFIX[INFO1]   = "\033[{:s}mINFO    \033[0m".format(CLR_CYAN)
CLRFIX[INFO2]   = "\033[{:s}mINFO    \033[0m".format(CLR_BLUE)
CLRFIX[FOCUS]   = "\033[{:s}mINFO    \033[0m".format(CLR_GREEN)
CLRFIX[WARNING] = "\033[{:s}mWARNING \033[0m".format(CLR_PINK)
CLRFIX[ERROR]   = "\033[{:s}mERROR   \033[0m".format(CLR_RED)


def check_format(*args, level: int, msg: str, **kargs) -> None:
    r"""
    Check message format.

    Args
    ----
    - *args
    - level
        Logging level.
    - msg
        Message.
    - **kargs

    Returns
    -------

    """
    # Message starts with (class.function, ), and end with dot.
    buf = msg.split(", ")[0].split(".")
    if (len(buf) == 2 or level in (INFO1, INFO2, FOCUS)):
        pass
    else:
        warning(
            "__main__.check_format, message should start with \"class." \
            "function, \".",
        )

    # Message ends with dot.
    if (msg[-1] == "."):
        pass
    else:
        warning(
            "__main__.check_format, message should end with \".\".",
        )


def log(level: int, fmt:str, *args, **kargs) -> None:
    r"""
    Log debug message.

    Args
    ----
    - level
        Logging level.
    - fmt
        Formatter.
    - *args
    - **kargs

    Returns
    -------

    """
    # Get message string.
    msg = fmt.format(*args, **kargs)
    check_format(level=level, msg=msg)

    # Use universal logger for multiple-line logging.
    global UNIVERSAL_LOGGER
    global MAX
    first = True
    previous = "\033[0m"
    for buf in msg.split("\n"):
        while (len(buf) > 0):
            # Get maximum pure characters and the latest style.
            ptr = 0
            cnt = 0
            style = previous
            while (ptr < len(buf) and cnt < MAX):
                if (buf[ptr] == "\033"):
                    style = "\033"
                    while (buf[ptr] != "m"):
                        style = style + buf[ptr]
                        ptr += 1
                    style = style + "m"
                else:
                    cnt += 1
                ptr += 1

            # Log at most maximum characters with previous styles.
            if (first):
                lead = "{:s}| {:s}".format(CLRFIX[level], previous)
                first = False
            else:
                lead = "\033[0m        | {:s}".format(previous)
            UNIVERSAL_LOGGER.log(level, lead + buf[:ptr] + "\033[0m")
            buf = buf[ptr:]
            previous = style


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Define Logging Operations >>
# 1, debug (10).
# 2, info1 (20).
# 3, info2 (25).
# 4, focus (30).
# 5, warning (40).
# 6, error (50).
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


def debug(*args, **kargs) -> None:
    r"""
    Log debug message.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------

    """
    # Send message to universal logger.
    log(DEBUG, *args, **kargs)


def info1(*args, **kargs) -> None:
    r"""
    Log info (dark) message.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------

    """
    # Send message to universal logger.
    log(INFO1, *args, **kargs)


def info2(*args, **kargs) -> None:
    r"""
    Log info (bright) message.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------

    """
    # Send message to universal logger.
    log(INFO2, *args, **kargs)


def focus(*args, **kargs) -> None:
    r"""
    Log focusing message.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------

    """
    # Send message to universal logger.
    log(FOCUS, *args, **kargs)


def warning(*args, **kargs) -> None:
    r"""
    Log warning message.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------

    """
    # Send message to universal logger.
    log(WARNING, *args, **kargs)


def error(*args, **kargs) -> None:
    r"""
    Log error message.

    Args
    ----
    - *args
    - **kargs

    Returns
    -------

    """
    # Send message to universal logger.
    log(ERROR, *args, **kargs)