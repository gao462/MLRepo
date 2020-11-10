# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import List

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
from doc.base import FileSysDocument, GLOBAL
from doc.globe import ModuleDocument, GlobalDocument
from doc.series import ClassDocument


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


class DirectoryDocument(FileSysDocument):
    r"""
    Document for a directory.
    """
    def parse(
        self: DirectoryDocument, path: str, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - path
            Path of documentizing file.
        - *args
        - **kargs

        Returns
        -------

        """
        # Super.
        FileSysDocument.parse(self, path, *args, **kargs)

        # Traverse the tree.
        self.subdirs = []
        self.files = []
        for itr in os.listdir(path):
            itr = os.path.join(path, itr)
            if (os.path.isdir(itr)):
                base = os.path.basename(itr)
                if (base == "__pycache__"):
                    # Some directory name should be ignored.
                    pass
                elif (base[0] == "."):
                    # Hidden directory should be ignored.
                    pass
                else:
                    dirdoc = DirectoryDocument(rootdoc=self.ROOTDOC)
                    dirdoc.parse(itr)
                    self.subdirs.append(dirdoc)
            elif (os.path.isfile(itr)):
                base, ext = os.path.splitext(itr)
                base = os.path.basename(base)
                if (ext == ".py"):
                    if (base == "__init__"):
                        warning("Skip for now.")
                    else:
                        filedoc = FileDocument(rootdoc=self.ROOTDOC)
                        filedoc.parse(itr)
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
        if (os.path.basename(self.path) == self.ROOT):
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
                    self.GITHUB, filedoc.path, row,
                )
                self.classes["{:s}.{:s}".format(filedoc.me, key)] = location

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
        self.notes_console = console
        self.notes_markdown = markdown

        # Save markdown note as README.
        file = open(os.path.join(self.path, "README.md"), "w")
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


class FileDocument(FileSysDocument):
    r"""
    Document for a file.
    """
    def parse(
        self: FileDocument, path: str, *args: object, **kargs: object,
    ) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - path
            Path of documentizing file.
        - *args
        - **kargs

        Returns
        -------

        """
        # Super.
        FileSysDocument.parse(self, path, *args, **kargs)

        # File document has a module-import document and a global document.
        self.modules = ModuleDocument(
            path=self.path, level=0, hierarchy=GLOBAL,
            superior=None, filedoc=self,
        )
        self.sections = GlobalDocument(
            path=self.path, level=0, hierarchy=GLOBAL,
            superior=None, filedoc=self,
        )

        # Load tokenized code and parse it.
        self.code = Code()
        self.code.load_file(self.path)
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
        console = ["## {:s}".format(self.path)]
        markdown = ["## {:s}".format(self.path)]

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