# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Dict, Tuple

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
import doc.base
import doc.block
import doc.statement
import doc.series


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


class ModuleDocument(doc.base.CodeDocument):
    r"""
    Document for module imports.
    """
    def allocate(self: ModuleDocument, *args: object, **kargs: object) -> None:
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
        # Define constant code text.
        text = (
            "# Add development library to path.\n" \
            "if (os.path.basename(os.getcwd()) == \"MLRepo\"):\n" \
            "    sys.path.append(os.path.join(\".\"))\n" \
            "else:\n" \
            "    print(\"Code must strictly work in \\\"MLRepo\\\".\")\n" \
            "    exit()"
        )

        # Modules are constant.
        self.future = doc.block.ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.typing = doc.block.ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.python = doc.block.ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.adding = doc.block.ConstBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC, constant=text,
        )
        self.logging = doc.block.ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.develop = doc.block.ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )

        # Allocate buffer to trace imports.
        self.modules: Dict[str, List[str]] = {}
        self.identifiers: Dict[str, str] = {}
        self.mapping: Dict[str, str] = {}

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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

        # Parse code.
        self.future.parse(self.code)
        self.code.blank_next(1)
        self.typing.parse(self.code)
        self.code.blank_next(1)
        self.python.parse(self.code)
        self.code.blank_next(1)
        self.adding.parse(self.code)
        self.code.blank_next(1)
        self.logging.parse(self.code)
        self.code.blank_next(1)
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
        if (self.FILEDOC.ME == "pytorch.logging"):
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

    def notes(self: ModuleDocument, *args: object, **kargs: object) -> None:
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
        self.markdown.append(
            "- Dependent on: {:s}".format(", ".join([
                "`{:s}`".format(itr) for itr in self.modules.keys()
            ])),
        )

        # Import block just integrates its children notes with blank breaks.
        self.markdown.append("")
        self.markdown.append("  > ```python")
        for child in (
            self.future, self.typing, self.python, self.adding, self.logging,
            self.develop,
        ):
            child.notes()
            for itr in child.markdown:
                if (len(itr) == 0):
                    self.markdown.append("  >")
                else:
                    self.markdown.append("  > {:s}".format(itr))
            self.markdown.append("  >")
        self.markdown[-1] = "  > ```"

        # Clear children notes for memory efficency.
        for child in (
            self.future, self.typing, self.python, self.adding, self.logging,
            self.develop,
        ):
            child.markdown.clear()


class GlobalDocument(doc.base.CodeDocument):
    r"""
    Document for global level codes.
    """
    def allocate(self: GlobalDocument, *args: object, **kargs: object) -> None:
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
        # Children are a list of introductions and sections.
        self.sections: List[Tuple[
            doc.statement.IntroDocument, doc.series.SeriesDocument,
        ]] = []

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
        doc.base.CodeDocument.parse(self, code, *args, **kargs)

        # Parse introduction and code series until EOF.
        while (not self.code.eof()):
            # Allocate and append first.
            intro = doc.statement.IntroDocument(
                level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                filedoc=self.FILEDOC,
            )
            series = doc.series.SeriesDocument(
                level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                filedoc=self.FILEDOC,
            )
            self.sections.append((intro, series))

            # Parse code.
            self.code.blank_next(2)
            intro.parse(self.code)
            self.code.blank_next(2)
            series.parse(self.code)

    def notes(self: GlobalDocument, *args: object, **kargs: object) -> None:
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
        for intro, series in self.sections:
            intro.notes()
            series.notes()
            if (first):
                first = False
            else:
                self.markdown.append("")
            self.markdown.extend(intro.markdown)
            self.markdown.append("")
            self.markdown.extend(series.markdown)

        # Clear children notes for memory efficency.
        for intro, series in self.sections:
            intro.markdown.clear()
            series.markdown.clear()