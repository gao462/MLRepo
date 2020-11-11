# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import Union, List, Dict

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
from doc.code import Code, Line, paragraphize, UNIT, MAX, FIRST
from doc.code import paragraphize
import doc.base
import doc.filesys
import doc.func


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Statement Code Document Objects >>
# Code document for a line of statement.
# Different statement types have their own workflow, but they all save line of
# tokens belong to them for potential styled code recovery.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class CommentDocument(doc.base.CodeDocument):
    r"""
    Document for a line of comment statement.
    """
    def allocate(
        self: CommentDocument, *args: object, **kargs: object,
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
        # Allocate document memory for comment lines.
        self.memory: List[Line] = []

    def parse(
        self: CommentDocument, code: Code, *args: object, **kargs: object,
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

        # Read in all consecutive comments.
        texts = []
        while (not self.code.eof()):
            # Get current line.
            obj = self.code.get()
            obj.reset()

            # Stop for non-comment token head.
            if (obj.check(token.COMMENT, level=self.LEVEL)):
                pass
            else:
                break

            # Parse current line.
            comment = obj.get().text
            obj.match(token.COMMENT, level=self.LEVEL)
            obj.match(token.NL, level=self.LEVEL)
            texts.append(comment[2:])

            # Save and move to next line.
            self.memory.append(obj)
            self.code.next()

        # Translate parsed text into paragraphs.
        self.translate(texts)

    def translate(
        self: CommentDocument, texts: List[str], *args: object,
        **kargs: object,
    ) -> None:
        r"""
        Translate parsed text into paragraphs.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Translate parsed text into paragraphs.
        try:
            self.paragraphs = paragraphize(texts)
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

    def notes(self: CommentDocument, *args: object, **kargs: object) -> None:
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
        # Statement note is just its code lines without indents.
        console = []
        markdown = []
        start = self.LEVEL * UNIT
        for itr in self.memory:
            msg = itr.text[start:]
            console.append("\033[30;1m{:s}\033[0m".format(msg))
            markdown.append(msg)
        self.notes_console = console
        self.notes_markdown = markdown


class ImportDocument(doc.base.CodeDocument):
    r"""
    Document for a line of import statement.
    """
    def allocate(self: ImportDocument, *args: object, **kargs: object) -> None:
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
        # Save imported modules.
        self.modules: Dict[str, List[str]] = {}
        self.identifiers: Dict[str, str] = {}
        self.mapping: Dict[str, str] = {}

    def parse(
        self: ImportDocument, code: Code, *args: object, **kargs: object,
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

        # Get current line and parse according to the first word.
        obj = self.code.get()
        obj.reset()
        getattr(self, "parse_{:s}".format(obj.get().text))(obj)

        # Save the only parsed line in document memory.
        self.memory = obj

    def parse_import(
        self: ImportDocument, line: Line, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse information (import, as) into document.

        Args
        ----
        - self
        - line
            A line of parsing code words.
        - *args
        - **kargs

        Returns
        -------

        """
        # First word is fixed.
        self.type = "import"
        line.match("import", level=self.LEVEL)

        # Match the module name.
        module = self.parse_module(line)
        rename = self.parse_rename(line)
        self.append_module(module, rename)
        line.match(token.NEWLINE, level=self.LEVEL)

    def parse_from(
        self: ImportDocument, line: Line, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse information (from, import, as) into document.

        Args
        ----
        - self
        - line
            A line of parsing code words.
        - *args
        - **kargs

        Returns
        -------

        """
        # First word is fixed.
        self.type = "from"
        line.match("from", level=self.LEVEL)

        # Match the module name.
        module = self.parse_module(line)

        # Next word is fixed.
        line.match("import", level=self.LEVEL)

        # Match identifiers until the end of the line.
        first = True
        while (not line.eol()):
            if (first):
                first = False
            elif (line.check(",", level=self.LEVEL)):
                line.match(",", level=self.LEVEL)
            else:
                break
            identifier = self.parse_identifier(line)
            rename = self.parse_rename(line)
            self.append_identifier(identifier, rename, module=module)
        line.match(token.NEWLINE, level=self.LEVEL)

    def parse_module(
        self: ImportDocument, line: Line, *args: object, **kargs: object,
    ) -> str:
        r"""
        Parse information (module) into document.

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
            Module name.

        """
        # Module is a list of names concatenated by ".".
        buf = [line.get().text]
        line.match(token.NAME, level=self.LEVEL)
        while (line.check(".", level=self.LEVEL)):
            line.match(".", level=self.LEVEL)
            buf.append(line.get().text)
            line.match(token.NAME, level=self.LEVEL)
        return ".".join(buf)

    def parse_identifier(
        self: ImportDocument, line: Line, *args: object, **kargs: object,
    ) -> str:
        r"""
        Parse information (identifier) into document.

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
            Identifier name.

        """
        # Identifier is just a name.
        name = line.get().text
        line.match(token.NAME, level=self.LEVEL)
        return name

    def parse_rename(
        self: ImportDocument, line: Line, *args: object, **kargs: object,
    ) -> Union[str, None]:
        r"""
        Parse information (as) into document.

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
            Identifier name.

        """
        # First word is fixed or rename is not defined.
        if (line.check("as", level=self.LEVEL)):
            line.match("as", level=self.LEVEL)
        else:
            return None

        # Rename is just a name.
        name = line.get().text
        line.match(token.NAME, level=self.LEVEL)
        return name

    def append_module(
        self: ImportDocument, module: str, module2: Union[str, None],
        *args: object, **kargs: object,
    ) -> None:
        r"""
        Append an identifier import to document.

        Args
        ----
        - self
        - module
            Module name.
        - module2
            Module rename.
        - identifier
            Identifier name.
        - identifier2
            Identifier rename.
        - *args
        - **kargs

        Returns
        -------

        Trace module and identifier name mappings.
        There final name should be unique in the file since both are globally
        claimed.
        If collision happens, overwrite as python does.
        """
        # Trace rename of the module.
        self.modules[module] = []
        if (module2 is None):
            self.mapping[module] = module
        else:
            self.mapping[module2] = module

    def append_identifier(
        self: ImportDocument, identifier: str, identifier2: Union[str, None],
        *args: object, module: str, **kargs: object,
    ) -> None:
        r"""
        Append an identifier import to document.

        Args
        ----
        - self
        - identifier
            Identifier name.
        - identifier2
            Identifier rename.
        - *args
        - module
            Module name.
        - **kargs

        Returns
        -------

        """
        # Import module first if it has not been imported.
        if (module in self.modules):
            pass
        else:
            self.modules[module] = []

        # Trace module and rename of the identifier.
        if (identifier2 is None):
            self.identifiers[identifier] = module
        else:
            self.identifiers[identifier2] = module
        if (identifier2 is None):
            self.mapping[identifier] = identifier
        else:
            self.mapping[identifier2] = identifier

    def notes(self: ImportDocument, *args: object, **kargs: object) -> None:
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
        # Statement note is just its code lines without indents.
        start = self.LEVEL * UNIT
        console = []
        markdown = []
        msg = self.memory.text[start:]
        if (self.type == "import"):
            console.append("\033[35mimport\033[0m{:s}".format(msg[6:]))
        else:
            console.append("\033[35mfrom\033[0m{:s}".format(msg[4:]))
        markdown.append(msg)
        self.notes_console = console
        self.notes_markdown = markdown


class IntroDocument(CommentDocument):
    r"""
    Document for an introduction statement.
    """
    def translate(
        self: IntroDocument, texts: List[str], *args: object, **kargs: object,
    ) -> None:
        r"""
        Translate parsed text into paragraphs.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Head and tail are constant.
        if (
            texts[0] == "=" * (MAX - 2) and
            texts[1] == "*" * (MAX - 2) and
            texts[2] == "-" * (MAX - 2) and
            texts[-3] == "-" * (MAX - 2) and
            texts[-2] == "*" * (MAX - 2) and
            texts[-1] == "=" * (MAX - 2) and
            texts[3][0:3] == "<< " and texts[3][-3:] == " >>"
        ):
            pass
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " introduction requires constant head and tail lines.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # The first line must be the only title.
        words = texts[3][3:-3].split(" ")
        for itr in words:
            if (re.match(FIRST, itr) is None):
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " introduction requires title words to be capitalized.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
            else:
                pass
        self.title = " ".join(words)

        # Translate parsed text into paragraphs.
        try:
            self.paragraphs = paragraphize(texts[4:-3])
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

    def notes(self: IntroDocument, *args: object, **kargs: object) -> None:
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
        # Statement note is just its code lines without indents.
        console = []
        markdown = []
        console.append("### {:s}".format(self.title))
        markdown.append("### {:s}".format(self.title))
        for itr in self.paragraphs:
            console.append("")
            markdown.append("")
            console.append(" ".join(itr))
            markdown.append(" ".join(itr))
        self.notes_console = console
        self.notes_markdown = markdown


class DescriptionDocument(doc.base.CodeDocument):
    r"""
    Document for a description statement prototype.
    """
    def allocate(
        self: DescriptionDocument, *args: object, **kargs: object,
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
        # Allocate document memory for comment lines.
        self.memory: List[Line] = []
        self.descs: Dict[str, str] = {}

    def parse(
        self: DescriptionDocument, code: Code, *args: object, **kargs: object,
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

        # Get description.
        obj = self.code.get()
        obj.reset()
        text = obj.get().text
        obj.match(token.STRING, level=self.LEVEL)

        # Description always occupy multiple lines.
        while (True):
            if (obj.eol()):
                self.memory.append(obj)
                self.code.next()
                obj = self.code.get()
                obj.reset()
            elif (obj.check(token.NEWLINE, level=self.LEVEL)):
                break
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " description should occupy multiple lines without" \
                    " anything else.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
        obj.match(token.NEWLINE, level=self.LEVEL)
        self.memory.append(obj)
        self.code.next()

        # Remove indent from description.
        decoding = text.split("\n")
        for i in range(1, len(decoding)):
            if (len(decoding[i]) > 0):
                decoding[i] = decoding[i][UNIT * self.LEVEL:]
            else:
                pass

        # Description has content head and tail.
        if (decoding[0] == "r\"\"\"" and decoding[-1] == "\"\"\""):
            pass
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " description has constant head and tail",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Decode description.
        self.decode(decoding[1:-1])

    def decode(
        self: DescriptionDocument, texts: List[str], *args: object,
        **kargs: object,
    ) -> None:
        r"""
        Decode list of texts into document.

        Args
        ----
        - self
        - text
            A list of decoding texts.
        - *args
        - **kargs

        Returns
        -------

        """
        # Prototype may not implement everything.
        error("Function is not implemented.")
        raise NotImplementedError


class ClassDescDocument(DescriptionDocument):
    r"""
    Document for a description of class statement.
    """
    def decode(
        self: ClassDescDocument, texts: List[str], *args: object,
        **kargs: object,
    ) -> None:
        r"""
        Decode list of texts into document.

        Args
        ----
        - self
        - text
            A list of decoding texts.
        - *args
        - **kargs

        Returns
        -------

        """
        # Translate parsed text into paragraphs.
        try:
            self.descs["paragraphs"] = paragraphize(texts)
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError


class FuncDescDocument(DescriptionDocument):
    r"""
    Document for a description of function statement.
    """
    def decode(
        self: FuncDescDocument, texts: List[str], *args: object,
        **kargs: object,
    ) -> None:
        r"""
        Decode list of texts into document.

        Args
        ----
        - self
        - text
            A list of decoding texts.
        - *args
        - **kargs

        Returns
        -------

        """
        # Split into 4 parts by the first 3 blank lines.
        ptr = 0
        breaks = [0, 0, 0]
        for i in range(len(texts)):
            if (len(texts[i]) == 0):
                breaks[ptr] = i
                ptr += 1
                if (ptr == len(breaks)):
                    break
                else:
                    pass
            else:
                pass
        texts_1 = texts[0:breaks[0]]
        texts_args = texts[breaks[0] + 1:breaks[1]]
        texts_returns = texts[breaks[1] + 1:breaks[2]]
        texts_2 = texts[breaks[2] + 1:]

        # Translate parsed text into paragraphs.
        try:
            self.descs["paragraphs_1"] = paragraphize(texts_1)
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Translate parsed text into paragraphs.
        try:
            self.descs["paragraphs_2"] = paragraphize(texts_2)
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Save argument and return description for later review.
        self.descs["args"] = texts_args
        self.descs["returns"] = texts_returns

    def review(
        self: FuncDescDocument, argdoc: doc.func.ArgumentDocument,
        returndoc: doc.func.TypeHintDocument, *args: object, **kargs: object,
    ) -> None:
        r"""
        Review argument and return.

        Args
        ----
        - self
        - argdoc
            Argument document.
        - returndoc
            Return document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Review separately.
        self.review_args(argdoc)
        self.review_returns(returndoc)

    def review_args(
        self: FuncDescDocument, argdoc: doc.func.ArgumentDocument,
        *args: object, **kargs: object,
    ) -> None:
        r"""
        Review argument and return.

        Args
        ----
        - self
        - argdoc
            Argument document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Get texts.
        texts = self.descs["args"]

        # Argument description has constant head.
        buf = []
        if (texts[0] == "Args" and texts[1] == "----"):
            buf.extend(texts[0:2])
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " argument document has constant head.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Traverse later contents.
        ptr = 0
        texts = texts[2:]
        while (ptr < len(texts)):
            # Get argument name.
            name = texts[ptr][2:]
            ptr += 1
            attach = []
            buf.append(name)

            # Some arguments have no attachment.
            if (name in ("self", "cls", "*args", "**kargs")):
                continue
            else:
                pass

            # Get attachment.
            while (ptr < len(texts)):
                if (texts[ptr][0].isspace()):
                    pass
                else:
                    break
                attach.append(texts[ptr][UNIT:])
                ptr += 1
            try:
                attach = paragraphize(attach)
            except:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " fail to translate paragraphs.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
            buf.append(attach)

    def review_returns(
        self: FuncDescDocument, returndoc: doc.func.TypeHintDocument,
        *args: object, **kargs: object,
    ) -> None:
        r"""
        Review argument and return.

        Args
        ----
        - self
        - argdoc
            Argument document.
        - returndoc
            Return document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Get texts.
        texts = self.descs["returns"]

        # Argument description has constant head.
        buf = []
        if (texts[0] == "Returns" and texts[1] == "-------"):
            buf.extend(texts[0:2])
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " return document has constant head.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError
