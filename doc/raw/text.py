# Import future.
from __future__ import annotations

# Import typing.
from typing import Any as VarArg
from typing import Final as Const
from typing import Tuple as MultiReturn
from typing import Type, Protocol
from typing import TextIO, BinaryIO
from typing import Union, Tuple, List, Dict, Set, Callable

# Import dependencies.
import sys
import os

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from pytorch.logging import MAX, UNIT, POSITION


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Load Text >>
# Text loading operations.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


def load_texts(
    path: str,
    *args: VarArg,
    **kargs: VarArg,
) -> List[Tuple[int, str]]:
    r"""
    Load texts as list of indented lines from a file.

    Args
    ----
    - path
        File path

    Returns
    -------
    - contents
        Texts as list of indented lines from a file.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Load and check in the meanwhile.
    file = open(path, "r")
    contents = []
    for i, line in enumerate(file):
        # Get and check line info.
        check(line, path=path, row=i + 1)
        level = indent(line, path=path, row=i + 1)
        line = line.strip()
        contents.append((level, line))
    file.close()

    # The last line can not be empty.
    if (len(contents[-1][1]) == 0):
        error(
            "File \"{:s}\", last line can not be empty.",
            POSITION.format(
                "file: {:s}, line {:d}".format(path, len(contents)),
            ),
        )
        raise RuntimeError
    else:
        pass
    return contents


def check(
    text: str,
    *args: VarArg,
    path: str, row: int,
    **kargs: VarArg,
) -> None:
    r"""
    Check raw line text.

    Args
    ----
    - text
        Raw text
    - *args
    - path
        File path
    - row
        Row ID.
    - **kargs

    Returns
    -------

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Check proper line ending.
    if (text[-1] != "\n"):
        error(
            "File \"{:s}\", line should end with \"\\n\".",
            POSITION.format("file: {:s}, line {:d}".format(path, row)),
        )
        raise RuntimeError
    else:
        pass

    # Check and remove tail blanks.
    if (len(text.rstrip()) + 1 != len(text)):
        error(
            "File \"{:s}\", line has trailing spaces.",
            POSITION.format("file: {:s}, line {:d}".format(path, row)),
        )
        raise RuntimeError
    else:
        pass

    # Check proper line length.
    if (len(text.rstrip()) > MAX):
        error(
            "File \"{:s}\", line is long.",
            POSITION.format("file: {:s}, line {:d}".format(path, row)),
        )
        raise RuntimeError
    else:
        pass

    # Clean spaces for pure text check.
    text = text.strip()

    # Check inline break.
    if (
        len(text) > 0 and text[-1] == "\\" and text != "# \\" and
        len(text) > 2 and text[-3:-1] != "\" "
    ):
        print(text)
        error(
            "File \"{:s}\", inline break \"\\\" only works for string.",
            POSITION.format("file: {:s}, line {:d}".format(path, row)),
        )
        raise RuntimeError
    else:
        pass

    # Check string consistency.
    if (chr(39) in text):
        error(
            "File \"{:s}\", string should use \"\"\" rather than \"{:s}\".",
            POSITION.format("file: {:s}, line {:d}".format(path, row)),
            chr(39),
        )
        raise RuntimeError
    else:
        pass


def indent(
    text: str,
    *args: VarArg,
    path:str, row: int,
    **kargs: VarArg,
) -> int:
    r"""
    Get row indent level.

    Args
    ----
    - text
        Raw text
    - *args
    - path
        File path
    - row
        Row ID.
    - **kargs

    Returns
    -------
    - level
        Indent level.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Get number of spaces.
    text = text.rstrip()
    num_spaces = len(text) - len(text.lstrip())
    if (num_spaces % UNIT == 0):
        return num_spaces // UNIT
    else:
        error(
            "File \"{:s}\", weird indent.",
            POSITION.format("file: {:s}, line {:d}".format(path, row)),
        )
        raise RuntimeError