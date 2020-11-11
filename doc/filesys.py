# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List, Tuple, Union, Dict

# Import dependencies.
import sys
import os
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
from doc.code import Code
import doc.base
import doc.globe
import doc.series


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


class DirectoryDocument(doc.base.FileSysDocument):
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
        doc.base.FileSysDocument.__init__(self, path, *args, **kargs)

        # Save necessary attributes.
        self.ROOTDOC = self if rootdoc is None else rootdoc

        # File system should trace definitions.
        self.classes: Dict[str, str] = {}

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
                        filedoc = FileDocument(itr, rootdoc=self.ROOTDOC)
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
        if (os.path.basename(self.PATH) == self.ROOT):
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

        # Register definitions from files.
        for filedoc in self.files:
            for key, row in filedoc.classes.items():
                location = "{:s}/blob/master/{:s}{:s}".format(
                    self.GITHUB, filedoc.PATH, row,
                )
                self.classes["{:s}.{:s}".format(filedoc.ME, key)] = location

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
        console = []
        markdown = []
        for filedoc in self.files:
            filedoc.notes()
            console.extend(["", "---", ""])
            markdown.extend(["", "---", ""])
            console.extend(filedoc.notes_console)
            markdown.extend(filedoc.notes_markdown)

        # Generate table of content.
        self.notes_console = toc(console) + console
        self.notes_markdown = toc(markdown) + markdown

        # Save markdown note as README.
        file = open(os.path.join(self.PATH, "README.md"), "w")
        file.write("\n".join(self.notes_markdown))
        file.close()

        # Clear children notes for memory efficency.
        for filedoc in self.files:
            filedoc.notes_console.clear()
            filedoc.notes_markdown.clear()

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
        print("Done")


class FileDocument(doc.base.FileSysDocument):
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
        doc.base.FileSysDocument.__init__(self, path, *args, **kargs)

        # Save necessary attributes.
        self.ROOTDOC = self if rootdoc is None else rootdoc

        # Get module path from file path.
        _, self.PATH = self.PATH.split(os.path.join(" ", self.ROOT, " ")[1:-1])
        self.ME = self.PATH.replace(os.path.join(" ", " ")[1:-1], ".")
        self.ME, _ = os.path.splitext(self.ME)

        # Set code to parse on.
        self.code = Code()

        # File document has a module-import document and a global document.
        self.modules = doc.globe.ModuleDocument(
            path=self.PATH, level=0, hierarchy=doc.base.GLOBAL,
            superior=None, filedoc=self,
        )
        self.sections = doc.globe.GlobalDocument(
            path=self.PATH, level=0, hierarchy=doc.base.GLOBAL,
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
                if (isinstance(component, doc.series.ClassDocument)):
                    self.classes[component.name] = "#L{:d}".format(
                        component.row,
                    )
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
        # Create title by file path.
        console = ["## {:s}".format(self.PATH)]
        markdown = ["## {:s}".format(self.PATH)]

        # Extend notes by imported modules.
        self.modules.notes()
        console.append("")
        markdown.append("")
        console.extend(self.modules.notes_console)
        markdown.extend(self.modules.notes_markdown)

        # Extend notes by global sections.
        self.sections.notes()
        console.append("")
        markdown.append("")
        console.extend(self.sections.notes_console)
        markdown.extend(self.sections.notes_markdown)
        self.notes_console = console
        self.notes_markdown = markdown

        # Clear children notes for memory efficency.
        self.modules.notes_console.clear()
        self.modules.notes_markdown.clear()


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
        headers.append((level, text, github_header(refer)))

    # Generate TOC.
    toc = ["* Table of Content"]
    for level, text, refer in headers:
        indent = "  " * (level - 1)
        link = "{:s}* [{:s}](#{:s})".format(indent, text, refer)
        toc.append(link)
    return toc


def github_header(text: str, *args, **kargs) -> str:
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

    # Github reference should be lower case concatenated by "-".
    refer = re.sub(r"[^\w]+", "-", refer.lower())
    return refer
