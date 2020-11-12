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
from doc.code import Code, MAX, UNIT
import doc.base
import doc.statement
import doc.filesys
import doc.func


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

    def dedent(self: SeriesDocument, *args: object, **kargs: object) -> bool:
        r"""
        Check if a dedent is happening.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            Signal of ending of a series.
            It is equivalent to dedent at the first next non-trival line.

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

    def notes(self: SeriesDocument, *args: object, **kargs: object) -> None:
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
        first = True
        for child in self.components:
            # First item has no breaks.
            if (first):
                first = False
            else:
                self.markdown.append("")

            # Generate child notes.
            child.notes()
            self.markdown.extend(child.markdown)

        # Clear children notes for memory efficency.
        for child in self.components:
            child.markdown.clear()


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

        # Parse code.
        self.description.parse(self.code)
        self.body.parse(self.code)

    def notes(self: ClassDocument, *args: object, **kargs: object) -> None:
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
                modname = self.FILEDOC.modules.mapping[itr]
                dirpath = os.path.join(
                    self.FILEDOC.FOLDER, *modname.split(".")[:-1],
                )
                classname = self.super[len(modname) + 1:]
                break
            else:
                modname = ""
                dirpath = ""
                classname = self.super
        if (len(modname) == 0 and classname in self.FILEDOC.classes):
            modname = self.FILEDOC.ME
            dirpath = self.FILEDOC.ROOTDOC.PATH
        else:
            pass

        # Locate the super.
        if (len(modname) == 0):
            # Python class has no reference.
            link = self.super
        elif (dirpath == self.FILEDOC.ROOTDOC.PATH):
            # Get in-page reference directly.
            full = "{:s}.{:s}".format(modname, classname)
            refer = "Class: {:s}".format(full)
            refer = doc.filesys.github_header(refer)
            link = "[{:s}](#{:s})".format(full, refer)
        else:
            # Get Github page.
            raise NotImplementedError

        # Title is class name.
        self.markdown.extend(["---", ""])
        self.markdown.append("## Class: {:s}.{:s}".format(
            self.FILEDOC.ME, self.name,
        ))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
        )
        source = "{:s}#L{:d}".format(source, self.row)
        self.markdown.append("")
        self.markdown.append("- Source: [Github]({:s})".format(source))

        # Super class is required.
        self.markdown.append("")
        self.markdown.append("- Super: {:s}".format(link))

        # Put descriptions here.
        for para in self.description.title:
            self.markdown.append("")
            self.markdown.append(" ".join(para))

        # Return to TOC, file.
        self.markdown.append("")
        self.markdown.append(
            "[[TOC]](#table-of-content) [[File]](#{:s})".format(
                doc.filesys.github_header("File: {:s}".format(
                    self.FILEDOC.PATH,
                )),
            ),
        )

        # Get body note as a code block
        self.body.notes()
        buf = []
        for itr in self.body.markdown:
            if (len(itr) == 0 or itr[0] != "#"):
                buf.append(itr)
            elif (itr[3] in ("F", "B")):
                buf.append("#" + itr)
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " class can only documentize functions and blocks.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
        self.markdown.append("")
        self.markdown.append("- Members:")
        self.markdown.extend(doc.filesys.toc(buf)[2:])
        self.markdown.append("")
        self.markdown.extend(buf)

        # Clear children notes for memory efficency.
        self.body.markdown.clear()


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

        # Get the arguments.
        argdoc = doc.func.ArgumentDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC, multiple=(obj.memory[-2].text != ":"),
        )
        argdoc.parse(self.code)
        obj = self.code.get()
        obj.match("->", level=self.LEVEL)
        returndoc = doc.func.TypeHintDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        returndoc.parse(self.code)
        obj = self.code.get()
        obj.match(":", level=self.LEVEL)
        obj.match(token.NEWLINE, level=self.LEVEL)
        self.code.next()

        # Parse components.
        self.description.parse(self.code)
        self.description.review(argdoc, returndoc)
        self.body.parse(self.code)

    def notes(self: FunctionDocument, *args: object, **kargs: object) -> None:
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
        self.markdown.extend(["---", ""])
        if (self.HIERARCHY == doc.base.GLOBAL):
            self.markdown.append("## Function: {:s}.{:s}".format(
                self.FILEDOC.ME, self.name.replace("_", "\\_"),
            ))
        else:
            self.markdown.append("## Function: {:s}.{:s}.{:s}".format(
                self.FILEDOC.ME, getattr(self.SUPERIOR.SUPERIOR, "name"),
                self.name.replace("_", "\\_"),
            ))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
        )
        source = "{:s}#L{:d}".format(source, self.row)
        self.markdown.append("")
        self.markdown.append("- Source: [Github]({:s})".format(source))

        # Add description 1 here.
        for para in self.description.title:
            self.markdown.append("")
            self.markdown.append(" ".join(para))

        # Add arguments.
        self.markdown.append("")
        self.markdown.append("> **Arguments**")
        ptr = 0
        while (ptr < len(self.description.arg_names)):
            # The first argument has no breaks.
            if (ptr == 0):
                pass
            else:
                self.markdown.append(">")

            # Get name and type hint first.
            name = self.description.arg_names[ptr]
            hint = self.description.arg_hints[ptr]
            desc = self.description.arg_descs[ptr]
            ptr += 1

            # Some arguments have no attachment.
            if (name == "*args"):
                self.markdown.append("> - **{:s}**: *{:s}*".format(
                    "\\*args", hint,
                ))
            elif (name == "**kargs"):
                self.markdown.append("> - **{:s}**: *{:s}*".format(
                    "\\*\\*kargs", hint,
                ))
            else:
                self.markdown.append("> - **{:s}**: *{:s}*".format(name, hint))

            # Output argument paragraphs with indent.
            for para in desc:
                self.markdown.append(">")
                self.markdown.append(">   {:s}".format(" ".join(para)))

        # Add returns.
        self.markdown.append("")
        self.markdown.append("> **Returns**")
        ptr = 0
        while (ptr < len(self.description.return_names)):
            # The first argument has no breaks.
            if (ptr == 0):
                pass
            else:
                self.markdown.append(">")

            # Get name and type hint first.
            name = self.description.return_names[ptr]
            hint = self.description.return_hints[ptr]
            desc = self.description.return_descs[ptr]
            ptr += 1
            self.markdown.append("> - **{:s}**: *{:s}*".format(name, hint))

            # Output argument paragraphs with indent.
            for para in desc:
                self.markdown.append(">")
                self.markdown.append(">   {:s}".format(" ".join(para)))

        # Add description 2 here.
        for para in self.description.attach:
            self.markdown.append("")
            self.markdown.append(" ".join(para))

        # Get body note as a code block
        self.body.notes()
        self.markdown.append("")
        self.markdown.append("> ```python")
        for itr in self.body.markdown:
            if (len(itr) == 0):
                self.markdown.append(">")
            else:
                self.markdown.append("> {:s}".format(itr))
        self.markdown.append("> ```")

        # Return to class.
        if (self.HIERARCHY == doc.base.GLOBAL):
            class_link = ""
        else:
            holder = self.SUPERIOR.SUPERIOR
            class_link = " [[Class]](#{:s})".format(
                doc.filesys.github_header("Class: {:s}.{:s}".format(
                    holder.FILEDOC.ME, getattr(holder, "name"),
                )),
            )

        # Return to TOC, file.
        self.markdown.append("")
        self.markdown.append(
            "[[TOC]](#table-of-content) [[File]](#{:s}){:s}".format(
                doc.filesys.github_header("File: {:s}".format(
                    self.FILEDOC.PATH,
                )),
                class_link,
            ),
        )

        # Clear children notes for memory efficency.
        self.body.markdown.clear()


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
        self.memory = []
        while (True):
            if (self.code.eof() or self.code.blank_top(self.NUM_BLANKS)):
                break
            else:
                self.memory.append(self.code.get())
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
        # Get code snap with comments.
        snap = []
        self.comment.notes()
        snap.extend(self.comment.markdown)
        start = self.LEVEL * UNIT
        for com in self.memory:
            snap.append(com.text[start:])

        # Clear children notes for memory efficency.
        self.comment.markdown.clear()

        # In deep level there is no need to wrap headers.
        if (self.HIERARCHY in (doc.base.GLOBAL, doc.base.CLASS)):
            pass
        else:
            self.markdown.extend(snap)
            return

        # Get first sentence in the comment with limited length.
        title = self.comment.paragraphs[0][0]
        if (len(title) > self.MAX):
            title = title[0:self.MAX - 3].strip() + "..."
        else:
            pass
        self.markdown.extend(["---", ""])
        if (self.HIERARCHY == doc.base.GLOBAL):
            self.markdown.append("## Block: {:s}: {:s}".format(
                self.FILEDOC.ME, title,
            ))
        else:
            self.markdown.append("## Block: {:s}.{:s}: {:s}".format(
                self.FILEDOC.ME, getattr(self.SUPERIOR.SUPERIOR, "name"),
                title,
            ))

        # Super link to source code is required.
        source = os.path.join(
            self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
        )
        source = "{:s}#L{:d}".format(source, self.row)
        self.markdown.append("")
        self.markdown.append("- Source: [Github]({:s})".format(source))

        # Add code snap here.
        self.markdown.append("")
        self.markdown.append("> ```python")
        for itr in snap:
            if (len(itr) == 0):
                self.markdown.append(">")
            else:
                self.markdown.append("> {:s}".format(itr))
        self.markdown.append("> ```")

        # Return to class.
        if (self.HIERARCHY == doc.base.GLOBAL):
            class_link = ""
        else:
            holder = self.SUPERIOR.SUPERIOR
            class_link = " [[Class]](#{:s})".format(
                doc.filesys.github_header("Class: {:s}.{:s}".format(
                    holder.FILEDOC.ME, getattr(holder, "name"),
                )),
            )

        # Return to TOC, file.
        self.markdown.append("")
        self.markdown.append(
            "[[TOC]](#table-of-content) [[File]](#{:s}){:s}".format(
                doc.filesys.github_header("File: {:s}".format(
                    self.FILEDOC.PATH,
                )),
                class_link,
            ),
        )

        # Clear children notes for memory efficency.
        pass