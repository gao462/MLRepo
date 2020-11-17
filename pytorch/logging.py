# Import future.
from __future__ import annotations

# Import typing.
from typing import Any as ArgT
from typing import Any as KArgT
from typing import Any as Naive
from typing import Final as Const
from typing import Tuple as MultiReturn
from typing import Type, Protocol
from typing import TextIO, BinaryIO
from typing import Union, Tuple, List, Dict, Set, Callable
from typing import TypeVar, Generic
from typing import cast

# Import dependencies.
import sys
import os
import logging
import re

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
# << Default Definition >>
# Default definition calls ahead of global constant claim.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# \
# ANNOTATE VARIABLES
# \
# Different levels as integers.
NULL: Const = 0
DEBUG: Const = 10
INFO1: Const = 20
INFO2: Const = 25
FOCUS: Const = 30
WARNING: Const = 40
ERROR: Const = 50


# \
# ANNOTATE VARIABLES
# \
# Colorful ASCII characters on ConEmu palette.
CLR_BLACK: Const = "30"
CLR_ORANGE: Const = "31"
CLR_TEAL: Const = "32"
CLR_OLIVE: Const = "33"
CLR_CADET: Const = "34"
CLR_PURPLE: Const = "35"
CLR_NAVY: Const = "36"
CLR_PALE: Const = "37"
CLR_GRAY: Const = "30;1"
CLR_RED: Const = "31;1"
CLR_GREEN: Const = "32;1"
CLR_YELLOW: Const = "33;1"
CLR_BLUE: Const = "34;1"
CLR_PINK: Const = "35;1"
CLR_CYAN: Const = "36;1"
CLR_WHITE: Const = "37;1"


# \
# ANNOTATE VARIABLES
# \
# Colorful fix-length message headers.
CLRFIX: Const = {
    NULL: "\033[0m        \033[0m",
    DEBUG: "\033[{:s}mDEBUG   \033[0m".format(CLR_YELLOW),
    INFO1: "\033[{:s}mINFO    \033[0m".format(CLR_CYAN),
    INFO2: "\033[{:s}mINFO    \033[0m".format(CLR_BLUE),
    FOCUS: "\033[{:s}mINFO    \033[0m".format(CLR_GREEN),
    WARNING: "\033[{:s}mWARNING \033[0m".format(CLR_PINK),
    ERROR: "\033[{:s}mERROR   \033[0m".format(CLR_RED),
}


# \
# ANNOTATE VARIABLES
# \
# Special colorful words.
POSITION: Const = "\033[31;1;47;1m{:s}\033[0m"


# \
# ANNOTATE VARIABLES
# \
# Maximum number of characters per message line.
# Number of indent spaces.
MAX: Const = 79
UNIT: Const = 4


# \
# ANNOTATE VARIABLES
# \
# Define message regex.
NUMBER: Const = r"(0|[1-9][0-9]*)"
UNIT_INITIAL: Const = r"([A-Z][A-Za-z]*|{:s})".format(NUMBER)
UNIT_INSIDE: Const = r"([a-z]+|{:s}|{:s})".format(UNIT_INITIAL, NUMBER)
INITIAL: Const = r"({:s}(-{:s})*)".format(UNIT_INITIAL, UNIT_INSIDE)
INSIDE: Const = r"({:s}(-{:s})*)".format(UNIT_INSIDE, UNIT_INSIDE)
MATH: Const = r"$([^\n\$]|\\[^\n])+$"
CODE: Const = r"`([^\n\\`]|\\[^\n])+`"
STRING: Const = r"\"([^\n\\\"]|\\[^\n])*\""
FIRST: Const = r"({:s}|{:s}|{:s}|{:s})".format(
    INITIAL, MATH, CODE, STRING,
)
LATER: Const = r"({:s}|{:s}|{:s}|{:s})".format(INSIDE, MATH, CODE, STRING)
BREAK: Const = r"( |, )"
PARANTHESE: Const = r"\({:s}({:s}{:s})*\)".format(LATER, BREAK, LATER)
SENTENCE: Const = r"^{:s}({:s}({:s}|{:s}))*(\.|:)$".format(
    FIRST, BREAK, LATER, PARANTHESE,
)


def default_logger(
    name: str, level: int,
    *args: ArgT,
    **kargs: KArgT,
) -> logging.Logger:
    r"""
    Default logger.

    Args
    ----
    - name
        Logger name.
    - level
        Logging level.
    - *args
    - **kargs

    Returns
    -------
    - logger
        Default logger.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Allocate logger.
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    # Define logging line format.
    formatter = logging.Formatter("%(message)s")

    # Define console streaming.
    console = logging.StreamHandler()
    console.setLevel(level=level)
    console.setFormatter(formatter)

    # Add stream to logger.
    logger.addHandler(console)
    return logger


# Univeral logger.
universal: logging.Logger = default_logger(__file__, DEBUG)


def update_universal_logger(
    logger: logging.Logger,
    *args: ArgT,
    **kargs: KArgT,
) -> None:
    r"""
    Update universal logger.

    Args
    ----
    - logger
        New logger.
    - *args
    - **kargs

    Returns
    -------

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # \
    # GLOBAL VARIABLES
    # \
    global universal

    # Replace directly.
    universal = logger


def chunk(
    messages: List[str],
    *args: ArgT,
    **kargs: KArgT,
) -> List[str]:
    r"""
    Chunk messages into messages with length limitation.

    Args
    ----
    - messages
        A list of logging messages.
    - *args
    - **kargs

    Returns
    -------
    - lines
        A list of logging lines with limited length.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Cut senetences with length limitation.
    lines = []
    buf = []
    color = ["\033[0m"]
    for text in messages:
        # Empty line is special.
        if (len(text) == 0):
            lines.append(text)
            lines.append("".join(color))
        else:
            pass

        # Split line text if necessary.
        ptr = 0
        while (ptr < len(text)):
            # Scan a color coding.
            if (text[ptr] == "\033"):
                color = ["\033"]
                while (ptr < len(text) and text[ptr] != "m"):
                    color.append(text[ptr])
                    ptr += 1
                if (text[ptr] == "m"):
                    color.append("m")
                    ptr += 1
                else:
                    # Use naive print inside logging operations.
                    msgerr = "Open color code."
                    print(msgerr)
                    raise RuntimeError
                buf.extend(color)
            else:
                buf.append(text[ptr])
                ptr += 1

            # Detect length limitation.
            if (len(buf) == MAX or ptr == len(text)):
                lines.append("".join(buf))
                lines.append("".join(color))
                buf = []
            else:
                pass

    # Concatenate color codes with line text.
    lines = ["\033[0m"] + lines[:-1]
    outputs = []
    for i in range(len(lines) // 2):
        outputs.append(
            "{:s}{:s}\033[0m".format(lines[i * 2], lines[i * 2 + 1]),
        )
    return outputs


def log(
    level: int,
    fmt: str,
    *args: object,
    **kargs: object,
) -> None:
    r"""
    Log message.

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
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # \
    # GLOBAL VARIABLES
    # \
    global universal

    # Get message string.
    message = fmt.format(*args, **kargs)
    paragraphs = paragraphize(message.split("\n"))

    # Generate a list of texts.
    lines = []
    for sec in paragraphs:
        lines.append(" ".join(sec))
        lines.append("")
    outputs = chunk(lines[:-1])

    # Break message into lines with color inheritance.
    universal.log(level, "{:s} | {:s}".format(CLRFIX[level], outputs[0]))
    for itr in outputs[1:]:
        universal.log(level, "{:s} | {:s}".format(CLRFIX[NULL], itr))


def paragraphize(
    messages: List[str],
    *args: ArgT,
    **kargs: KArgT,
) -> List[List[str]]:
    r"""
    Transfer a list of messages into paragraphs.

    Args
    ----
    - messages
        Messages
    - *args
    - **kargs

    Returns
    -------
    - paragraphs
        Paragraphs.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Empty is a special case.
    if (len(messages) == 0):
        return []
    else:
        pass

    # Attach an additional blank line as replacement for EOM.
    buf = messages + [""]

    # Break messages by single blank lines.
    paragraphs = []
    ptr = 0
    while (ptr < len(buf)):
        # Take messages for decoding until a blank line.
        start = ptr
        decoding = []
        while (len(buf[ptr]) > 0):
            decoding.append(buf[ptr])
            ptr += 1

        # Decode according to different flags.
        if (decoding[0] == "$$"):
            paragraphs.extend(mathize(decoding, row=start + 1))
        elif (decoding[0][0:3] == "```"):
            paragraphs.extend(codize(decoding, row=start + 1))
        else:
            paragraphs.extend(textize(decoding, row=start + 1))

        # Go over the tail blank line as moving to next.
        ptr += 1
    return paragraphs


def mathize(
    decoding: List[str],
    *args: ArgT,
    row: int,
    **kargs: KArgT,
) -> List[List[str]]:
    r"""
    Transfer a list of messages into a match block.

    Args
    ----
    - texts
        Texts.
    - *args
    - row
        Transfer starting row ID in raw list of messages.
    - **kargs

    Returns
    -------
    - block
        Math block.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Locate starting and ending row IDs.
    start = row
    end = start + len(decoding) - 1

    # Block must end properly.
    if (decoding[-1] != "$$"):
        # Use naive print inside logging operations.
        msgerr = (
            "Message {:s}, math block starts from line {:d} and is" \
            " expected to end by line {:d}.".format(
                POSITION.format("line {:d}".format(end)), start, end,
            )
        )
        print(msgerr)
        raise RuntimeError
    else:
        pass

    # Math block requires no decoding.
    return [[itr] for itr in decoding]


def codize(
    decoding: List[str],
    *args: ArgT,
    row: int,
    **kargs: KArgT,
) -> List[List[str]]:
    r"""
    Transfer a list of messages into a code block.

    Args
    ----
    - texts
        Texts.
    - *args
    - row
        Transfer starting row ID in raw list of messages.
    - **kargs

    Returns
    -------
    - block
        Math block.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Locate starting and ending row IDs.
    start = row
    end = start + len(decoding) - 1

    # Block must end properly.
    if (decoding[-1] != "$$"):
        # Use naive print inside logging operations.
        msgerr = (
            "Message {:s}, code block starts from line {:d} and is" \
            " expected to end by line {:d}.".format(
                POSITION.format("line {:d}".format(end)), start, end,
            )
        )
        print(msgerr)
        raise RuntimeError
    else:
        pass

    # Code block requires no decoding.
    return [[itr] for itr in decoding]


def textize(
    decoding: List[str],
    *args: ArgT,
    row: int,
    **kargs: KArgT,
) -> List[List[str]]:
    r"""
    Transfer a list of messages into a text block.

    Args
    ----
    - texts
        Texts.
    - *args
    - row
        Transfer starting row ID in raw list of messages.
    - **kargs

    Returns
    -------
    - block
        Text block.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Locate starting and ending row IDs.
    start = row
    end = start + len(decoding) - 1

    # Decode sentences from given messages.
    block = []
    buf = []
    for i, itr in enumerate(decoding):
        buf.append(itr)
        if (itr[-1] == "." or i == len(decoding) - 1):
            # A sentence is ending, decode and clear buffer.
            sentence = " ".join(buf)
            buf.clear()

            # Check sentence regex.
            if (re.match(SENTENCE, sentence) is None):
                # Use naive print inside logging operations.
                msgerr = (
                    "Message {:s}, wrong sentence regex.\n\n" \
                    "```\n{:s}\n```".format(
                        POSITION.format("line {:d}".format(start + i)),
                        sentence,
                    )
                )
                print(msgerr)
                raise RuntimeError
            else:
                pass

            # Append sentence to the block.
            block.append(sentence)
        else:
            # A sentence is not ending, continue.
            pass
    return [block]


class CallableLog(Protocol):
    r"""
    Log function type.
    """
    def __call__(
        self: CallableLog,
        fmt: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Call.

        Args
        ----
        - self
        - fmt
            Formatter.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # VIRTUAL
        # \
        ...


def wrap(
    level: int,
    *args: ArgT,
    **kargs: KArgT,
) -> CallableLog:
    r"""
    Bind log function with a level integer.

    Args
    ----
    - level
        Level integer.
    - *args
    - **kargs

    Returns
    -------
    - wrapped
        Wrapped function.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    def wrapped(
        fmt: str,
        *args: object,
        **kargs: object,
    ) -> None:
        r"""
        Wrapped function.

        Args
        ----
        - fmt
            Formatter.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Pass the given level integer.
        log(level, fmt, *args, **kargs)

    # Return the wrapped function.
    return wrapped


# Wrap a benck of log functions.
debug = wrap(DEBUG)
info1 = wrap(INFO1)
info2 = wrap(INFO2)
focus = wrap(FOCUS)
warning = wrap(WARNING)
error = wrap(ERROR)
