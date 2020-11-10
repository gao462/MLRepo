# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Union

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
from doc.code import Code, MAX
from doc.base import CodeDocument, GLOBAL, CLASS, FUNCTION
from doc.statement import CommentDocument


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Series Code Document Objects >>
# Code document for a series of codes.
# It works as a midterm contatenation for class definitions, function
# definitions and code blocks with the same indent level, thus it contains
# nothing in memory except a list of documents attached to it.
#
# It will mutually import with ClassDocument, FunctionDocument,
# OPBlockDocument.
# Thus, they four are aggregated together in this file.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class SeriesDocument(CodeDocument):
    r"""
    Document for a series of code.
    """
    def parse(
        self: SeriesDocument, code: Code, *args: object, **kargs: object,
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

        # Parse components until dedent.
        first = True
        num_blanks = 1 + int(self.HIERARCHY == GLOBAL)
        self.components: List[
            Union[ClassDocument, FunctionDocument, OPBlockDocument],
        ] = []
        while (not self.dedent()):
            # The first item has no breaks.
            if (first):
                first = False
            else:
                self.code.blank_next(num_blanks)

            # Get component class.
            keyword = self.code.get().memory[0]
            doc: Union[ClassDocument, FunctionDocument, OPBlockDocument]
            if (keyword.text == "class"):
                doc = ClassDocument(
                    path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                    superior=self, filedoc=self.FILEDOC,
                )
            elif (keyword.text == "def"):
                doc = FunctionDocument(
                    path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                    superior=self, filedoc=self.FILEDOC,
                )
            else:
                doc = OPBlockDocument(
                    path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                    superior=self, filedoc=self.FILEDOC,
                )

            # Create component document and parse it.
            doc.parse(code)
            self.components.append(doc)

    def dedent(self, *args: object, **kargs: object) -> bool:
        r"""
        Check if a dedent is happening.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Move the pointer to next non-trival line.
        ptr = self.code.scan
        while (True):
            # EOF is equivalent to dedent.
            if (ptr == len(self.code.memory)):
                return True
            else:
                pass

            # Fetch line and check.
            obj = self.code.memory[ptr]
            if (len(obj.memory) == 1 and obj.memory[0].check(token.NL)):
                pass
            elif (obj.text == "# " + "=" * (MAX - 2)):
                # Introduction is a  special stop signal for series.
                return True
            else:
                break

            # Move to next.
            ptr += 1
        return self.code.memory[ptr].level < self.LEVEL

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
        first = True
        for itr in self.components:
            if (first):
                first = False
            else:
                console.append("")
                markdown.append("")
            itr.notes()
            console.extend(itr.notes_console)
            markdown.extend(itr.notes_markdown)
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        for itr in self.components:
            itr.notes_console.clear()
            itr.notes_markdown.clear()


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Class Code Document Objects >>
# Code document for a definition of class.
# It can mutually import with SeriesDocument, thus it is put in this file.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ClassDocument(CodeDocument):
    r"""
    Document for a definition of class.
    """
    def parse(
        self: ClassDocument, code: Code, *args: object, **kargs: object,
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

        # Hierarchy of class body may change.
        if (self.HIERARCHY == GLOBAL, CLASS):
            hierarchy = CLASS
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " class is limited to be global level.",
                self.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Get the class name.
        obj = self.code.get()
        obj.reset()
        obj.match("class", level=self.LEVEL)
        self.name = obj.get().text
        obj.match(token.NAME, level=self.LEVEL)

        # Get the super name.
        obj.match("(", level=self.LEVEL)
        buf = [obj.get().text]
        obj.match(token.NAME, level=self.LEVEL)
        while (obj.check(".", level=self.LEVEL)):
            obj.match(".", level=self.LEVEL)
            buf.append(obj.get().text)
            obj.match(token.NAME, level=self.LEVEL)
        self.super = ".".join(buf)
        obj.match(")", level=self.LEVEL)
        obj.match(":", level=self.LEVEL)
        obj.match(token.NEWLINE, level=self.LEVEL)
        self.code.next()

        # Parse components.
        self.body = SeriesDocument(
            path=self.PATH, level=self.LEVEL + 1, hierarchy=hierarchy,
            superior=self, filedoc=self.FILEDOC,
        )
        num_blanks = 1 + int(self.HIERARCHY == GLOBAL)
        while (True):
            if (self.code.eof() or self.code.blank_top(num_blanks)):
                break
            else:
                self.code.next()

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
        # Search for the super location.
        if (self.super in self.FILEDOC.modules.identifiers):
            # Get Github page.
            layers = self.FILEDOC.modules.identifiers[self.super].split(".")
            page = os.path.join(
                self.FILEDOC.GITHUB, "tree", "main", *layers[:-1],
            )

            # Get in-page reference.
            refer = "Class: {:s}".format(self.super)
            refer = re.sub(r"\.", "", refer)
            refer = re.sub(r"[^\w]+", "-", refer.lower().strip())
            link = "[{:s}]({:s}#{:s})".format(self.super, page, refer)
        elif (self.super in self.FILEDOC.classes):
            # Get in-page reference directly.
            refer = "Class: {:s}".format(self.super)
            refer = re.sub(r"\.", "", refer)
            refer = re.sub(r"[^\w]+", "-", refer.lower().strip())
            link = "[{:s}](#{:s})".format(self.super, refer)
        else:
            link = self.super

        # Title is class name.
        console, markdown = [], []
        console.append("#### Class: \033[32;1m{:s}\033[0m".format(self.name))
        markdown.append("#### Class: {:s}".format(self.name))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.path,
        )
        source = "{:s}#L{:d}".format(source, self.row)
        console.append("")
        markdown.append("")
        console.append("- Source: [Github]({:s})".format(source))
        markdown.append("- Source: [Github]({:s})".format(source))

        # Super class is required.
        console.append("")
        markdown.append("")
        console.append("- Super: \033[32m{:s}\033[0m".format(self.super))
        markdown.append("- Super: {:s}".format(link))

        # Block notes is just a list of its statments notes.
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        pass


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Function Code Document Objects >>
# Code document for a definition of function.
# It can mutually import with SeriesDocument, thus it is put in this file.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class FunctionDocument(CodeDocument):
    r"""
    Document for a definition of function.
    """
    def parse(
        self: FunctionDocument, code: Code, *args: object, **kargs: object,
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

        # Hierarchy of class body may change.
        if (self.HIERARCHY in (GLOBAL, CLASS)):
            hierarchy = FUNCTION
        else:
            hierarchy = self.HIERARCHY

        # Get the function name.
        obj = self.code.get()
        obj.reset()
        obj.match("def", level=self.LEVEL)
        self.name = obj.get().text
        obj.match(token.NAME, level=self.LEVEL)

        # Get the super name.
        obj.match("(", level=self.LEVEL)
        while (not obj.check(")", level=self.LEVEL)):
            obj.next()
            if (obj.eol()):
                self.code.next()
                obj = self.code.get()
                obj.reset()
            else:
                pass
        obj.match(")", level=self.LEVEL)
        obj.match("->", level=self.LEVEL)
        while (not obj.check(":", level=self.LEVEL)):
            obj.next()
            if (obj.eol()):
                self.code.next()
                obj = self.code.get()
                obj.reset()
            else:
                pass
        obj.match(":", level=self.LEVEL)
        obj.match(token.NEWLINE, level=self.LEVEL)
        self.code.next()

        # Parse components.
        self.body = SeriesDocument(
            path=self.PATH, level=self.LEVEL + 1, hierarchy=hierarchy,
            superior=self, filedoc=self.FILEDOC,
        )
        num_blanks = 1 + int(self.HIERARCHY == GLOBAL)
        while (True):
            if (self.code.eof() or self.code.blank_top(num_blanks)):
                break
            else:
                self.code.next()

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
        # Title is function name.
        console, markdown = [], []
        console.append(
            "#### Function: \033[34;1m{:s}\033[0m".format(self.name),
        )
        markdown.append("#### Function: {:s}".format(self.name))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.path,
        )
        source = "{:s}#L{:d}".format(source, self.row)
        console.append("")
        markdown.append("")
        console.append("- Source: [Github]({:s})".format(source))
        markdown.append("- Source: [Github]({:s})".format(source))

        # Block notes is just a list of its statments notes.
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        pass


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Operation Block Code Document Objects >>
# Code document for a block of operation code.
# It can mutually import with SeriesDocument, thus it is put in this file.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class OPBlockDocument(CodeDocument):
    r"""
    Document for a block of operation code.
    """
    # Define constants.
    MAX = 20

    def parse(
        self: OPBlockDocument, code: Code, *args: object, **kargs: object,
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

        # Parse components.
        self.body = SeriesDocument(
            path=self.PATH, level=self.LEVEL + 1, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        num_blanks = 1 + int(self.HIERARCHY == GLOBAL)
        while (True):
            if (self.code.eof() or self.code.blank_top(num_blanks)):
                break
            else:
                self.code.next()

    def notes(self: OPBlockDocument, *args: object, **kargs: object) -> None:
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
        # Get first sentence in the comment.
        title = self.comment.paragraphs[0][0]
        if (len(title) > self.MAX):
            title = title[0:self.MAX - 3] + "..."
        else:
            pass

        # Title is block comment with limited length.
        console, markdown = [], []
        console.append("#### Block: \033[30;1m{:s}\033[0m".format(title))
        markdown.append("#### Block: {:s}".format(title))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.path,
        )
        source = "{:s}#L{:d}".format(source, self.row)
        console.append("")
        markdown.append("")
        console.append("- Source: [Github]({:s})".format(source))
        markdown.append("- Source: [Github]({:s})".format(source))

        # Block notes is just a list of its statments notes.
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        pass