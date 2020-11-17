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
import hashlib

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << File System Operations >>
# Some file system related operations which are not provided by os.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


def ensure_dir(
    path: str,
    *args: ArgT,
    **kargs: KArgT,
) -> None:
    r"""
    Ensure existence of path directory.

    Args
    ----
    - path
        Path.
    - *args
    - **kargs

    Returns
    -------

    """
    # \
    # ANNOTATE VARIABLES
    # \
    ...

    # Create directory if it does not exist.
    if (os.path.isdir(path)):
        pass
    elif (os.path.isfile(path)):
        warning("\"{:s}\" can be both a directory and a file.", path)
    else:
        os.makedirs(path)


def md5(
    path: str,
    *args: ArgT,
    **kargs: KArgT,
) -> str:
    r"""
    Get MD5 hash.

    Args
    ----
    - path
        Path.
    - *args
    - **kargs

    Returns
    -------
    - val
        MD5 hash value.

    """
    # \
    # ANNOTATE VARIABLES
    # \
    processor: hashlib._Hash
    block_size: int
    val: str
    file: BinaryIO
    chunk: bytes

    # Get hash processor.
    processor = hashlib.md5()
    block_size = 128 * processor.block_size

    # Null file has empty hash.
    if (os.path.isfile(path)):
        pass
    else:
        return ""

    # process file chunk by chunk
    file = open(path, 'rb')
    while True:
        chunk = file.read(block_size)
        if (len(chunk) == 0):
            break
        else:
            processor.update(chunk)
    file.close()

    # Get hash value from processor.
    return processor.hexdigest()