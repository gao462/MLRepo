# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn

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
from doc.filesys import DirectoryDocument


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main >>
# Main branch starts from here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# Generate all notes.
doc = DirectoryDocument(os.path.abspath("."), rootdoc=None)
doc.parse()