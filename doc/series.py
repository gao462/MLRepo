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
import doc.base
import doc.statement


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


class SeriesDocument(doc.base.CodeDocument):
    r"""
    Document for a series of code.
    """
    def allocate(self: SeriesDocument, *args: object, **kargs: object) -> None:
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
        # Children are a list of classes, functions or operation blocks.
        self.components: List[Union[
            ClassDocument, FunctionDocument, OPBlockDocument,
        ]] = []

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == doc.base.GLOBAL)

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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

        # Parse components until dedent.
        first = True
        while (not self.dedent()):
            # Move blank lines first except for the first time.
            if (first):
                first = False
            else:
                self.code.blank_next(self.NUM_BLANKS)

            # Allocate according to keyword and append.
            keyword = self.code.get().memory[0]
            itr: Union[ClassDocument, FunctionDocument, OPBlockDocument]
            if (keyword.text == "class"):
                itr = ClassDocument(
                    level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                    filedoc=self.FILEDOC,
                )
            elif (keyword.text == "def"):
                itr = FunctionDocument(
                    level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                    filedoc=self.FILEDOC,
                )
            else:
                itr = OPBlockDocument(
                    level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                    filedoc=self.FILEDOC,
                )
            self.components.append(itr)

            # Parse code.
            itr.parse(self.code)

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


class ClassDocument(doc.base.CodeDocument):
    r"""
    Document for a definition of class.
    """
    def allocate(self: ClassDocument, *args: object, **kargs: object) -> None:
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
        # Hierarchy of class body is limited and may change.
        if (self.HIERARCHY == doc.base.GLOBAL):
            hierarchy = doc.base.CLASS
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " class is limited to be global level.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Children are a description and a series of codes.
        self.description = doc.statement.ClassDescDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )
        self.body = SeriesDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == doc.base.GLOBAL)

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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

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
        while (True):
            if (self.code.eof() or self.code.blank_top(self.NUM_BLANKS)):
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
        # Get imported global variables sorted by inverse length.
        knowns = sorted(
            self.FILEDOC.modules.mapping.keys(), key=lambda x: -len(x),
        )

        # Find the first variable matching the super name.
        for itr in knowns:
            if (itr in self.super):
                source = itr
                prefix = self.FILEDOC.modules.mapping[source]
                break
            else:
                source = ""
                prefix = ""
        suffix = self.super[len(source):]

        # Locate the super.
        if (len(source) == 0 and suffix in self.FILEDOC.classes):
            # Get in-page reference directly.
            refer = "Class: {:s}".format(suffix)
            refer = re.sub(r"\.", "", refer)
            refer = re.sub(r"[^\w]+", "-", refer.lower().strip())
            link = "[{:s}](#{:s})".format(self.super, refer)
        elif (len(source) == 0):
            # Python class has no reference.
            link = self.super
        else:
            # Get Github page.
            layers = (prefix + suffix).split(".")
            page = os.path.join(
                self.FILEDOC.ROOTDOC.GITHUB, "tree", "main", *layers[:-1],
            )

            # Get in-page reference.
            refer = "Class: {:s}".format(layers[-1])
            refer = re.sub(r"\.", "", refer)
            refer = re.sub(r"[^\w]+", "-", refer.lower().strip())
            link = "[{:s}]({:s}#{:s})".format(self.super, page, refer)

        # Title is class name.
        console, markdown = [], []
        console.append("#### Class: \033[32;1m{:s}\033[0m".format(self.name))
        markdown.append("#### Class: {:s}".format(self.name))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
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


class FunctionDocument(doc.base.CodeDocument):
    r"""
    Document for a definition of function.
    """
    def allocate(
        self: FunctionDocument, *args: object, **kargs: object,
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
        # Hierarchy of function body may change.
        if (self.HIERARCHY in (doc.base.GLOBAL, doc.base.CLASS)):
            hierarchy = doc.base.FUNCTION
        else:
            hierarchy = self.HIERARCHY

        # Children are a description and a series of codes.
        self.description = doc.statement.FuncDescDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )
        self.body = SeriesDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == doc.base.GLOBAL)

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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

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
        while (True):
            if (self.code.eof() or self.code.blank_top(self.NUM_BLANKS)):
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
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
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


class OPBlockDocument(doc.base.CodeDocument):
    r"""
    Document for a block of operation code.
    """
    # Define constants.
    MAX = 20

    def allocate(
        self: OPBlockDocument, *args: object, **kargs: object,
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
        # Children are a description and a block of operations.
        self.comment = doc.statement.CommentDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == doc.base.GLOBAL)

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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

        # Parse comment code.
        self.comment.parse(self.code)
        while (True):
            if (self.code.eof() or self.code.blank_top(self.NUM_BLANKS)):
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
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
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