# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Dict

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
from doc.base import CodeDocument
from doc.block import ImportBlockDocument, ConstBlockDocument
from doc.statement import IntroDocument
from doc.series import SeriesDocument


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Global Code Document Objects >>
# Code document on global level.
# It contains module import document which traces all imported modules and
# identifiers and broadcasts them to deeper code documents.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ModuleDocument(CodeDocument):
    r"""
    Document for module imports.
    """
    def parse(
        self: ModuleDocument, code: Code, *args: object, **kargs: object,
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

        # Future module import block.
        self.future = ImportBlockDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        self.future.parse(self.code)

        # A single blank line as break.
        self.code.blank_next(1)

        # Typing module import block.
        self.typing = ImportBlockDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        self.typing.parse(self.code)

        # A single blank line as break.
        self.code.blank_next(1)

        # Dependent (python) module import block.
        self.python = ImportBlockDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        self.python.parse(self.code)

        # A single blank line as break.
        self.code.blank_next(1)

        # Adding development library is a constant operation included by two
        # levels.
        text = (
            "# Add development library to path.\n" \
            "if (os.path.basename(os.getcwd()) == \"MLRepo\"):\n" \
            "    sys.path.append(os.path.join(\".\"))\n" \
            "else:\n" \
            "    print(\"Code must strictly work in \\\"MLRepo\\\".\")\n" \
            "    exit()"
        )
        self.adding = ConstBlockDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC, constant=text,
        )
        self.adding.parse(self.code)

        # A single blank line as break.
        self.code.blank_next(1)

        # Logging module import block.
        self.logging = ImportBlockDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        self.logging.parse(self.code)

        # A single blank line as break.
        self.code.blank_next(1)

        # Dependent (development) module import block.
        self.develop = ImportBlockDocument(
            path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
            superior=self, filedoc=self.FILEDOC,
        )
        self.develop.parse(self.code)

        # Some import blocks are strictly required.
        assert (
            len(self.future.comment.paragraphs) == 1 and
            len(self.future.comment.paragraphs[0]) == 1 and
            self.future.comment.paragraphs[0][0] == "Import future."
        )
        assert (
            len(self.typing.comment.paragraphs) == 1 and
            len(self.typing.comment.paragraphs[0]) == 1 and
            self.typing.comment.paragraphs[0][0] == "Import typing."
        )
        assert (
            len(self.python.comment.paragraphs) == 1 and
            len(self.python.comment.paragraphs[0]) == 1 and
            self.python.comment.paragraphs[0][0] == "Import dependencies."
        )
        assert (
            len(self.logging.comment.paragraphs) == 1 and
            len(self.logging.comment.paragraphs[0]) == 1 and
            self.logging.comment.paragraphs[0][0] == "Import logging."
        )
        assert (
            len(self.develop.comment.paragraphs) == 1 and
            len(self.develop.comment.paragraphs[0]) == 1 and
            self.develop.comment.paragraphs[0][0] == "Import dependencies."
        )

        # Some import commands are strictly required.
        assert (
            len(self.future.statements) == 1 and
            self.future.check(0, "from __future__ import annotations")
        )
        assert (
            len(self.typing.statements) > 1 and
            self.typing.check(0, "from typing import Any") and
            self.typing.check(1, "from typing import Tuple as MultiReturn")
        )

        # Some import commands are required except for some files.
        if (self.FILEDOC.me == "pytorch.logging"):
            pass
        else:
            assert (
                len(self.logging.statements) > 0 and
                self.logging.check(
                    0,
                    "from pytorch.logging import debug, info1, info2, focus" \
                    ", warning, error",
                )
            )

        # Merge all imports.
        self.modules: Dict[str, List[str]] = {}
        self.identifiers = {}
        self.mapping = {}
        for child in (
            self.future, self.typing, self.python, self.logging, self.develop,
        ):
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
        # Generate the dependencies.
        dependencies = list(self.modules.keys())
        mods_console = [
            "`\033[35m{:s}\033[0m`".format(itr) for itr in dependencies
        ]
        mods_markdown = [
            "`{:s}`".format(itr) for itr in dependencies
        ]
        console = ["- Dependent on: {:s}".format(", ".join(mods_console))]
        markdown = ["- Dependent on: {:s}".format(", ".join(mods_markdown))]

        # Import block just integrates its children notes with blank breaks.
        console.append("")
        markdown.append("")
        console.append("  > ```python")
        markdown.append("  > ```python")
        for child in (
            self.future, self.typing, self.python, self.adding, self.logging,
            self.develop,
        ):
            child.notes()
            for itr in child.notes_console:
                if (len(itr) == 0):
                    console.append("  >")
                else:
                    console.append("  > {:s}".format(itr))
            for itr in child.notes_markdown:
                if (len(itr) == 0):
                    markdown.append("  >")
                else:
                    markdown.append("  > {:s}".format(itr))
            console.append("  >")
            markdown.append("  >")
        console[-1] = "  > ```"
        markdown[-1] = "  > ```"
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        for child in (
            self.future, self.typing, self.python, self.adding, self.logging,
            self.develop,
        ):
            child.notes_console.clear()
            child.notes_markdown.clear()


class GlobalDocument(CodeDocument):
    r"""
    Document for global level codes.
    """
    def parse(
        self: GlobalDocument, code: Code, *args: object, **kargs: object,
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

        # Parse introduction and code series until EOF.
        self.sections = []
        while (not self.code.eof()):
            # Two blank lines as header.
            self.code.blank_next(2)

            # Parse introduction.
            intro = IntroDocument(
                path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                superior=self, filedoc=self.FILEDOC,
            )
            intro.parse(self.code)

            # Two blank lines as break.
            self.code.blank_next(2)

            # Parse code series.
            series = SeriesDocument(
                path=self.PATH, level=self.LEVEL, hierarchy=self.HIERARCHY,
                superior=self, filedoc=self.FILEDOC,
            )
            series.parse(self.code)
            self.sections.append((intro, series))

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
        for intro, series in self.sections:
            if (first):
                first = False
            else:
                console.append("")
                markdown.append("")
            intro.notes()
            console.extend(intro.notes_console)
            markdown.extend(intro.notes_markdown)
            console.append("")
            markdown.append("")
            series.notes()
            console.extend(series.notes_console)
            markdown.extend(series.notes_markdown)
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        for intro, series in self.sections:
            intro.notes_console.clear()
            intro.notes_markdown.clear()
            series.notes_console.clear()
            series.notes_markdown.clear()