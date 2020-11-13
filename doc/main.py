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
import torch

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from doc.raw.text import load_texts


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main Branch >>
# Main branch starts here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


load_texts("pytorch/logging.py")