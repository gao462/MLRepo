# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Dict, Union

# Import dependencies.
import sys
import os
import token

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
from doc.base import CodeDocument, Document, BRANCH, FileSysDocument
from doc.statement import CommentDocument, ImportDocument, ConstDocument


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Block Code Document Objects >>
# Code document on block level.
# There are several kinds of block documents, but they all share the same
# workflow.
#
# A block often start with several comments lines, except that in a branch with
# only one block, it may have no comments.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class BlockDocument(CodeDocument):
    r"""
    Document for a block of code prototype.
    """
    def parse(
        self: BlockDocument, code: Code, *args: object, **kargs: object,
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
        # Super.
        CodeDocument.parse(self, code, *args, **kargs)

        # Parse comment first according first word without scanning.
        self.comment = CommentDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        self.comment.parse(self.code)

        # Parse statements of the block.
        self.parse_statements()

    def parse_statements(self, *args: object, **kargs: object) -> None:
        r"""
        Parse all statements of the document.

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


class ImportBlockDocument(BlockDocument):
    r"""
    Document for a block of import code.
    """
    def parse_statements(
        self: ImportBlockDocument, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse all statements of the document.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Parsea a new document from current line.
        self.statements: List[ImportDocument] = []
        while (not self.eob()):
            child = ImportDocument(
                path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                superior=self, filedoc=self.FILEDOC,
            )
            child.parse(self.code)
            self.statements.append(child)
            self.code.next()

        # Merge all imports.
        self.modules: Dict[str, List[str]] = {}
        self.identifiers = {}
        self.mapping = {}
        for child in self.statements:
            for name, members in child.modules.items():
                if (name in self.modules):
                    pass
                else:
                    self.modules[name] = []
                self.modules[name].extend(members)
            for name, source in child.identifiers.items():
                self.identifiers[name] = source
            for rename, name in child.mapping.items():
                self.mapping[rename] = name

    def eob(self: ImportBlockDocument, *args: object, **kargs: object) -> bool:
        r"""
        Check end of the block.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            Signal for end of the block.

        """
        # A single blank line is the end.
        return self.code.blank_top(1)

    def notes(
        self: ImportBlockDocument, *args: object, **kargs: object,
    ) -> None:
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
        # Block notes is just a list of its statments notes.
        console, markdown = [], []
        if (self.comment.null):
            pass
        else:
            self.comment.notes()
            console.extend(self.comment.notes_console)
            markdown.extend(self.comment.notes_markdown)
        for itr in self.statements:
            itr.notes()
            console.extend(itr.notes_console)
            markdown.extend(itr.notes_markdown)
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        self.comment.notes_console.clear()
        self.comment.notes_markdown.clear()
        for itr in self.statements:
            itr.notes_console.clear()
            itr.notes_markdown.clear()

    def check(
        self: ImportBlockDocument, i: int, text: str, *args: object,
        **kargs: object,
    ) -> bool:
        r"""
        Check if requiring row is exactly the given text.

        Args
        ----
        - self
        - i
            Row ID.
        - text
            Requiring text.

        Returns
        -------
        - flag
            If the text is satisfied.

        This is specially defined because some imports are constantly required.

        """
        # Match directly
        return self.statements[i].memory.text == text


class ConstBlockDocument(BlockDocument):
    r"""
    Document for a block of constant code.
    """
    def __init__(
        self: ConstBlockDocument, *args: object,
        path: str, level: int, hierarchy: int,
        superior: Union[CodeDocument, None], filedoc: FileSysDocument,
        constant: str,
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
        - constant
            Constant code text.
        - **kargs

        Returns
        -------

        """
        # Super.
        BlockDocument.__init__(
            self, *args, path=path, level=level, hierarchy=hierarchy,
            superior=superior, filedoc=filedoc, **kargs,
        )

        # Save necessary attributes.
        self.CONSTANT = constant.split("\n")

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
        # Super.
        CodeDocument.parse(self, code, *args, **kargs)

        # Parse statements of the block without comments.
        self.statements = []
        for itr in self.CONSTANT:
            child = ConstDocument(
                path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                superior=self, filedoc=self.FILEDOC, constant=itr,
            )
            child.parse(self.code)
            self.statements.append(child)
            self.code.next()

        # Generate notes.
        self.notes()

    def notes(self, *args: object, **kargs: object) -> None:
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
        # Block notes is just a list of its statments notes.
        console, markdown = [], []
        for itr in self.statements:
            itr.notes()
            console.extend(itr.notes_console)
            markdown.extend(itr.notes_markdown)
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        for itr in self.statements:
            itr.notes_console.clear()
            itr.notes_markdown.clear()