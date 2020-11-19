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
# << Message Object >>
# Message object parse a list of string lines, and decode them into:
# A paragraph which is multiple regular sentences concatenated by space.
# A math block starts and ends both by a "$$" line.
# A code block starts and ends both by a "```" line where header may be
# followed languange name.
#
# Those elements must be split by a blank line.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# Define common word regex.
NUMBER: Const = r"(0|[1-9][0-9]*)(.[0-9]+)?"
UNIT_INITIAL: Const = r"([A-Z][A-Za-z]*|{:s})".format(NUMBER)
UNIT_INSIDE: Const = r"([a-z]+|{:s}|{:s})".format(NUMBER, UNIT_INITIAL)

# Define composed word regex.
COMP_INITIAL: Const = r"({:s}(-{:s})*)".format(UNIT_INITIAL, UNIT_INSIDE)
COMP_INSIDE: Const = r"({:s}(-{:s})*)".format(UNIT_INSIDE, UNIT_INSIDE)

# Define inline specialist regex.
MATH: Const = r"$([^\\$]|\\.)+$"
CODE: Const = r"`([^\\`]|\\.)+`"
STRING: Const = r"\"([^\\\"]|\\.)*\""

# Define sentence element regex.
ELE_INITIAL: Const = r"({:s}|{:s}|{:s}|{:s})".format(
    COMP_INITIAL, MATH, CODE, STRING,
)
ELE_INSIDE: Const = r"({:s}|{:s}|{:s}|{:s})".format(
    COMP_INSIDE, MATH, CODE, STRING,
)
ELE_BREAK: Const = r"( |, )"

# Define sentence regex
PARANTHESE: Const = r"\({:s}({:s}{:s})*\)".format(
    ELE_INSIDE, ELE_BREAK, ELE_INSIDE,
)
SENTENCE: Const = r"^{:s}({:s}({:s}|{:s}))*(\.|:)$".format(
    ELE_INITIAL, ELE_BREAK, ELE_INSIDE, PARANTHESE,
)


class Line(object):
    r"""
    Line object
    """
    def __init__(
        self: Line,
        raw: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - raw
            Raw message line.
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Save necessary attributes
        self.raw = raw

        # Get purified text.
        ptr = 0
        escapes = ["\033", "[", "0", "m"]
        buf = []
        while (ptr < len(raw)):
            # Detect style ASCII
            if (raw[ptr] == "\033"):
                # Initialize escape characters.
                escapes = ["\033"]

                # Get head char.
                if (ptr + 1 < len(raw) and raw[ptr + 1] == "["):
                    pass
                else:
                    print(
                        "\033[1;4;mEscape characters require head" \
                        " \"[\"\033[0m.",
                    )
                    raise RuntimeError
                escapes.append("[")
                ptr += 1

                # Parse until tail char.
                while (ptr < len(raw) and raw[ptr] != "m"):
                    escapes.append(raw[ptr])
                    ptr += 1

                # Get tail char
                if (raw[ptr] == "m"):
                    pass
                else:
                    print(
                        "\033[1;4;mEscape characters require tail" \
                        " \"m\"\033[0m.",
                    )
                    raise RuntimeError
                escapes.append("m")
                ptr += 1
            else:
                pass

            # Get character and move to next.
            buf.append(raw[ptr])
            ptr += 1
        self.lastyle = "".join(escapes)
        self.pure = "".join(buf)

        # Get not-ending signal.
        ptr = 0
        scan = ""
        while (ptr < len(raw)):
            # Detect two-char character
            if (raw[ptr] == "\\" and ptr + 1 < len(raw)):
                scan = raw[ptr:ptr + 2]
                ptr += 2
            else:
                scan = raw[ptr]
                ptr += 1
        self.not_ending = (scan == "~")


class Message(object):
    r"""
    Message object.
    """
    def __init__(
        self: Message,
        raw: List[str],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - raw
            Raw message strings.
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode raw line strings.
        self.rawlines = [Line(itr) for itr in raw]

        # Get real lines to decode.
        ptr = 0
        memory = []
        while (ptr < len(self.rawlines)):
            memory.append(self.rawlines[ptr].raw)
            while (
                self.rawlines[ptr].not_ending and ptr + 1 < len(self.rawlines)
            ):
                ptr += 1
                memory[-1] = memory[-1] + self.rawlines[ptr].raw

        # Decode memory.
