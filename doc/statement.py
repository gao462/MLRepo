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
from doc.base import CodeDocument, Document, BRANCH, FileSysDocument


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


class CommentDocument(CodeDocument):
    r"""
    Document for a line of comment statement.
    """
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
        CodeDocument.parse(self, code, *args, **kargs)

        # Allocate document memory for comment lines.
        self.memory = []

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

        # Generate notes.
        self.notes()

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
        # Branch block may have no comments.
        if (len(texts) > 0):
            self.null = False
        elif (self.LEVEL == BRANCH):
            self.null = True
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " Non-branch block requires comments.",
                self.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Translate parsed text into paragraphs.
        try:
            self.paragraphs = paragraphize(texts)
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.PATH, "line {:d}".format(self.row),
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


class ImportDocument(CodeDocument):
    r"""
    Document for a line of import statement.
    """
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
        CodeDocument.parse(self, code, *args, **kargs)

        # Save imported modules
        self.modules: Dict[str, List[str]] = {}
        self.identifiers: Dict[str, str] = {}
        self.mapping: Dict[str, str] = {}

        # Get current line and parse according to the first word.
        obj = self.code.get()
        obj.reset()
        getattr(self, "parse_{:s}".format(obj.get().text))(obj)

        # Save the only parsed line in document memory.
        self.memory = obj

        # Generate notes.
        self.notes()

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

        Trace module and identifier name mappings. There final name should be
        unique in the file since both are globally claimed. If collision
        happens, overwrite as python does.

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


class ConstDocument(CodeDocument):
    r"""
    Document for a line of constant statement.
    """
    def __init__(
        self: ConstDocument, *args: object,
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
        CodeDocument.__init__(
            self, *args, path=path, level=level, hierarchy=hierarchy,
            superior=superior, filedoc=filedoc, **kargs,
        )

        # Save necessary attributes.
        self.CONSTANT = constant

    def parse(
        self: ConstDocument, code: Code, *args: object, **kargs: object,
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

        # Get current line.
        obj = self.code.get()

        # Directly match the text.
        if (obj.text == self.CONSTANT):
            pass
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " expect\n\"\"\"\n{:s}\n\"\"\", but get\n\"\"\"\n{:s}\"\"\".",
                self.PATH, "line {:d}".format(obj.row),
                self.CONSTANT, obj.text,
            )
            raise RuntimeError

        # Save the only parsed line in document memory.
        self.memory = obj

        # Generate notes.
        self.notes()

    def notes(self: ConstDocument, *args: object, **kargs: object) -> None:
        r"""
        Generate notes.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - console
            Console notes.
        - markdown
            Markdown notes.

        This will generate notes for console and markdown in the same time.
        For most part of the notes, they will share the same Markdown syntex
        except that console notes will use ASCII color codes for some keywords.

        """
        # Statement note is just its code lines without indents.
        start = self.LEVEL * UNIT
        console = []
        markdown = []
        msg = self.memory.text[start:]
        console.append(msg)
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
                self.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # The first line must be the only title.
        words = texts[3][3:-3].split(" ")
        for itr in words:
            if (re.match(FIRST, itr) is None):
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " introduction requires title words to be capitalized.",
                    self.PATH, "line {:d}".format(self.row),
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
                self.PATH, "line {:d}".format(self.row),
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