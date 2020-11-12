# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Tuple, Union

# Import dependencies.
import sys
import os
import token
import re

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from doc.code import Code, MAX, Line
import doc.base
import doc.statement
import doc.filesys


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Function Code Document Objects >>
# Code document for function related codes.
# This only contains elements of a function, for example, arguments, returns.
# The function document itself is defined in series module.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class TypeHintDocument(doc.base.CodeDocument):
    r"""
    Document for type hint definition.
    """
    def allocate(
        self: TypeHintDocument, *args: object, **kargs: object,
    ) -> None:
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
        # Allocate children hints.
        self.children: List[TypeHintDocument] = []

    def parse(
        self: TypeHintDocument, code: Code, *args: object, **kargs: object,
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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

        # Get type name.
        obj = self.code.get()
        self.name = self.parse_type(obj)

        # Get children type hint if it exists.
        if (obj.check("[", level=self.LEVEL)):
            pass
        else:
            return

        # Match left.
        obj.match("[", level=self.LEVEL)
        if (obj.check(token.NL, level=self.LEVEL)):
            multiple = True
            obj.match(token.NL, level=self.LEVEL)
            self.code.next()
            obj = self.code.get()
            obj.reset()
        else:
            multiple = False

        # Deal with recursive hints.
        level2 = self.LEVEL + int(multiple)
        while (not self.code.eof()):
            # Right means ending.
            if (obj.check("]", level=self.LEVEL)):
                break
            else:
                pass

            # Get type hint.
            hint = TypeHintDocument(
                level=level2, hierarchy=self.HIERARCHY, superior=self,
                filedoc=self.FILEDOC,
            )
            hint.parse(self.code)
            self.children.append(hint)

            # Get break.
            if (obj.check("]", level=self.LEVEL)):
                break
            else:
                obj.match(",", level=level2)

            # May reach the end of a line.
            if (obj.check(token.NL, level=level2)):
                obj.match(token.NL, level=level2)
                self.code.next()
                obj = self.code.get()
                obj.reset()
            else:
                pass

        # Match right.
        obj.match("]", level=self.LEVEL)

    def parse_type(
        self: TypeHintDocument, line: Line, *args: object, **kargs: object,
    ) -> str:
        r"""
        Parse information (type) into document.

        Args
        ----
        - self
        - line
            A line of parsing code words.
        - *args
        - **kargs

        Returns
        -------
        - name
            Type name.

        """
        # Module is a list of names concatenated by ".".
        buf = [line.get().text]
        line.match(token.NAME, level=self.LEVEL)
        while (line.check(".", level=self.LEVEL)):
            line.match(".", level=self.LEVEL)
            buf.append(line.get().text)
            line.match(token.NAME, level=self.LEVEL)
        return ".".join(buf)

    def text(self: TypeHintDocument, *args: object, **kargs: object) -> str:
        r"""
        Get text message of type hint.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - msg
            Message.

        """
        # Get name recursively.
        if (len(self.children) > 0):
            buf = [itr.text() for itr in self.children]
            recursive = "[{:s}]".format(", ".join(buf))
        else:
            recursive = ""
        return "{:s}{:s}".format(self.name, recursive)


class ArgumentDocument(doc.base.CodeDocument):
    r"""
    Document for argument definition.
    """
    def __init__(
        self: ArgumentDocument, *args: object,
        level: int, hierarchy: int,
        superior: Union[doc.base.CodeDocument, None],
        filedoc: doc.filesys.FileDocument, multiple: bool, **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - level
            Indent level.
        - hierarchy
            Hierarchy integer.
        - superior
            Superior code document.
        - filedoc
            Document of the file of the code.
        - multiple
            If True, argument is multiple-line definition.
        - **kargs

        Returns
        -------

        """
        # Super.
        doc.base.CodeDocument.__init__(
            self, *args, level=level, hierarchy=hierarchy, superior=superior,
            filedoc=filedoc, **kargs,
        )

        # Save necessary attributes.
        self.MULTIPLE = multiple

    def allocate(
        self: ArgumentDocument, *args: object, **kargs: object,
    ) -> None:
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
        # Allocate argument buffer.
        self.items: List[Tuple[str, TypeHintDocument]] = []

    def parse(
        self: ArgumentDocument, code: Code, *args: object, **kargs: object,
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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

        # Match left.
        obj = self.code.get()
        obj.match("(", level=self.LEVEL)
        if (self.MULTIPLE):
            obj.match(token.NL, level=self.LEVEL)
            self.code.next()
            obj = self.code.get()
            obj.reset()
        else:
            pass

        # Match argument names and type hints.
        level2 = self.LEVEL + int(self.MULTIPLE)
        while (not self.code.eof()):
            # Right means ending.
            if (obj.check(")", level=self.LEVEL)):
                break
            else:
                pass

            # It is possible to have "*args" and "**kargs".
            if (obj.check("*", level=level2)):
                prefix = "*"
                obj.match("*", level=level2)
            elif (obj.check("**", level=level2)):
                prefix = "**"
                obj.match("**", level=level2)
            else:
                prefix = ""

            # Get argument name.
            suffix = obj.get().text
            obj.match(token.NAME, level=level2)
            name = prefix + suffix

            # Get type hint.
            obj.match(":", level=level2)
            hint = TypeHintDocument(
                level=level2, hierarchy=self.HIERARCHY, superior=self,
                filedoc=self.FILEDOC,
            )
            hint.parse(self.code)
            self.items.append((name, hint))

            # Get break.
            if (obj.check(")", level=self.LEVEL)):
                break
            else:
                obj.match(",", level=level2)

            # May reach the end of a line.
            if (obj.check(token.NL, level=level2)):
                obj.match(token.NL, level=level2)
                self.code.next()
                obj = self.code.get()
                obj.reset()
            else:
                pass

        # Match right.
        obj.match(")", level=self.LEVEL)