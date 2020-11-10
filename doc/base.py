# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Union, Dict

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


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Document Prototype Objects >>
# Document prototypes are defined.
#
# Document is overall prototype, and is used for file system related things.
# CodeDocument is an inheritance of Document, but it works on tokenized code
# of an arbitrary file rather than file system.
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


# Hierarchy constants.
GLOBAL = 0
CLASS = 1
FUNCTION = 2
BLOCK = 3
BRANCH = 4


class FileSysDocument(Document):
    r"""
    Document for file system prototype.
    """
    # Define Github constants.
    ROOT = "MLRepo"
    GITHUB = "https://github.com/gao462/{:s}".format(ROOT)

    def __init__(
        self: FileSysDocument, *args: object,
        rootdoc: Union[FileSysDocument, None], **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - rootdoc
            Document for root directory.
        - **kargs

        Returns
        -------

        """
        # Super.
        Document.__init__(self, *args, **kargs)

        # Save necessary attributes.
        self.ROOTDOC = self if rootdoc is None else rootdoc

        # File system should trace definitions.
        self.classes: Dict[str, str] = {}

    def parse(
        self: FileSysDocument, path: str, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse information into document.

        Args
        ----
        - self
        - path
            Path to the document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Ensure path is relative to defined root.
        if (os.path.basename(path) == "MLRepo"):
            pass
        else:
            _, path = path.split(os.path.join(" ", self.ROOT, " ")[1:-1])
        self.path = path

        # Get module name for the file.
        self.me = self.path.replace(os.path.join(" ", " ")[1:-1], ".")
        self.me, _ = os.path.splitext(self.me)


class CodeDocument(Document):
    r"""
    Document for code prototype.
    """
    def __init__(
        self: CodeDocument, *args: object,
        path: str, level: int, hierarchy: int,
        superior: Union[CodeDocument, None], filedoc: FileSysDocument,
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
        self.PATH = path
        self.LEVEL = level
        self.HIERARCHY = hierarchy
        self.SUPERIOR = self if superior is None else superior
        self.FILEDOC = filedoc

    def parse(self, code: Code, *args: object, **kargs: object) -> None:
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