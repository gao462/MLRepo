# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Union

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
from doc.code import Code
import doc.filesys


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Document Objects >>
# Prototype of document.
# It also includes prototype for file system document and real code document.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Document(object):
    r"""
    Document prototype.
    """
    def __init__(self: Document, *args: object, **kargs: object) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Allocate notes buffer.
        self.notes_console: List[str] = []
        self.notes_markdown: List[str] = []

    def notes(self: Document, *args: object, **kargs: object) -> None:
        r"""
        Generate notes.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        This will generate notes for console and markdown in the same time.
        For most part of the notes, they will share the same Markdown syntex
        except that console notes will use ASCII color codes for some keywords.
        """
        # Prototype may not implement everything.
        error("Function is not implemented.")
        raise NotImplementedError


class FileSysDocument(Document):
    r"""
    Document for file system prototype.
    """
    # Define Github constants.
    ROOT = "MLRepo"
    GITHUB = "https://github.com/gao462/{:s}".format(ROOT)

    def __init__(
        self: Document, path: str, *args: object, **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - path
            Path of this document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Super.
        Document.__init__(self, *args, **kargs)

        # Save necessary attributes
        self.PATH = path


# Hierarchy constants.
GLOBAL = 0
CLASS = 1
FUNCTION = 2
BLOCK = 3
BRANCH = 4


class CodeDocument(Document):
    r"""
    Document for code prototype.
    """
    def __init__(
        self: CodeDocument, *args: object,
        level: int, hierarchy: int,
        superior: Union[CodeDocument, None], filedoc: doc.filesys.FileDocument,
        **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - path
            Path of its file document.
        - level
            Indent level.
        - hierarchy
            Hierarchy integer.
        - superior
            Superior code document.
        - filedoc
            Document of the file of the code.
        - **kargs

        Returns
        -------

        """
        # Super.
        Document.__init__(self, *args, **kargs)

        # Save necessary attributes.
        self.LEVEL = level
        self.HIERARCHY = hierarchy
        self.SUPERIOR = self if superior is None else superior
        self.FILEDOC = filedoc

        # Allocate children memory.
        self.allocate()

    def allocate(self: CodeDocument, *args: object, **kargs: object) -> None:
        r"""
        Allocate children memory.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Prototype may not implement everything.
        error("Function is not implemented.")
        raise NotImplementedError

    def parse(
        self: CodeDocument, code: Code, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse information into document.

        Args
        ----
        - self
        - code
            Code scanner used for parsing.
        - *args
        - **kargs

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.row = code.scan + 1