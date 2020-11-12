# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Union, Dict, Tuple

# Import dependencies.
import sys
import os
import re
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
from doc.code import Code, Line
from doc.code import MAX, UNIT, FIRST
from doc.code import paragraphize


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Document Objects >>
# Prototype of document.
# It also includes prototype for file system document and real code document.
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
        self.markdown: List[str] = []

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


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << File System Document Objects >>
# Documentize tokenized code files, and check style rules in the meanwhile.
#
# In this level, a document directory controller will traverse every folder in
# MLRepo.
# At each folder, controller will identify all python files, and generate their
# markdown notes by their file controllers.
# Generated notes is then merged into README file inside current directory.
#
# In the README file, super links to exact Github code position are also
# created for global or global-class level classes, functions, and blocks.
# Styled code snaps for those parts are also attached with them.
#
# For function or class inside a function, local-class or branch-of-block, it
# will be compressed into its name definition.
# Arguments or codes of it will be replaced by "..." which can be used as
# python ellipsis for code.
#
# After the generation, a strict description matching is applied on classes
# with inheritance relationships so that inherited classes only extends
# function argument names and description details of inheriting classes.
# This also autofills the exact Github code positions for module imports and
# classes.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class FileSysDocument(Document):
    r"""
    Document for file system prototype.
    """
    # Define Github constants.
    PROJECT = "MLRepo"
    FOLDER = "/u/antor/u12/gao462/{:s}".format(PROJECT)
    GITHUB = "https://github.com/gao462/{:s}".format(PROJECT)

    def __init__(
        self: Document, path: str, *args: object, **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - path
            Path of this document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Super.
        Document.__init__(self, *args, **kargs)

        # Save necessary attributes
        self.PATH = path


class DirectoryDocument(FileSysDocument):
    r"""
    Document for a directory.
    """
    def __init__(
        self: DirectoryDocument, path: str, *args: object,
        rootdoc: Union[DirectoryDocument, None], **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - path
            Path of this document.
        - *args
        - rootdoc
            Document for root directory.
        - **kargs

        Returns
        -------

        """
        # Super.
        FileSysDocument.__init__(self, path, *args, **kargs)

        # Save necessary attributes.
        self.ROOTDOC = self if rootdoc is None else rootdoc

        # File system should trace definitions.
        self.classes: Dict[str, str] = {}
        self.classdocs: Dict[str, ClassDocument] = {}

    def parse(self: DirectoryDocument, *args: object, **kargs: object) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Traverse the tree.
        self.subdirs = []
        self.files = []
        for itr in os.listdir(self.PATH):
            itr = os.path.join(self.PATH, itr)
            if (os.path.isdir(itr)):
                base = os.path.basename(itr)
                if (base == "__pycache__"):
                    # Some directory name should be ignored.
                    pass
                elif (base[0] == "."):
                    # Hidden directory should be ignored.
                    pass
                else:
                    dirdoc = DirectoryDocument(itr, rootdoc=self.ROOTDOC)
                    dirdoc.parse()
                    self.subdirs.append(dirdoc)
            elif (os.path.isfile(itr)):
                base, ext = os.path.splitext(itr)
                base = os.path.basename(base)
                if (ext == ".py"):
                    if (base == "__init__"):
                        warning("Skip \"{:s}\" for now.".format(itr))
                    else:
                        filedoc = FileDocument(itr, rootdoc=self)
                        filedoc.parse()
                        self.files.append(filedoc)
                elif (ext in (".md", ".sh")):
                    # Some extension name should be ignored.
                    pass
                elif (base == ".gitignore"):
                    # Some no-extension file should be ignored.
                    pass
                else:
                    error(
                        "At \"{:s}\", expect a python/Markdown/bash/Git file.",
                        itr,
                    )
                    raise RuntimeError
            else:
                error(
                    "At \"{:s}\", expect a directory/file.",
                    itr,
                )
                raise RuntimeError

        # Register all definitions from documents in the tree.
        self.register()

        # Root specific operations.
        if (self.PATH == self.FOLDER):
            self.root()
        else:
            pass

    def register(
        self: DirectoryDocument, *args: object, **kargs: object,
    ) -> None:
        r"""
        Register definitions.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Register definitions from sub directories.
        for dirdoc in self.subdirs:
            for key, location in dirdoc.classes.items():
                self.classes[key] = location
            for key, holder in dirdoc.classdocs.items():
                self.classdocs[key] = holder

        # Register definitions from files.
        for filedoc in self.files:
            for key, row in filedoc.classes.items():
                location = "{:s}/blob/master/{:s}{:s}".format(
                    self.GITHUB, filedoc.PATH, row,
                )
                self.classes["{:s}.{:s}".format(filedoc.ME, key)] = location
            for key, holder in filedoc.classdocs.items():
                self.classdocs["{:s}.{:s}".format(filedoc.ME, key)] = holder

    def notes(self: DirectoryDocument, *args: object, **kargs: object) -> None:
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
        # Generate sub directory notes.
        for dirdoc in self.subdirs:
            dirdoc.notes()

        # Generate file notes
        for filedoc in self.files:
            filedoc.notes()
            self.markdown.extend(["", "---", ""])
            self.markdown.extend(filedoc.markdown)

        # Generate table of content.
        self.markdown = toc(self.markdown) + self.markdown

        # Save markdown note as README.
        file = open(os.path.join(self.PATH, "README.md"), "w")
        file.write("\n".join(self.markdown))
        file.close()

        # Clear children notes for memory efficency.
        for filedoc in self.files:
            filedoc.markdown.clear()

    def root(self: DirectoryDocument, *args: object, **kargs: object) -> None:
        r"""
        Root specific operations.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Generate notes.
        self.notes()


class FileDocument(FileSysDocument):
    r"""
    Document for a file.
    """
    def __init__(
        self: FileDocument, path: str, *args: object,
        rootdoc: Union[DirectoryDocument, None], **kargs: object,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - path
            Path of this document.
        - *args
        - rootdoc
            Document for root directory.
        - **kargs

        Returns
        -------

        """
        # Super.
        FileSysDocument.__init__(self, path, *args, **kargs)

        # Save necessary attributes.
        self.ROOTDOC = self if rootdoc is None else rootdoc

        # Get module path from file path.
        _, self.PATH = self.PATH.split(self.FOLDER)
        self.PATH = self.PATH[1:]
        self.ME = self.PATH.replace(os.path.join(" ", " ")[1:-1], ".")
        self.ME, _ = os.path.splitext(self.ME)

        # File system should trace definitions.
        self.classes: Dict[str, str] = {}
        self.classdocs: Dict[str, ClassDocument] = {}

        # Set code to parse on.
        self.code = Code()

        # File document has a module-import document and a global document.
        self.modules = ModuleDocument(
            path=self.PATH, level=0, hierarchy=GLOBAL,
            superior=None, filedoc=self,
        )
        self.sections = GlobalDocument(
            path=self.PATH, level=0, hierarchy=GLOBAL,
            superior=None, filedoc=self,
        )

    def parse(self: FileDocument, *args: object, **kargs: object) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Load tokenized code and parse it.
        self.code.load_file(self.PATH)
        self.code.reset()
        self.modules.parse(self.code)
        self.sections.parse(self.code)

        # Register classes.
        self.register_classes()

    def register_classes(
        self: FileDocument, *args: object, **kargs: object,
    ) -> None:
        r"""
        Register defined classes for later consistency check.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Register defined classes.
        self.classes = {}
        for _, section in self.sections.sections:
            for component in section.components:
                if (isinstance(component, ClassDocument)):
                    self.classes[component.name] = "#L{:d}".format(
                        component.row,
                    )
                    self.classdocs[component.name] = component
                else:
                    pass

    def notes(self: FileDocument, *args: object, **kargs: object) -> None:
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
        # Extend notes by global sections.
        self.sections.notes()
        self.markdown.extend(self.sections.markdown)

        # Extend notes by module imports.
        self.modules.notes()

        # Generate file header and TOC.
        index = [""] + toc(self.markdown)[2:]
        self.markdown = index + [""] + self.markdown
        self.markdown = ["## File: {:s}".format(self.PATH)] + self.markdown

        # Clear children notes for memory efficency.
        self.sections.markdown.clear()
        self.modules.markdown.clear()


def toc(notes: List[str], *args: object, **kargs: object) -> List[str]:
    r"""
    Generate table of content from given notes.

    Args
    ----
    - notes
        Notes.
    - *args
    - **kargs

    Returns
    -------
    - toc
        Notes for table of content.

    """
    # Registrate all headers by Github header reference behavior.
    headers: List[Tuple[int, str, str]] = []
    has_file = False
    has_section = False
    for itr in notes:
        # Header level matters.
        level = 0
        while (level < len(itr) and itr[level] == "#"):
            level += 1
        if (level == 0):
            continue
        else:
            pass

        # Get header text.
        text = itr[level + 1:]
        refer = text

        # Github reference ignores colorful ASCII even in console.
        refer = re.sub(r"\033\[[^m]+m", "", refer)
        refer = github_header(refer)
        headers.append((level, text, refer))
        if (len(refer) > 5 and refer[0:5] == "file-"):
            has_file = True
        elif (len(refer) > 8 and refer[0:8] == "section-"):
            has_section = True
        else:
            pass

    # Generate TOC.
    toc = ["## Table Of Content", ""]
    for level, text, refer in headers:
        num = level - 2
        if (len(refer) > 5 and refer[0:5] == "file-"):
            pass
        elif (len(refer) > 8 and refer[0:8] == "section-"):
            num += int(has_file)
        else:
            num += (int(has_file) + int(has_section))
        indent = "  " * num
        link = "{:s}* [{:s}](#{:s})".format(indent, text, refer)
        toc.append(link)
    return toc


def github_header(text: str, *args: object, **kargs: object) -> str:
    r"""
    Get a Github header reference.

    Args
    ----
    - text
        Header text.
    - *args
    - **kargs

    Returns
    -------
    - refer
        Reference text.

    """
    # Github reference ignores "." or "/".
    refer = text
    refer = re.sub(r"(\.|/)", "", refer).strip()

    # Github reference replaces escape characters.
    refer = re.sub(r"\\_", "_", refer)

    # Github reference should be lower case concatenated by "-".
    refer = re.sub(r"[^\w]+", "-", refer.lower())
    return refer


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Code Code Document Objects >>
# Code document on codes of in a file.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# Hierarchy constants.
GLOBAL = 0
CLASS = 1
FUNCTION = 2
BLOCK = 3
BRANCH = 4


class CodeDocument(Document):
    r"""
    Document for code prototype.
    """
    def __init__(
        self: CodeDocument, *args: object,
        level: int, hierarchy: int,
        superior: Union[CodeDocument, None], filedoc: FileDocument,
        **kargs: object,
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
        - **kargs

        Returns
        -------

        """
        # Super.
        Document.__init__(self, *args, **kargs)

        # Save necessary attributes.
        self.LEVEL = level
        self.HIERARCHY = hierarchy
        self.SUPERIOR = self if superior is None else superior
        self.FILEDOC = filedoc

        # Allocate children memory.
        self.allocate()

    def allocate(self: CodeDocument, *args: object, **kargs: object) -> None:
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
        # Prototype may not implement everything.
        error("Function is not implemented.")
        raise NotImplementedError

    def parse(
        self: CodeDocument, code: Code, *args: object, **kargs: object,
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
        # Save necessary attributes.
        self.code = code
        self.row = code.scan + 1


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
        self.future = ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.typing = ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.python = ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.adding = ConstBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC, constant=text,
        )
        self.logging = ImportBlockDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.develop = ImportBlockDocument(
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
        CodeDocument.parse(self, code, *args, **kargs)

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


class GlobalDocument(CodeDocument):
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
        self.sections: List[Tuple[IntroDocument, SeriesDocument]] = []

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
        while (not self.code.eof()):
            # Allocate and append first.
            intro = IntroDocument(
                level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                filedoc=self.FILEDOC,
            )
            series = SeriesDocument(
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
            intro.notes()
            series.markdown.clear()


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
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)

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


class ClassDocument(CodeDocument):
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
        if (self.HIERARCHY == GLOBAL):
            hierarchy = CLASS
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " class is limited to be global level.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Children are a description and a series of codes.
        self.description = ClassDescDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )
        self.body = SeriesDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)

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
            getattr(self.FILEDOC.ROOTDOC, "classes").keys(),
            key=lambda x: -len(x),
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
            refer = github_header(refer)
            link = "[{:s}](#{:s})".format(full, refer)
        else:
            # Get Github page.
            print(dirpath, modname, classname)
            raise NotImplementedError

        # Check inheritance.
        if (len(modname) > 0):
            full = "{:s}.{:s}".format(modname, classname)
            superdoc = getattr(self.FILEDOC.ROOTDOC, "classdocs")[full]
            self.check_inheritance(
                superdoc,
                myname="{:s}.{:s}".format(self.FILEDOC.ME, self.name),
                suname=full,
            )
        else:
            pass

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
                github_header("File: {:s}".format(
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
        self.markdown.extend(toc(buf)[2:])
        self.markdown.append("")
        self.markdown.extend(buf)

        # Clear children notes for memory efficency.
        self.body.markdown.clear()

    def check_inheritance(
        self: ClassDocument, superdoc: ClassDocument, *args: object,
        myname: str, suname: str, **kargs: object,
    ) -> None:
        r"""
        Ensure inheritance.

        Args
        ----
        - self
        - superdoc
            Document of super class.
        - *args
        - myname
            Focusing class name.
        - suname
            Super class name.
        - **kargs

        Returns
        -------

        """
        # Get functions of mine.
        self.myfuncs = {}
        for component in self.body.components:
            if (isinstance(component, FunctionDocument)):
                self.myfuncs[component.name] = component
            else:
                pass

        # Get functions of super.
        self.sufuncs = {}
        for component in superdoc.body.components:
            if (isinstance(component, FunctionDocument)):
                self.sufuncs[component.name] = component
            else:
                pass

        # Get override items.
        override = list(set(self.myfuncs.keys()) & set(self.sufuncs.keys()))

        # Get inheritance checking items.
        for itr in override:
            func_consistency(
                self.myfuncs[itr], su=self.sufuncs[itr], myname=myname,
                suname=suname,
            )


def func_consistency(
    my: FunctionDocument, *args: object, su: FunctionDocument,
    myname: str, suname: str, **kargs: object,
) -> None:
    r"""
    Ensure consistency.

    Args
    ----
    - my
        Focusing class function document.
    - *args
    - su
        Super class function document.
    - myname
        Focusing class name.
    - suname
        Super class name.
    - **kargs

    Returns
    -------

    """
    # Get esssential items.
    my_title = my.description.title
    my_arg_names = my.description.arg_names
    my_arg_descs = my.description.arg_descs
    my_ret_names = my.description.return_names
    my_ret_descs = my.description.return_descs
    my_attach = my.description.attach
    su_title = su.description.title
    su_arg_names = su.description.arg_names
    su_arg_descs = su.description.arg_descs
    su_ret_names = su.description.return_names
    su_ret_descs = su.description.return_descs
    su_attach = su.description.attach

    # Super texts should be a subset of my texts.
    if (is_subparagraphs(su_title, my_title)):
        pass
    else:
        error(
            "Title text of \"{:s}.{:s}\" should a subset of" \
            " \"{:s}.{:s}\".",
            myname, my.name, suname, su.name,
        )
        raise RuntimeError
    if (is_subparagraphs(su_attach, my_attach)):
        pass
    else:
        error(
            "Attached text of \"{:s}.{:s}\" should a subset of" \
            " \"{:s}.{:s}\".",
            myname, my.name, suname, su.name,
        )
        raise RuntimeError

    # Break ordered and keyword things.
    my_arg_break = order_key_argbreak(my_arg_names)
    su_arg_break = order_key_argbreak(su_arg_names)
    my_argord_names = my_arg_names[:my_arg_break - 1]
    my_argkey_names = my_arg_names[my_arg_break + 1:-1]
    my_argord_descs = my_arg_descs[:my_arg_break - 1]
    my_argkey_descs = my_arg_descs[my_arg_break + 1:-1]
    su_argord_names = su_arg_names[:my_arg_break - 1]
    su_argkey_names = su_arg_names[my_arg_break + 1:-1]
    su_argord_descs = su_arg_descs[:my_arg_break - 1]
    su_argkey_descs = su_arg_descs[my_arg_break + 1:-1]

    # Arguments and returns should also be subsets.
    if (is_subdefs(
        su_argord_names, my_argord_names,
        su_argord_descs, my_argord_descs,
    )):
        pass
    else:
        error(
            "Ordered argument of \"{:s}.{:s}\" should a subset of" \
            " \"{:s}.{:s}\".",
            myname, my.name, suname, su.name,
        )
        raise RuntimeError
    if (is_subdefs(
        su_argkey_names, my_argkey_names,
        su_argkey_descs, my_argkey_descs,
    )):
        pass
    else:
        error(
            "Keyword argument of \"{:s}.{:s}\" should a subset of" \
            " \"{:s}.{:s}\".",
            myname, my.name, suname, su.name,
        )
        raise RuntimeError
    if (is_subdefs(
        su_ret_names, my_ret_names,
        su_ret_descs, my_ret_descs,
    )):
        pass
    else:
        error(
            "Return of \"{:s}.{:s}\" should a subset of" \
            " \"{:s}.{:s}\".",
            myname, my.name, suname, su.name,
        )
        raise RuntimeError


def is_subparagraphs(
    small: List[List[str]], large: List[List[str]],
    *args: object, **kargs: object,
) -> bool:
    r"""
    Is a subset list of paragraphs.

    Args
    ----
    - small
        Smaller paragraphs.
    - large
        Larger paragraphs.
    - *args
    - **kargs

    Returns
    -------
    - flag
        If True, smaller one is subset of larger one.

    """
    # Check line by line.
    for i in range(len(small)):
        if (i < len(large) and " ".join(small[i]) == " ".join(large[i])):
            pass
        else:
            return False
    return True


def is_subdefs(
    small1: List[str], large1: List[str],
    small2: List[List[List[str]]], large2: List[List[List[str]]],
    *args: object, **kargs: object,
) -> bool:
    r"""
    Is a subset list of paragraphs.

    Args
    ----
    - small1
        Smaller names.
    - large1
        Larger names.
    - small2
        Smaller paragraphs.
    - large2
        Larger paragraphs.
    - *args
    - **kargs

    Returns
    -------
    - flag
        If True, smaller one is subset of larger one.

    """
    # Check name by name.
    for i in range(len(small1)):
        if (i < len(large1) and small1[i] == large1[i]):
            if (is_subparagraphs(small2[i], large2[i])):
                pass
            else:
                return False
        else:
            return False
    return True


def order_key_argbreak(
    names: List[str], *args: object, **kargs: object,
) -> int:
    r"""
    Break position between ordered and keyword arguments

    Args
    ----
    - names
        Argument names.
    - *args
    - **kargs

    Returns
    -------
    - i
        Break index.

    """
    # Traverse to find.
    for i, itr in enumerate(names):
        if (itr == "*args"):
            return i
        else:
            pass
    return len(names)


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
        if (self.HIERARCHY in (GLOBAL, CLASS)):
            hierarchy = FUNCTION
        else:
            hierarchy = self.HIERARCHY

        # Children are a description and a series of codes.
        self.description = FuncDescDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )
        self.body = SeriesDocument(
            level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
            filedoc=self.FILEDOC,
        )

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)

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

        # Get the function name.
        obj = self.code.get()
        obj.reset()
        obj.match("def", level=self.LEVEL)
        self.name = obj.get().text
        obj.match(token.NAME, level=self.LEVEL)

        # Get the arguments.
        argdoc = ArgumentDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC, multiple=(obj.memory[-2].text != ":"),
        )
        argdoc.parse(self.code)
        obj = self.code.get()
        obj.match("->", level=self.LEVEL)
        returndoc = TypeHintDocument(
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
        # In deep level there is no need to provide details.
        if (self.HIERARCHY in (GLOBAL, CLASS)):
            pass
        else:
            self.markdown.append("def {:s}(...):".format(self.name))
            self.markdown.append("{:s}...;".format(" " * UNIT))
            return

        # Title is function name.
        self.markdown.extend(["---", ""])
        if (self.HIERARCHY == GLOBAL):
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
                self.markdown.append("> - *{:s}*: `{:s}`".format(
                    "\\*args", hint,
                ))
            elif (name == "**kargs"):
                self.markdown.append("> - *{:s}*: `{:s}`".format(
                    "\\*\\*kargs", hint,
                ))
            else:
                self.markdown.append("> - *{:s}*: `{:s}`".format(name, hint))

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
            self.markdown.append("> - *{:s}*: `{:s}`".format(name, hint))

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
        if (self.HIERARCHY == GLOBAL):
            class_link = ""
        else:
            holder = self.SUPERIOR.SUPERIOR
            class_link = " [[Class]](#{:s})".format(
                github_header("Class: {:s}.{:s}".format(
                    holder.FILEDOC.ME, getattr(holder, "name"),
                )),
            )

        # Return to TOC, file.
        self.markdown.append("")
        self.markdown.append(
            "[[TOC]](#table-of-content) [[File]](#{:s}){:s}".format(
                github_header("File: {:s}".format(
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


class OPBlockDocument(CodeDocument):
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
        self.comment = CommentDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )

        # Number of blank breaks is based on hierarchy.
        self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)

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
        if (self.HIERARCHY in (GLOBAL, CLASS)):
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
        if (self.HIERARCHY == GLOBAL):
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
        if (self.HIERARCHY == GLOBAL):
            class_link = ""
        else:
            holder = self.SUPERIOR.SUPERIOR
            class_link = " [[Class]](#{:s})".format(
                github_header("Class: {:s}.{:s}".format(
                    holder.FILEDOC.ME, getattr(holder, "name"),
                )),
            )

        # Return to TOC, file.
        self.markdown.append("")
        self.markdown.append(
            "[[TOC]](#table-of-content) [[File]](#{:s}){:s}".format(
                github_header("File: {:s}".format(
                    self.FILEDOC.PATH,
                )),
                class_link,
            ),
        )

        # Clear children notes for memory efficency.
        pass


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


class TypeHintDocument(CodeDocument):
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
        CodeDocument.parse(self, code, *args, **kargs)

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


class ArgumentDocument(CodeDocument):
    r"""
    Document for argument definition.
    """
    def __init__(
        self: ArgumentDocument, *args: object,
        level: int, hierarchy: int,
        superior: Union[CodeDocument, None], filedoc: FileDocument,
        multiple: bool, **kargs: object,
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
        CodeDocument.__init__(
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
        CodeDocument.parse(self, code, *args, **kargs)

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
    def allocate(
        self: BlockDocument, *args: object, **kargs: object,
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
        # Block ususally start with a comment, then statements.
        self.comment = CommentDocument(
            level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
            filedoc=self.FILEDOC,
        )
        self.allocate_statements()

    def allocate_statements(
        self: BlockDocument, *args: object, **kargs: object,
    ) -> None:
        r"""
        Allocate statement children memory.

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

        # Parse code.
        self.comment.parse(self.code)
        self.parse_statements()

    def parse_statements(
        self: BlockDocument, *args: object, **kargs: object,
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
        # Prototype may not implement everything.
        error("Function is not implemented.")
        raise NotImplementedError


class ImportBlockDocument(BlockDocument):
    r"""
    Document for a block of import code.
    """
    def allocate_statements(
        self: ImportBlockDocument, *args: object, **kargs: object,
    ) -> None:
        r"""
        Allocate statement children memory.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Import block only has import statements.
        self.statements: List[ImportDocument] = []

        # Save imported modules.
        self.modules: Dict[str, List[str]] = {}
        self.identifiers: Dict[str, str] = {}
        self.mapping: Dict[str, str] = {}

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
        while (not self.eob()):
            child = ImportDocument(
                level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
                filedoc=self.FILEDOC,
            )
            child.parse(self.code)
            self.statements.append(child)
            self.code.next()

        # Merge all imports.
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
        self.comment.notes()
        self.markdown.extend(self.comment.markdown)
        for itr in self.statements:
            itr.notes()
            self.markdown.extend(itr.markdown)

        # Clear children notes for memory efficency.
        self.comment.markdown.clear()
        for itr in self.statements:
            itr.markdown.clear()

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
        - *args
        - **kargs

        Returns
        -------
        - flag
            If the text is satisfied.

        This is specially defined because some imports are constantly required.
        """
        # Match directly
        return self.statements[i].memory.text == text


class ConstBlockDocument(CodeDocument):
    r"""
    Document for a block of constant code.
    """
    def __init__(
        self: ConstBlockDocument, *args: object,
        level: int, hierarchy: int,
        superior: Union[CodeDocument, None], filedoc: FileDocument,
        constant: str, **kargs: object,
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
        - constant
            Constant code text.
        - **kargs

        Returns
        -------

        """
        # Super.
        CodeDocument.__init__(
            self, *args, level=level, hierarchy=hierarchy, superior=superior,
            filedoc=filedoc, **kargs,
        )

        # Save necessary attributes.
        self.CONSTANT = constant.split("\n")

    def allocate(
        self: ConstBlockDocument, *args: object, **kargs: object,
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
        # Allocate document memory for constant lines.
        self.memory: List[Line] = []

    def parse(
        self: ConstBlockDocument, code: Code, *args: object, **kargs: object,
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
        for i, itr in enumerate(self.CONSTANT):
            # Get current line.
            obj = self.code.get()

            # Directly match the constant text with current line.
            if (obj.text == itr):
                pass
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " expect\n\"\"\"\n{:s}\n\"\"\", but" \
                    " get\n\"\"\"\n{:s}\"\"\".",
                    self.FILEDOC.PATH, "line {:d}".format(obj.row),
                    itr, obj.text,
                )
                raise RuntimeError

            # Save verified line in document memory.
            self.memory.append(obj)
            self.code.next()

    def notes(
        self: ConstBlockDocument, *args: object, **kargs: object,
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
        # Block notes is just a list of code lines without indents.
        start = self.LEVEL * UNIT
        for itr in self.memory:
            self.markdown.append(itr.text[start:])


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
        CodeDocument.parse(self, code, *args, **kargs)

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
        - texts
            A list of parsed comment texts.
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
        start = self.LEVEL * UNIT
        for itr in self.memory:
            self.markdown.append(itr.text[start:])


class ImportDocument(CodeDocument):
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
        CodeDocument.parse(self, code, *args, **kargs)

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
        self.markdown.append(self.memory.text[start:])


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
        - texts
            A list of parsed introduction texts.
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
        self.markdown.append("## Section: {:s}".format(self.title))
        for itr in self.paragraphs:
            self.markdown.append("")
            self.markdown.append(" ".join(itr))

        # Return to TOC, file.
        self.markdown.append("")
        self.markdown.append(
            "[[TOC]](#table-of-content) [[File]](#{:s})".format(
                github_header("File: {:s}".format(
                    self.FILEDOC.PATH,
                )),
            ),
        )


class DescriptionDocument(CodeDocument):
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
        CodeDocument.parse(self, code, *args, **kargs)

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
        - texts
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
    def allocate(
        self: ClassDescDocument, *args: object, **kargs: object,
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
        # Super.
        DescriptionDocument.allocate(self, *args, **kargs)

    def decode(
        self: ClassDescDocument, texts: List[str], *args: object,
        **kargs: object,
    ) -> None:
        r"""
        Decode list of texts into document.

        Args
        ----
        - self
        - texts
            A list of decoding texts.
        - *args
        - **kargs

        Returns
        -------

        """
        # Translate parsed text into paragraphs.
        try:
            self.title = paragraphize(texts)
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
        - texts
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
            self.title = paragraphize(texts_1)
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
            self.attach = paragraphize(texts_2)
        except:
            # Extend paragraph error report.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " fail to translate paragraphs.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Save argument and return description for later review.
        self.texts_args = texts_args
        self.texts_returns = texts_returns

    def review(
        self: FuncDescDocument, argdoc: ArgumentDocument,
        returndoc: TypeHintDocument, *args: object, **kargs: object,
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
        self: FuncDescDocument, argdoc: ArgumentDocument, *args: object,
        **kargs: object,
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
        texts = self.texts_args

        # Argument description has constant head.
        if (texts[0] == "Args" and texts[1] == "----"):
            pass
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
        num = 0
        self.arg_names = []
        self.arg_hints = []
        self.arg_descs: List[List[List[str]]] = []
        while (ptr < len(texts)):
            # Get argument name.
            name = texts[ptr][2:]
            ptr += 1

            # Get definition.
            if (num == len(argdoc.items)):
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " defined arguments are less than described arguments.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
            else:
                pass
            given, hint = argdoc.items[num]
            num += 1

            # Argument name should match given definition.
            if (name == given):
                pass
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " defined argument \"{:s}\" does not match described" \
                    " argument name \"{:s}\".",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                    given, name,
                )
                raise RuntimeError
            self.arg_names.append(name)
            self.arg_hints.append(hint.text())

            # Some arguments have no attachment.
            if (name in ("self", "cls", "*args", "**kargs")):
                self.arg_descs.append([])
                continue
            else:
                pass

            # Get attachment.
            buf = []
            while (ptr < len(texts)):
                if (texts[ptr][0].isspace()):
                    pass
                else:
                    break
                buf.append(texts[ptr][UNIT:])
                ptr += 1
            try:
                attach = paragraphize(buf)
            except:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " fail to translate paragraphs.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
            self.arg_descs.append(attach)
        del self.texts_args

        # Check if there is argument without description.
        if (num == len(argdoc.items)):
            pass
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " some defined arguments (\"{:s}\", ...)have no descriptions.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
                argdoc.items[num][0],
            )
            raise RuntimeError

    def review_returns(
        self: FuncDescDocument, returndoc: TypeHintDocument,
        *args: object, **kargs: object,
    ) -> None:
        r"""
        Review argument and return.

        Args
        ----
        - self
        - returndoc
            Return document.
        - *args
        - **kargs

        Returns
        -------

        """
        # Get texts.
        texts = self.texts_returns

        # Argument description has constant head.
        if (texts[0] == "Returns" and texts[1] == "-------"):
            pass
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " return document has constant head.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError

        # Decode return document into a list a return type hints.
        if (returndoc.name == "None"):
            returnlist = []
        elif (returndoc.name == "MultiReturn"):
            returnlist = returndoc.children
        else:
            returnlist = [returndoc]

        # Traverse later contents.
        ptr = 0
        texts = texts[2:]
        num = 0
        self.return_names = []
        self.return_hints = []
        self.return_descs = []
        while (ptr < len(texts)):
            # Get argument name.
            name = texts[ptr][2:]
            ptr += 1

            # Get definition.
            if (num == len(returnlist)):
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " defined returns are less than described returns.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
            else:
                pass
            hint = returnlist[num]
            num += 1
            self.return_names.append(name)
            self.return_hints.append(hint.text())

            # Get attachment.
            buf = []
            while (ptr < len(texts)):
                if (texts[ptr][0].isspace()):
                    pass
                else:
                    break
                buf.append(texts[ptr][UNIT:])
                ptr += 1
            try:
                attach = paragraphize(buf)
            except:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " fail to translate paragraphs.",
                    self.FILEDOC.PATH, "line {:d}".format(self.row),
                )
                raise RuntimeError
            self.return_descs.append(attach)
        del self.texts_returns

        # Check if there is argument without description.
        if (num == len(returnlist)):
            pass
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " some defined returns have no descriptions.",
                self.FILEDOC.PATH, "line {:d}".format(self.row),
            )
            raise RuntimeError


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main >>
# Main branch starts from here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# Main branch.
if (__name__ == "__main__"):
    # Generate all notes.
    doc = DirectoryDocument(os.path.abspath("."), rootdoc=None)
    doc.parse()
else:
    pass