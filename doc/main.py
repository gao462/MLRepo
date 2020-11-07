# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import Tuple, Union, List

# Import dependencies.
import sys
import os
import tokenize
import token
import re
import logging

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error
from pytorch.logging import update_universal_logger, WARNING

# Import dependencies.


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Code Objects >>
# Tokenized code for any arbitrary file is defined based on Python token
# library.
# Each tokenized code word is automatically attached with its indent level for
# later styled document check.
#
# A scanner over tokenized code is also defined for the ease of check.
# Essential and shared utility functions related to code words are integrated.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Word(object):
    r"""
    Token word.
    """
    def set(
        self,
        val: int, text: str,
        row: int, level: Union[int, None], column: int,
    ) -> None:
        r"""
        Set word attributes.

        Args
        ----
        - self
        - val
            Token integer.
        - text
            Token text content.
        - row
            Token row index.
        - level
            Token indent level.
        - column
            Token column index.

        Returns
        -------

        """
        # Save necessary attributes.
        self.token = val
        self.token_string = token.tok_name[self.token]
        self.text = text
        self.row = row
        self.level = level
        self.column = column

    @property
    def position(self) -> str:
        r"""
        Position string.

        Args
        ----
        - self

        Returns
        -------
        - msg
            Position string.

        """
        # Get indent level, line (row) and column.
        return "(line {:d}, column: {:d})".format(self.row, self.column)


class Code(object):
    r"""
    Tokenized code with indent of a file.
    """
    def __init__(self) -> None:
        r"""
        Initialize.

        Args
        ----
        - self

        Returns
        -------

        """
        # Define constants.
        self.UNIT = 4
        self.MAX = 79

        # Define regular expressions.
        self.RX_NUM = r"([1-9][0-9]*)"
        self.RX_CAP = r"([A-Z][A-Za-z]*)"
        self.RX_CMN = r"([A-Za-z]+)"
        self.RX_FIRST = r"({:s}(-{:s})*)".format(
            "({:s}|{:s})".format(self.RX_CAP, self.RX_NUM),
            "({:s}|{:s})".format(self.RX_CMN, self.RX_NUM),
        )
        self.RX_LATER = r"({:s}(-{:s})*)".format(
            "({:s}|{:s})".format(self.RX_CMN, self.RX_NUM),
            "({:s}|{:s})".format(self.RX_CMN, self.RX_NUM),
        )
        self.RX_SENTENCE_BREAK = r" |, | \(|\)"
        self.RX_SENTENCE = r"{:s}(({:s}){:s})*.".format(
            self.RX_FIRST, self.RX_SENTENCE_BREAK, self.RX_LATER,
        )

    def __len__(self) -> int:
        r"""
        Length.

        Args
        ----
        - self

        Returns
        -------
        - length
            Length of remaining memory.

        """
        # Get directly.
        return len(self.memory) - self.ptr

    def load_file(self, path: str) -> None:
        r"""
        Load code tokens from given file.

        Args
        ----
        - self
        - path
            File path.

        Returns
        -------

        """
        # Save loaded path.
        self.path = path

        # Load file text lines.
        self.load_texts()
        self.rule_texts()

        # Load file tokens.
        self.load_tokens()

        # Review text lines and file tokens as lines of tokens.
        self.review()

    def load_texts(self) -> None:
        r"""
        Load text lines from given file.

        Args
        ----
        - self

        Returns
        -------

        """
        # Read text lines along with indent level.
        self.texts = []
        file = open(self.path, "r")
        for line in file:
            # Get indent level for current line.
            level = (len(line) - len(line.lstrip())) // self.UNIT
            line = line.strip()

            # Blank line is special.
            if (len(line) == 0):
                self.texts.append((None, line))
            else:
                self.texts.append((level, line))
        file.close()

    def load_tokens(self) -> None:
        r"""
        Load tokens from given file.

        Args
        ----
        - self

        Returns
        -------

        """
        # Load tokens except indent/dedent.
        self.tokens = []
        file = open(self.path, "r")
        buf = tokenize.generate_tokens(file.readline)
        for itr in buf:
            if (itr[0] in (token.INDENT, token.DEDENT)):
                pass
            else:
                self.tokens.append(itr)
        file.close()

    def rule_texts(self) -> None:
        r"""
        Check rules over text lines.

        Args
        ----
        - self

        Returns
        -------

        """
        # Check each text lines.
        for i, line in enumerate(self.texts):
            self.line_rule_length(i + 1, line)
            self.line_rule_char(i + 1, line)
            self.line_rule_break(i + 1, line)

    def line_rule_length(self, index: int, line: str) -> None:
        r"""
        Check length rule over a text line.

        Args
        ----
        - self
        - index
            Line index.
        - line
            Line content.

        Returns
        -------

        """
        # Text length is limited.
        if (len(line) > self.MAX):
            error(
                "{:s}, \"{:s}\", {:s}, too long (>{:d}).",
                "{:s}.line_rule_length".format(self.__class__.__name__),
                self.path,
                "\033[31;1;47;1mline {:d}\033[0m".format(index),
                self.MAX,
            )
            raise RuntimeError
        else:
            pass

    def line_rule_char(self, index: int, line: str) -> None:
        r"""
        Check character rule over a text line.

        Args
        ----
        - self
        - index
            Line index.
        - line
            Line content.

        Returns
        -------

        """
        # Some charaters are rejected.
        if (chr(39) in line):
            error(
                "{:s}, \"{:s}\", {:s}, invalid char (\"{:s}\").",
                "{:s}.line_rule_char".format(self.__class__.__name__),
                self.path,
                "\033[31;1;47;1m{:d}\033[0m".format(index),
                chr(39),
            )
            raise RuntimeError
        else:
            pass

    def line_rule_break(self, index: int, line: str) -> None:
        r"""
        Check line break rule over a text line.

        Args
        ----
        - self
        - index
            Line index.
        - line
            Line content.

        Returns
        -------

        """
        # Line break is rejected except for strings.
        if (line[-2:] == " \\" and line[-3] != "\""):
            error(
                "{:s}, \"{:s}\", {:s}, line break is disabled.",
                "{:s}.line_rule_break".format(self.__class__.__name__),
                self.path,
                "\033[31;1;47;1m{:s}\033[0m".format(index),
            )
            raise RuntimeError
        else:
            pass

    def review(self) -> None:
        r"""
        Review text lines and tokens as lines of tokens.

        Args
        ----
        - self

        Returns
        -------

        """
        # Define real buffer.
        self.memory = []

        # Traverse lines and get their tokens.
        num_texts = len(self.texts)
        while (self.tokens[0][0] != token.ENDMARKER):
            # Get the starting token.
            val, content, (start, index), (end, _), _ = self.tokens.pop(0)
            if (num_texts - len(self.texts) + 1 == start):
                pass
            else:
                error(
                    "{:s}, \"{:s}\", impossible branch.",
                    "{:s}.review".format(self.__class__.__name__),
                    self.path,
                )
                raise NotImplementedError

            # String can have multiple lines with different indent levels.
            level, _ = self.texts.pop(0)
            if (val == token.STRING):
                for i in range(start + 1, end + 1):
                    buf, _ = self.texts.pop(0)
            else:
                pass

            # Construct the initial word.
            word = Word()
            word.set(val, content, start, level, index)
            self.memory.append(word)

            # Get tokens of the same lines.
            targets = list(range(start, end + 1))
            while (self.tokens[0][2][0] in targets):
                val, content, (start, index), (end, _), _ = self.tokens.pop(0)
                word = Word()
                word.set(val, content, start, None, index)
                self.memory.append(word)

        # A file has an implicit EOF line.
        if (len(self.texts) == 0 and len(self.tokens) == 1):
            # Append the last EOF word.
            val, content, (start, index), (end, _), _ = self.tokens.pop(0)
            word = Word()
            word.set(val, content, start, None, index)
            self.memory.append(word)

            # Clear raw text and token buffers.
            del self.texts
            del self.tokens
        else:
            error(
                "{:s}, \"{:s}\", impossible branch.",
                "{:s}.line_rule_break".format(self.__class__.__name__),
                self.path,
            )
            raise NotImplementedError

    def reset(self) -> None:
        r"""
        Reset scanning status.

        Args
        ----
        - self

        Returns
        -------

        """
        # Reset word pointer.
        self.ptr = 0

    def next(self) -> None:
        r"""
        Move to next scanning status.

        Args
        ----
        - self

        Returns
        -------

        """
        # Move word pointer.
        self.ptr += 1

    @property
    def top(self) -> Word:
        r"""
        Get the first focusing word.

        Args
        ----
        - self

        Returns
        -------
        - word
            Top word.

        """
        # Get directly.
        return self.memory[self.ptr]

    def preview(self, shift: int) -> Word:
        r"""
        Get the preview of word shifted from first focusing word.

        Args
        ----
        - self
        - shift
            Shifting offset.

        Returns
        -------
        - word
            Shifted word.

        """
        # Get directly.
        return self.memory[self.ptr + shift]

    def fit(self, level: int, target: Union[int, str, None]) -> bool:
        r"""
        Check if scanning token fits the target.

        Args
        ----
        - self
        - level
            Targe token indent level.
        - target
            Target token ID or text.
            If None, it means anything.

        Returns
        -------
        - flag
            If True, target is satisfied by current token.

        """
        # Check different cases.
        obj = self.top
        flag = (obj.level is None or obj.level == level)
        if (isinstance(target, int)):
            return flag and (target is None or obj.token == target)
        else:
            return flag and (target is None or obj.text == target)

    def eof(self) -> bool:
        r"""
        Get EOF signal.

        Args
        ----
        - self

        Returns
        -------
        - flag
            EOF signal.

        """
        # Check EOF token.
        return self.fit(0, token.ENDMARKER)

    def paragraphs(self, contents: List[str]) -> List[List[str]]:
        r"""
        Break given content into list of paragraphs.

        Args
        ----
        - self
        - contents
            Given contents.

        Returns
        -------
        - texts
            Text of contents as list of paragraphs.
            Each paragraph is a list of regular sentence.

        """
        # Concatenate contents and break into sentences by "." at line end.
        buf = []
        sentences = []
        texts = []
        for line in contents + [""]:
            # Current paragraph ends by a blank line.
            if (len(line) == 0):
                if (len(buf) > 0 or len(sentences) == 0):
                    error(
                        "{:s}, \"{:s}\", {:s}, comments require" \
                        " paragraphs being separated by a blank line," \
                        " sentences being separated by \"\\n\", and each" \
                        " sentence being of regex \"{:s}\".",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.path,
                        "\033[31;1;47;1mahead {:s}\033[0m".format(
                            self.top.position,
                        ),
                        self.RX_SENTENCE,
                    )
                    raise RuntimeError
                else:
                    texts.append(sentences)
                    sentences = []
                    continue
            else:
                pass

            # Add line to current sentence.
            buf.append(line)

            # A sentence ends by a line ending with ".".
            if (line[-1] == "."):
                itr = " ".join(buf)
                buf.clear()
                if (re.match(self.RX_SENTENCE, itr) is None):
                    error(
                        "{:s}, \"{:s}\", {:s}, comments require paragraphs" \
                        " being separated by a blank line, sentences being" \
                        " separated by \"\\n\", and each sentence being of" \
                        " regex \"{:s}\", but get\n\"\"\"\n{:s}\n\"\"\".",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.path,
                        "\033[31;1;47;1mahead {:s}\033[0m".format(
                            self.top.position,
                        ),
                        self.RX_SENTENCE, itr,
                    )
                    raise RuntimeError
                else:
                    sentences.append(itr)
            else:
                pass
        return texts


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Document Objects >>
# Documentize tokenized code files, and check style rules in the meanwhile.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Document(object):
    r"""
    Document prototype.
    """
    # Define constants.
    GITHUB = "https://github.com/gao462/MLRepo"

    def __init__(self) -> None:
        r"""
        Initialize.

        Args
        ----
        - self

        Returns
        -------

        """
        # Prototype can not be instantiated.
        error("{:s}.__init__, is not implemented.", self.__class__.__name__)
        raise NotImplementedError

    def parse(self, *args, **kargs) -> None:
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
        # Prototype can not be instantiated.
        error("{:s}.parse, is not implemented.", self.__class__.__name__)
        raise NotImplementedError

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Prototype can not be instantiated.
        error("{:s}.markdown, is not implemented.", self.__class__.__name__)
        raise NotImplementedError


class DirectoryDocument(Document):
    r"""
    Document for a directory.
    """
    def __init__(self) -> None:
        r"""
        Initialize.

        Args
        ----
        - self

        Returns
        -------

        """
        # Nothing is required.
        pass

    def parse(self, root: str) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - root
            Root of the project.

        Returns
        -------

        """
        # Traverse the tree.
        self.subdirs = []
        self.files = []
        self.readme = []
        for itr in os.listdir(root):
            path = os.path.join(root, itr)
            if (os.path.isdir(path)):
                if (itr in ("__pycache__", ".git")):
                    pass
                else:
                    child = DirectoryDocument()
                    child.parse(path)
                    self.subdirs.append(child)
            elif (os.path.isfile(path)):
                if (os.path.splitext(path)[1] == ".py"):
                    child = FileDocument()
                    child.parse(path)
                    self.files.append(child)
                    self.readme.append("")
                    self.readme.append("---")
                    self.readme.append("")
                    self.readme.extend(child.markdown())
                elif (os.path.splitext(path)[1] in (".md", ".sh")):
                    pass
                elif (itr == ".gitignore"):
                    pass
                else:
                    error(
                        "{:s}, \"{:s}\", impossible branch.",
                        "{:s}.parse".format(self.__class__.__name__),
                        root,
                    )
                    raise NotImplementedError
            else:
                error(
                    "{:s}, \"{:s}\", impossible branch.",
                    "{:s}.parse".format(self.__class__.__name__),
                    root,
                )
                raise NotImplementedError
        if (len(self.files) > 0):
            file = open(os.path.join(root, "README.md"), "w")
            file.write("\n".join(self.readme))
            file.close()
        else:
            pass


class FileDocument(Document):
    r"""
    Document for a file.
    """
    def __init__(self) -> None:
        r"""
        Initialize.

        Args
        ----
        - self

        Returns
        -------

        """
        # Nothing is required.
        pass

    def parse(self, path: str) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - path
            Path of documentizing file.

        Returns
        -------

        """
        # Load tokenized code.
        _, self.path = path.split(os.path.join("", "MLRepo", ""))
        self.code = Code()
        self.code.load_file(self.path)
        self.code.reset()

        # File document is a module import document and a global document.
        self.modules = ModuleDocument(self.path, 0, GLOBAL)
        self.sections = GlobalDocument(self.path, 0, GLOBAL)
        self.modules.parse(self.code)
        self.sections.parse(self.code)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Get path as title.
        notes = ["## {:s}".format(self.path)]
        notes.append("")
        notes.extend(self.modules.markdown())
        notes.append("")
        notes.extend(self.sections.markdown())
        return notes


# Hierarchy constants.
GLOBAL = 0
CLASS = 1
FUNCTION = 2
BLOCK = 3
SHORT = 4


class CodeDocument(Document):
    r"""
    Document prototype for code.
    """
    def __init__(self, path: str, level: int, hierarchy: int) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - path
            Path of its file document.
        - level
            Indent level.
        - hierarchy
            Hierarchy order.

        Returns
        -------

        """
        # Save necessary attributes.
        self.PATH = path
        self.LEVEL = level
        self.HIERARCHY = hierarchy

    def expect(self, *args) -> None:
        r"""
        Expect next several code words to be the arguments.

        Args
        ----
        - self
        - *args

        Returns
        -------

        """
        # Check if the target requirement is satisfied one-by-one.
        for itr in args:
            obj = self.code.top
            if (self.code.fit(self.LEVEL, itr)):
                self.code.next()
            elif (isinstance(itr, int)):
                if (obj.level is None):
                    buf = "inline"
                else:
                    buf = "indent {:d}".format(obj.level)
                error(
                    "{:s}, \"{:s}\", {:s}, expect indent {:d} token {:s}," \
                    " but get {:s} token {:s}.",
                    "{:s}.expect".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        obj.position,
                    ),
                    self.LEVEL, token.tok_name[itr],
                    buf, obj.token_string,
                )
                raise RuntimeError
            else:
                if (obj.level is None):
                    buf = "inline"
                else:
                    buf = "indent {:d}".format(obj.level)
                error(
                    "{:s}, \"{:s}\", {:s}, expect indent {:d} text \"{:s}\"," \
                    " but get {:s} text \"{:s}\".",
                    "{:s}.expect".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        obj.position,
                    ),
                    self.LEVEL, repr(itr)[1:-1],
                    buf, repr(obj.text)[1:-1],
                )
                raise RuntimeError


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Global Code Document Objects >>
# Code document on global level.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ModuleDocument(CodeDocument):
    r"""
    Document for module imports.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = code.top.position
        self.modules = {}

        # Typing import has constant head.
        self.expect("# Import typing.", token.NL)
        self.expect("from", "typing", "import", "Any", token.NEWLINE)
        self.append("typing", "Any")
        self.expect(
            "from", "typing", "import", "Tuple", "as", "MultiReturn",
            token.NEWLINE,
        )
        self.append("typing", "MultiReturn (Tuple)")
        self.append_until()

        # Dependency (python) import has constant head.
        self.expect(token.NL)
        self.expect("# Import dependencies.", token.NL)
        self.append_until()

        # Adding development library is a constant operation included by two
        # levels.
        self.expect(token.NL)
        self.expect("# Add development library to path.", token.NL)
        self.expect(
            "if", "(", "os", ".", "path", ".", "basename", "(", "os", ".",
            "getcwd", "(", ")", ")", "==", "\"MLRepo\"", ")", ":",
            token.NEWLINE,
        )
        ConstDocument(
            self.PATH, 1, GLOBAL, constants=[
                "sys", ".", "path", ".", "append", "(", "os", ".", "path", ".",
                "join", "(", "\".\"", ")", ")", token.NEWLINE,
            ],
        ).parse(self.code)
        self.expect("else", ":", token.NEWLINE)
        ConstDocument(
            self.PATH, 1, GLOBAL, constants=[
                "print", "(", "\"Code must strictly work in \\\"MLRepo\\\".\"",
                ")", token.NEWLINE,
            ],
        ).parse(self.code)
        ConstDocument(
            self.PATH, 1, GLOBAL, constants=[
                "exit", "(", ")", token.NEWLINE,
            ],
        ).parse(self.code)

        # Logging import has constant head.
        self.expect(token.NL)
        self.expect("# Import logging.", token.NL)
        if (self.PATH == os.path.join("pytorch", "logging.py")):
            pass
        else:
            self.expect(
                "from", "pytorch", ".", "logging", "import", "debug", ",",
                "info1", ",", "info2", ",", "focus", ",", "warning", ",",
                "error", token.NEWLINE
            )
            self.append("pytorch.logging", "debug")
            self.append("pytorch.logging", "info1")
            self.append("pytorch.logging", "info2")
            self.append("pytorch.logging", "focus")
            self.append("pytorch.logging", "warning")
            self.append("pytorch.logging", "error")
        self.append_until()

        # Dependency (development) import has constant head.
        self.expect(token.NL)
        self.expect("# Import dependencies.", token.NL)
        self.append_until()

        # Log parsed modules as main info.
        for module, identifiers in self.modules.items():
            info2(
                "{:s} Module \033[35;4m{:s}\033[0m[{:s}].",
                self.position, module, ", ".join(identifiers),
            )

    def append(self, module: str, identifier: Union[str, None]) -> None:
        r"""
        Append an import opertation.

        Args
        ----
        - self
        - module
            Module name.
        - identifier
            Identifier name.

        Returns
        -------

        """
        # Differentiate import and from-import.
        if (identifier is None):
            if (module in self.modules):
                error(
                    "{:s}, \"{:s}\", {:s}, dual import \"{:s}\".",
                    "{:s}.append".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1mahead {:s}\033[0m".format(
                        self.position,
                    ),
                    module,
                )
                raise RuntimeError
            else:
                self.modules[module] = {}
        else:
            if (module in self.modules):
                pass
            else:
                self.modules[module] = []
            self.modules[module].append(identifier)

    def append_until(self) -> None:
        r"""
        Append import operations until a blank line.

        Args
        ----
        - self

        Returns
        -------

        """
        # Get import line document until a blank line.
        while (
            not self.code.eof() and not self.code.fit(self.LEVEL, token.NL)
        ):
            imported = ImportDocument(self.PATH, 0, GLOBAL)
            imported.parse(self.code)
            for itr in imported.identifiers:
                self.append(imported.name, itr)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Get imported module names.
        imported = []
        for name, _ in self.modules.items():
            imported.append("`{:s}`".format(name))
        notes = ["- Dependent on: {:s}.".format(", ".join(imported))]
        return notes


class GlobalDocument(CodeDocument):
    r"""
    Document for global level codes.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.sections = []

        # Parse sections until EOF.
        while (not self.code.eof()):
            intro = IntroductionDocument(self.PATH, 0, GLOBAL)
            series = SeriesDocument(self.PATH, 0, GLOBAL)
            intro.parse(self.code)
            series.parse(self.code)
            self.sections.append((intro, series))

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Get children notes.
        notes = []
        notes.extend(self.sections[0][0].markdown())
        notes.append("")
        notes.extend(self.sections[0][1].markdown())
        for intro, series in self.sections[1:]:
            notes.append("")
            notes.extend(intro.markdown())
            notes.append("")
            notes.extend(series.markdown())
        return notes


class IntroductionDocument(CodeDocument):
    r"""
    Document for introduction codes.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = code.top.position
        self.title = None
        self.paragraphs = None

        # Construct introduction lines.
        intro_line1 = "# " + "=" * (self.code.MAX - 2)
        intro_line2 = "# " + "*" * (self.code.MAX - 2)
        intro_line3 = "# " + "-" * (self.code.MAX - 2)

        # Introduction head is constant.
        self.expect(token.NL, token.NL)
        self.expect(intro_line1, token.NL)
        self.expect(intro_line2, token.NL)
        self.expect(intro_line3, token.NL)

        # Introduction has a short title of strict format.
        title = self.code.top.text
        self.expect(token.COMMENT)
        self.expect(token.NL)
        items = title[2:].split(" ")
        lsharp, title, rsharp = items[0], items[1:-1], items[-1]
        if (lsharp == "<<" and rsharp == ">>"):
            # All title words show as the first word of a sentence.
            for itr in title:
                if (re.match(self.code.RX_FIRST, itr) is None):
                    error(
                        "{:s}, \"{:s}\", {:s}, introduction word requires" \
                        " regex \"{:s}\".",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.PATH,
                        "\033[31;1;47;1m{:s}\033[0m".format(
                            self.position,
                        ),
                        self.code.REGEX_WORD,
                    )
                    raise RuntimeError
                else:
                    pass
        else:
            error(
                "{:s}, \"{:s}\", {:s}, introduction title requires form" \
                " << title >>.",
                "{:s}.parse".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError
        self.title = " ".join(title)

        # Log parsed title ahead of introduction content.
        debug(
            "{:s}, {:s} Introduction \033[30;1;4m<< {:s} >>\033[0m.",
            "{:s}.parse".format(self.__class__.__name__),
            self.position, self.title,
        )

        # Directly merge later comment lines as introduction.
        comments = []
        while (
            not self.code.eof() and not self.code.fit(self.LEVEL, intro_line3)
        ):
            itr = self.code.top.text
            self.expect(token.COMMENT)
            self.expect(token.NL)
            comments.append(itr[2:])
        self.paragraphs = self.code.paragraphs(comments)

        # Log parsed paragraphs.
        info2(
            "{:s} Introduction \033[30;1;4m<< {:s} >>\033[0m.",
            self.position, self.title,
        )
        info1(
            "\"\"\"\n\033[30;1;4m{:s}\033[0m\n\"\"\".",
            "\n".join([" ".join(itr) for itr in self.paragraphs]),
        )

        # Introduction tail is constant.
        self.expect(intro_line3, token.NL)
        self.expect(intro_line2, token.NL)
        self.expect(intro_line1, token.NL)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Get introduction title as title.
        notes = ["### {:s}".format(self.title)]

        # Add paragraphs to the notes.
        for itr in self.paragraphs:
            notes.append("")
            notes.append(" ".join(itr))
        return notes


class SeriesDocument(CodeDocument):
    r"""
    Document for a series of codes (any hierarchy).
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.children = []

        # Loop until the end of this series.
        first = True
        while (True):
            # Different level on next non-trivial word means the end. EOF is
            # implicitly included.
            ptr = 0
            obj = self.code.preview(ptr)
            while (obj.token != token.ENDMARKER and obj.level is None):
                ptr += 1
                obj = self.code.preview(ptr)
            if (obj.level != self.LEVEL):
                break
            else:
                pass

            # An introduction line means another end.
            intro_line = "# " + "=" * (self.code.MAX - 2)
            flag = (self.HIERARCHY == GLOBAL and len(self.code) > 2)
            flag = (flag and self.code.preview(2).text == intro_line)
            if (flag):
                break
            else:
                pass

            # Get blank lines as the separator.
            if (self.HIERARCHY == GLOBAL):
                self.expect(token.NL, token.NL)
            elif (first):
                pass
            else:
                self.expect(token.NL)

            # Append child document of different types.
            flag1 = self.code.fit(self.LEVEL, "class")
            flag2 = self.code.fit(self.LEVEL, "def")
            flag3 = self.code.fit(self.LEVEL, "@")
            flag4 = self.code.fit(self.LEVEL, token.COMMENT)
            if (flag1):
                if (self.HIERARCHY == GLOBAL):
                    deeper = CLASS
                else:
                    deeper = BLOCK
                child = ClassDocument(self.PATH, self.LEVEL, deeper)
            elif (flag2 or flag3):
                if (self.HIERARCHY in (GLOBAL, CLASS)):
                    deeper = FUNCTION
                else:
                    deeper = BLOCK
                child = FunctionDocument(self.PATH, self.LEVEL, deeper)
            elif (flag4):
                child = BlockDocument(self.PATH, self.LEVEL, BLOCK)
            else:
                # Short block only works for series of only one item.
                if (len(self.children) > 0 or self.HIERARCHY not in (
                    BLOCK, SHORT,
                )):
                    now = self.code.top.position
                    error(
                        "{:s}, \"{:s}\", {:s}, comment is required and" \
                        " no-comment block must occupy the whole series.",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.PATH,
                        "\033[31;1;47;1m{:s}\033[0m".format(now),
                    )
                    raise RuntimeError
                else:
                    child = BlockDocument(self.PATH, self.LEVEL, SHORT)
                    child.parse(self.code)
                    self.children.append(child)
                    break
            child.parse(self.code)
            self.children.append(child)

            # First flag turns off after one loop.
            first = False

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Merge children notes.
        notes = []
        for i, child in enumerate(self.children):
            # The first item does not need separators.
            if (i == 0):
                pass
            else:
                notes.append("")

            # Just extend notes by children notes, except for block items in
            # global or class level.
            flag1 = isinstance(child, BlockDocument)
            flag2 = (self.HIERARCHY in (GLOBAL, CLASS))
            if (flag1 and flag2):
                notes.append("- Block")
                for itr in child.paragraphs:
                    notes.append("")
                    notes.append("  {:s}".format(" ".join(itr)))
            else:
                notes.extend(child.markdown())
        return notes


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Class Code Document Objects >>
# Code document for class definition.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ClassDocument(CodeDocument):
    r"""
    Document for a class definition.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.name = None
        self.super = None
        self.doc = None
        self.series = None

        # Get class name.
        self.name = self.code.preview(1).text
        self.expect("class")
        self.expect(token.NAME)

        # Class name has strict form.
        if (re.match(r"([A-Z][a-z0-9]*)+", self.name) is None):
            error(
                "{:s}, \"{:s}\", {:s}, class name should be" \
                " first-char-uppercase, and each word of it should be" \
                " tightly concatenated.",
                "{:s}.parse".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError
        else:
            pass

        # Get super name.
        buf = [self.code.preview(1).text]
        self.expect("(", token.NAME)
        while (not self.code.eof() and not self.code.fit(self.LEVEL, ")")):
            buf.append(self.code.preview(1).text)
            self.expect(".", token.NAME)
        self.expect(")", ":", token.NEWLINE)
        self.super = ".".join(buf)

        # Log parsed class name ahead of description.
        debug(
            "{:s}, {:s} Class \033[32;1;4m{:s}\033[0m({:s}).",
            "{:s}.parse".format(self.__class__.__name__),
            self.position, self.name, self.super,
        )

        # Get class document string.
        self.doc = ClassDocDocument(self.PATH, self.LEVEL + 1, self.HIERARCHY)
        self.doc.parse(self.code)

        # Log parsed class description.
        info2(
            "{:s} Class \033[32;1;4m{:s}\033[0m({:s}).",
            self.position, self.name, self.super,
        )
        info1(
            "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
            "\n".join([" ".join(itr) for itr in self.doc.paragraphs]),
        )

        # Get code series of the class.
        self.series = SeriesDocument(self.PATH, self.LEVEL + 1, self.HIERARCHY)
        self.series.parse(self.code)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Generate super link to code position.
        position = "{:s}/blob/master/{:s}#L{:s}".format(
            self.GITHUB, self.PATH,
            self.position[1:-1].split(", ")[0].split(" ")[1],
        )

        # Use class and super names as title.
        notes = [
            "- Class [**{:s}**]({:s})(*{:s}*)".format(
                self.name, position, self.super,
            ),
        ]

        # Add the description paragraphs to notes with indent.
        notes.append("")
        for itr in self.doc.paragraphs:
            notes.append("  {:s}".format(" ".join(itr)))

        # Add children notes with indent.
        notes.append("")
        for itr in self.series.markdown():
            if (len(itr) == 0):
                notes.append(itr)
            else:
                notes.append("  {:s}".format(itr))
        return notes


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Function Code Document Objects >>
# Code document for function definition.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class FunctionDocument(CodeDocument):
    r"""
    Document for a function definition.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.decorates = []
        self.name = None
        self.args = None
        self.returns = None
        self.doc = None
        self.series = None

        # Get decorators.
        while (not self.code.eof() and self.code.fit(self.LEVEL, "@")):
            itr = DecorateDocument(self.PATH, self.LEVEL, self.HIERARCHY)
            itr.parse(self.code)
            self.decorates.append(itr)

        # Get function name.
        self.name = self.code.preview(1).text
        self.expect("def")
        self.expect(token.NAME)

        # Class name has strict form.
        regex_pub = r"[a-z][a-z0-9]*(_[a-z][a-z0-9]*)*"
        regex_prv = r"__{:s}__".format(regex_pub)
        regex = r"({:s}|{:s})".format(regex_pub, regex_prv)
        if (re.match(regex, self.name) is None):
            error(
                "{:s}, \"{:s}\", {:s}, function name should be lowercase," \
                " each word of which should be concatenated by \"_\".",
                "{:s}.parse".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError
        else:
            pass

        # Log parsed function name ahead of description.
        debug(
            "{:s}, {:s} Function \033[34;1;4m{:s}\033[0m.",
            "{:s}.parse".format(self.__class__.__name__),
            self.position, self.name,
        )

        # Left paranthese with/without newlines.
        self.expect("(")
        if (self.code.top.token == token.NL):
            self.expect(token.NL)
            multiple = True
        else:
            multiple = False

        # Get arguments with potential indent.
        self.args = ArgumentDocument(
            self.PATH, self.LEVEL + int(multiple), self.HIERARCHY,
            multiple=multiple,
        )
        self.args.parse(self.code)

        # Right paranthese with/without newlines.
        self.expect(")", "->")

        # Get returns.
        self.returns = ReturnDocument(self.PATH, self.LEVEL, self.HIERARCHY)
        self.returns.parse(self.code)

        # Finish definition line.
        self.expect(":", token.NEWLINE)

        # Get class document string.
        self.doc = FunctionDocDocument(
            self.PATH, self.LEVEL + 1, self.HIERARCHY,
        )
        self.doc.parse(self.code)

        # Validate description.
        self.validate()

        # Log parsed decorators.
        for itr in self.decorates:
            info2(
                "{:s} Decorator \033[34;4m@{:s}\033[0m.",
                self.position, itr.name,
            )

        # Log parsed function.
        info2(
            "{:s} Function \033[34;1;4m{:s}\033[0m.",
            self.position, self.name,
        )
        info1(
            "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
            "\n".join([" ".join(itr) for itr in self.doc.paragraphs]),
        )

        # Log parsed function argument description.
        for (name, hint), (_, paragraphs) in zip(
            self.args.children, self.doc.args,
        ):
            if (name in ("self", "cls", "*args", "**kargs")):
                info2(
                    "{:s} Argument \033[31;4m{:s}\033[0m.",
                    self.position, name,
                )
            else:
                info2(
                    "{:s} Argument \033[31;4m{:s}\033[0m: " \
                    "\033[33;4m{:s}\033[m.",
                    self.position, name, hint.full_name,
                )
                info1(
                    "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
                    "\n".join([" ".join(itr) for itr in paragraphs]),
                )

        # Log parsed function return description.
        if (self.returns.multiple):
            for hint, (name, paragraphs) in zip(
                self.returns.children, self.doc.returns,
            ):
                info2(
                    "{:s} Return \033[33;1;4m{:s}\033[0m: " \
                    "\033[33;4m{:s}\033[m.",
                    self.position, name, hint.full_name,
                )
                info1(
                    "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
                    "\n".join([" ".join(itr) for itr in paragraphs]),
                )
        elif (len(self.doc.returns) == 0):
            info2(
                "{:s} Return \033[33;1;4m{:s}\033[0m.",
                self.position, "(no-return)",
            )
        else:
            hint = self.returns
            name, paragraphs = self.doc.returns[0]
            info2(
                "{:s} Return \033[33;1;4m{:s}\033[0m: " \
                "\033[33;4m{:s}\033[m.",
                self.position, name, hint.full_name,
            )
            info1(
                "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
                "\n".join([" ".join(itr) for itr in paragraphs]),
            )

        # Get code series of the class.
        self.series = SeriesDocument(self.PATH, self.LEVEL + 1, self.HIERARCHY)
        self.series.parse(self.code)

    def validate(self) -> None:
        r"""
        Validate description with arguments and returns.

        Args
        ----
        - self

        Returns
        -------

        """
        # Arguments should match on length and names.
        if (len(self.args.children) != len(self.doc.args)):
            error(
                "{:s}, \"{:s}\", {:s}, argument definition and description" \
                " does not match on length.",
                "{:s}.parse".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError
        else:
            pass
        for i, ((name_def, _), (name_des, _)) in enumerate(zip(
            self.args.children, self.doc.args,
        )):
            if (name_def == name_des):
                pass
            else:
                error(
                    "{:s}, \"{:s}\", {:s}, argument {:d} does not match" \
                    " (definition: {:s}, description: {:s}).",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        self.position,
                    ),
                    i, name_def, name_des,
                )
                raise RuntimeError

        # Returns should match on length except for no return case.
        if (self.returns.multiple):
            if (len(self.returns.children) != len(self.doc.returns)):
                error(
                    "{:s}, \"{:s}\", {:s}, return definition and description" \
                    " does not match on length.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        self.position,
                    ),
                )
                raise RuntimeError
            else:
                pass
        elif (self.returns.name != "None"):
            if (len(self.doc.returns) != 1):
                error(
                    "{:s}, \"{:s}\", {:s}, return definition and description" \
                    " does not match on length.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        self.position,
                    ),
                )
                raise RuntimeError
            else:
                pass
        else:
            if (len(self.doc.returns) == 0):
                pass
            else:
                error(
                    "{:s}, \"{:s}\", {:s}, no-return should not have any" \
                    " description.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        self.position,
                    ),
                )
                raise RuntimeError

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Generate super link to code position.
        position = "{:s}/blob/master/{:s}#L{:s}".format(
            self.GITHUB, self.PATH,
            self.position[1:-1].split(", ")[0].split(" ")[1],
        )

        # Get all argument names.
        arg_names = []
        for itr in self.args.children:
            if (itr[0] == "*args"):
                arg_names.append("\\*args")
            elif (itr[0] == "**kargs"):
                arg_names.append("\\*\\*kargs")
            else:
                arg_names.append(itr[0])
        arg_names = ", ".join(arg_names)

        # Use function and argument names as title.
        if (len(arg_names) == 0):
            notes = [
                "- Function [**{:s}**]({:s})()".format(
                    self.name, position,
                ),
            ]
        else:
            notes = [
                "- Function [**{:s}**]({:s})(*{:s}*)".format(
                    self.name, position, arg_names,
                ),
            ]

        # Add the description paragraphs to notes with indent.
        notes.append("")
        for itr in self.doc.paragraphs:
            notes.append("  {:s}".format(" ".join(itr)))

        # Add decorators to notes with indent.
        notes.append("")
        notes.append("  > **Decorators**")
        if (len(self.decorates) == 0):
            notes.append("  > No decorators.")
        else:
            for i, itr in enumerate(self.decorates):
                notes.append("  > {:d}. {:s}".format(i + 1, itr.name))

        # Add arguments to notes with indent.
        notes.append("")
        notes.append("  > **Arguments**")
        if (len(self.args.children) == 0):
            notes.append("  > No arguments.")
        else:
            for (name, hint), (_, paragraphs) in zip(
                self.args.children, self.doc.args,
            ):
                if (name in ("self", "cls")):
                    notes.append("  > - **{:s}**".format(name))
                elif (name == "*args"):
                    notes.append("  > - **{:s}**".format("\\*args"))
                elif (name == "**kargs"):
                    notes.append("  > - **{:s}**".format("\\*\\*kargs"))
                else:
                    notes.append(
                        "  > - **{:s}**: *{:s}*".format(name, hint.full_name),
                    )
                    for itr in paragraphs:
                        notes.append("  >   {:s}".format(" ".join(itr)))

        # Add returns to notes with indent.
        notes.append("")
        notes.append("  > **Returns**")
        if (self.returns.multiple):
            for hint, (name, paragraphs) in zip(
                self.returns.children, self.doc.returns,
            ):
                notes.append(
                    "  > - **{:s}**: *{:s}*".format(name, hint.full_name),
                )
                for itr in paragraphs:
                    notes.append("  >   {:s}".format(" ".join(itr)))
        elif (len(self.doc.returns) == 0):
            notes.append("  > No returns.")
        else:
            hint = self.returns
            name, paragraphs = self.doc.returns[0]
            notes.append(
                "  > - **{:s}**: *{:s}*".format(name, hint.full_name),
            )
            for itr in paragraphs:
                notes.append("  >   {:s}".format(" ".join(itr)))
        return notes


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Block Code Document Objects >>
# Code document on block level. This document will deal with a series of
# consecutive code lines (without any blank lines or dedent) starting with or
# without comment descriptions.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class BlockDocument(CodeDocument):
    r"""
    Document for a block of code lines.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.paragraphs = None
        self.children = []

        # Traverse comments as description.
        buf = []
        while (
            not self.code.eof() and self.code.fit(self.LEVEL, token.COMMENT)
        ):
            buf.append(self.code.top.text[2:])
            self.expect(token.COMMENT, token.NL)
        if (len(buf) == 0):
            if (self.HIERARCHY == SHORT):
                pass
            else:
                error(
                    "{:s}, \"{:s}\", {:s}, non-branch block requires" \
                    " description.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        self.position,
                    ),
                )
                raise RuntimeError
        else:
            self.paragraphs = self.code.paragraphs(buf)

        # Log parsed block.
        info2(
            "{:s} Block \033[30;1;4m{:s}\033[0m.",
            self.position, self.position,
        )
        if (self.paragraphs is None):
            pass
        else:
            info1(
                "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
                "\n".join([" ".join(itr) for itr in self.paragraphs]),
            )

        # Traverse code lines until dedent.
        while (not self.code.eof() and self.code.fit(self.LEVEL, None)):
            # NL does not check indent, thus it is a special ending.
            if (self.code.fit(self.LEVEL, token.NL)):
                break
            else:
                pass

            # There are multiple types of code lines.
            if (self.code.fit(self.LEVEL, "if")):
                child_cls = IfDocument
            elif (self.code.fit(self.LEVEL, "elif")):
                child_cls = ElifDocument
            elif (self.code.fit(self.LEVEL, "else")):
                child_cls = ElseDocument
            elif (self.code.fit(self.LEVEL, "while")):
                child_cls = WhileDocument
            elif (self.code.fit(self.LEVEL, "for")):
                child_cls = ForDocument
            else:
                child_cls = OperateDocument

            # If-elif-else is strictly paired.
            if (len(self.children) > 0):
                flag1 = (isinstance(self.children[-1], IfDocument))
                flag2 = (isinstance(self.children[-1], ElifDocument))
            else:
                flag1 = False
                flag2 = False
            if (flag1 or flag2):
                if (child_cls in (ElifDocument, ElseDocument)):
                    pass
                else:
                    now = self.code.top.position
                    error(
                        "{:s}, \"{:s}\", {:s}, if-elif-else is strictly" \
                        " paired together.",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.PATH,
                        "\033[31;1;47;1m{:s}\033[0m".format(now),
                    )
                    raise RuntimeError
            else:
                pass

            # Parse the child code lines.
            child = child_cls(self.PATH, self.LEVEL, SHORT)
            child.parse(self.code)
            self.children.append(child)


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Line Code Document Objects >>
# Code document on line level. These documents will memorize essential
# information inside a single code line. They also deal with other cases, e.g.,
# arguments, return type hints and so on.
#
# A single code line may corresponds to multiple text lines, e.g., multiple
# lines between a pair of parantheses. Slash line break for too long text lines
# is forbidden except for strings.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ImportDocument(CodeDocument):
    r"""
    Document for an import code line.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.identifiers = []

        # Differentiate import/from-import.
        if (self.code.fit(self.LEVEL, "import")):
            self.expect("import")
            self.parse_name()
            self.identifiers.append(None)
        else:
            self.expect("from")
            self.parse_name()
            self.expect("import")
            self.parse_identifiers()
        self.expect(token.NEWLINE)

    def parse_name(self) -> None:
        r"""
        Parse name.

        Args
        ----
        - self

        Returns
        -------

        """
        # First name is necessary.
        names = [self.code.top.text]
        self.expect(token.NAME)

        # Append all dotted submodules.
        while (not self.code.eof() and self.code.fit(self.LEVEL, ".")):
            self.expect(".")
            names.append(self.code.top.text)
            self.expect(token.NAME)
        self.name = ".".join(names)

    def parse_identifiers(self) -> None:
        r"""
        Parse identifiers.

        Args
        ----
        - self

        Returns
        -------

        """
        # First identifier is necessary.
        self.identifiers.append(self.code.top.text)
        self.expect(token.NAME)

        # Append all commaed identifiers.
        while (not self.code.eof() and self.code.fit(self.LEVEL, ",")):
            self.expect(",")
            self.identifiers.append(self.code.top.text)
            self.expect(token.NAME)


class ConstDocument(CodeDocument):
    r"""
    Document for a constant code line.
    """
    def __init__(self, *args, constants: List[Union[int, str]]) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - constants
            Constant words in the code line.

        Returns
        -------

        """
        # Super.
        CodeDocument.__init__(self, *args)

        # Save necessary attributes.
        self.CONSTS = constants

    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Constant code line only need verification.
        self.code = code
        self.expect(*self.CONSTS)


class DocStringDocument(CodeDocument):
    r"""
    Document for a document string for class/function.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.paragraphs = None

        # This only covers a string.
        raw = self.code.top.text
        self.expect(token.STRING, token.NEWLINE)

        # Multiple-line string should also fit indent level.
        buf = raw.split("\n")
        for i, itr in enumerate(buf[1:]):
            # Check indent level.
            if (len(itr) == 0):
                num_spaces = 0
                level = None
            else:
                num_spaces = len(itr) - len(itr.lstrip())
                level = num_spaces // self.code.UNIT
            flag = (level is None or level >= self.LEVEL)
            if (flag and num_spaces % self.code.UNIT == 0):
                pass
            else:
                error(
                    "{:s}, \"{:s}\", {:s}, expect document string with at" \
                    " least {:d} spaces (unit: {:d}), but get {:d} spaces.",
                    "{:s}.expect".format(self.__class__.__name__),
                    self.PATH,
                    "\033[31;1;47;1m{:s}\033[0m".format(
                        self.position,
                    ),
                    self.LEVEL * self.code.UNIT, self.code.UNIT, num_spaces,
                )
                raise RuntimeError

            # Clear spaces for later usage.
            buf[i + 1] = itr.strip()

        # Document string has constant head and tail.
        if (buf[0] == "r\"\"\"" and buf[-1] == "\"\"\""):
            buf = buf[1:-1]
        else:
            error(
                "{:s}, \"{:s}\", {:s}, document string requires constant" \
                " head \"r\"\"\"\" and tail \"\"\"\"\" lines.",
                "{:s}.expect".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError

        # Broadcast buffer for inheritence.
        self.buf = buf


class ClassDocDocument(DocStringDocument):
    r"""
    Document for a document string for class.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Super.
        DocStringDocument.parse(self, code)

        # Remaining buffer should only be paragraphs.
        self.paragraphs = self.code.paragraphs(self.buf)


class FunctionDocDocument(DocStringDocument):
    r"""
    Document for a document string for function.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Super.
        DocStringDocument.parse(self, code)

        # Split buffer into 4 parts by blank lines.
        parts = [[]]
        for itr in self.buf:
            if (len(itr) == 0 and len(parts) < 4):
                parts.append([])
            else:
                parts[-1].append(itr)
        if (len(parts) == 4):
            pass
        else:
            error(
                "{:s}, \"{:s}\", {:s}, function document requires 4 parts" \
                " separated by 3 blank lines in total.",
                "{:s}.expect".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError

        # First buffer should only be paragraphs.
        self.paragraphs = self.code.paragraphs(parts[0])

        # Log parsed function description.
        debug(
            "{:s}, {:s} Function Description:\n" \
            "\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
            "{:s}.parse".format(self.__class__.__name__),
            self.position,
            "\n".join([" ".join(itr) for itr in self.paragraphs]),
        )

        # Second buffer should be arguments.
        self.args = self.parse_args(parts[1])

        # Third buffer should be returns.
        self.returns = self.parse_returns(parts[2])

        # Fourth buffer is optional, and supports math & code.
        if (len(parts[3]) == 0):
            self.details = None
        else:
            self.details = self.parse_details(parts[3])

    def parse_args(self, part: List[str]) -> List[Tuple[str, List[List[str]]]]:
        r"""
        Parse argument description.

        Args
        ----
        - self
        - part
            Text content of argument description.

        Returns
        -------
        - desc
            A list of argument names and their description paragraphs.

        """
        # Argument description has constant head.
        if (part[0] == "Args" and part[1] == "----"):
            part = part[2:]
        else:
            error(
                "{:s}, \"{:s}\", {:s}, function argument document requires" \
                " constant head:\n\"\"\"\nArgs\n----\n\"\"\".",
                "{:s}.expect".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError

        # Traverse all argument names starting with "- ".
        desc = []
        for itr in part:
            if (itr[0:2] == "- "):
                name = itr[2:len(itr)]
                desc.append([name, []])
            else:
                desc[-1][1].append(itr)
        for i in range(len(desc)):
            if (desc[i][0] in ("self", "cls", "*args", "**kargs")):
                desc[i][1] = None
            else:
                desc[i][1] = self.code.paragraphs(desc[i][1])

        # Log parsed function argument description.
        for name, paragraphs in desc:
            if (name in ("self", "cls", "*args", "**kargs")):
                debug(
                    "{:s}, {:s} Argument Description \033[31;4m{:s}\033[0m.",
                    "{:s}.parse_args".format(self.__class__.__name__),
                    self.position, name,
                )
            else:
                debug(
                    "{:s}, {:s} Argument Description \033[31;4m{:s}\033[0m:" \
                    "\n\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
                    "{:s}.parse_args".format(self.__class__.__name__),
                    self.position, name,
                    "\n".join([" ".join(itr) for itr in paragraphs]),
                )
        return desc

    def parse_returns(
        self, part: List[str],
    ) -> List[Tuple[str, List[List[str]]]]:
        r"""
        Parse return description.

        Args
        ----
        - self
        - part
            Text content of return description.

        Returns
        -------
        - desc
            A list of return names and their description paragraphs.

        """
        # Argument description has constant head.
        if (part[0] == "Returns" and part[1] == "-------"):
            part = part[2:len(part)]
        else:
            error(
                "{:s}, \"{:s}\", {:s}, function return document requires" \
                " constant head:\n\"\"\"\nReturns\n-------\n\"\"\".",
                "{:s}.expect".format(self.__class__.__name__),
                self.PATH,
                "\033[31;1;47;1m{:s}\033[0m".format(
                    self.position,
                ),
            )
            raise RuntimeError

        # Traverse all return names starting with "- ".
        desc = []
        for itr in part:
            if (itr[0:2] == "- "):
                name = itr[2:len(itr)]
                desc.append([name, []])
            else:
                desc[-1][1].append(itr)
        for i in range(len(desc)):
            desc[i][1] = self.code.paragraphs(desc[i][1])

        # Log parsed function argument description.
        for name, paragraphs in desc:
            debug(
                "{:s}, {:s} Return Description \033[31;4m{:s}\033[0m:" \
                "\n\"\"\"\n\033[30;1;4m{:s}\033[m\n\"\"\".",
                "{:s}.parse_returns".format(self.__class__.__name__),
                self.position, name,
                "\n".join([" ".join(itr) for itr in paragraphs]),
            )
        return desc


class DecorateDocument(CodeDocument):
    r"""
    Document for a function decorator line.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.name = None
        self.inputs = None

        # Get decorator name.
        self.name = self.code.preview(1).text
        self.expect("@", token.NAME)

        # Log parsed decorator ahead of potential inputs.
        debug(
            "{:s}, {:s} Decorator \033[34;4m@{:s}\033[0m.",
            "{:s}.parse".format(self.__class__.__name__),
            self.position, self.name,
        )

        # Get decorator inputs.
        self.expect(token.NEWLINE)


class ArgumentDocument(CodeDocument):
    r"""
    Document for function arguments.
    """
    def __init__(self, *args, multiple: bool) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - multiple
            If True, the arguments are cross-line.

        Returns
        -------

        """
        # Super.
        CodeDocument.__init__(self, *args)

        # Save necessary attributes.
        self.MULTIPLE = multiple

    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.children = []

        # Parse each pair of name and type hint.
        while (True):
            # Check ending signal.
            if (self.code.eof() or self.code.fit(
                self.LEVEL - int(self.MULTIPLE), ")",
            )):
                break
            else:
                pass

            # Get name first.
            buf = []
            if (self.code.top.text in ("*", "**")):
                buf.append(self.code.top.text)
                self.expect(token.OP)
            else:
                pass
            buf.append(self.code.top.text)
            self.expect(token.NAME)
            name = "".join(buf)

            # Parse hint except for some special names.
            if (name in ("self", "cls", "*args", "**kargs")):
                hint = None
            else:
                self.expect(":")
                hint = TypeHintDocument(self.PATH, self.LEVEL, self.HIERARCHY)
                hint.parse(self.code)
            self.children.append((name, hint))

            # Log parsed argument ahead of description.
            if (name in ("self", "cls", "*args", "**kargs")):
                debug(
                    "{:s}, {:s} Argument \033[31;4m{:s}\033[0m.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.position, name,
                )
            else:
                debug(
                    "{:s}, {:s} Argument \033[31;4m{:s}\033[0m: " \
                    "\033[33;4m{:s}\033[m.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.position, name, hint.full_name,
                )

            # Deal with seperator except ending paranthese.
            if (self.code.fit(self.LEVEL, ")")):
                break
            else:
                self.expect(",")

            # Deal with cross-line definitions.
            if (self.MULTIPLE and self.code.fit(self.LEVEL, token.NL)):
                self.expect(token.NL)
            else:
                pass


class TypeHintDocument(CodeDocument):
    r"""
    Document for a type hint.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.name = None
        self.children = []

        # Parse type name of current level.
        buf = [self.code.top.text]
        self.expect(token.NAME)
        while (not self.code.eof() and self.code.fit(self.LEVEL, ".")):
            buf.append(self.code.preview(1).text)
            self.expect(".", token.NAME)
        self.name = ".".join(buf)

        # Parse potential children level.
        if (self.code.fit(self.LEVEL, "[")):
            # Left paranthese.
            self.expect("[")

            # Conside type hint of multiple lines.
            if (self.code.fit(self.LEVEL, token.NL)):
                self.expect(token.NL)
                offset = 1
            else:
                offset = 0

            # Parse all children type hints.
            child = TypeHintDocument(
                self.PATH, self.LEVEL + offset, self.HIERARCHY,
            )
            child.parse(self.code)
            self.children.append(child)
            while (not self.code.eof() and not self.code.fit(self.LEVEL, "]")):
                self.expect(",")
                child = TypeHintDocument(
                    self.PATH, self.LEVEL + offset, self.HIERARCHY,
                )
                child.parse(self.code)
                self.children.append(child)

            # Right paranthese.
            self.expect("]")
        else:
            pass

    @property
    def full_name(self) -> str:
        r"""
        Get full name including all children for the type hint.

        Args
        ----
        - self

        Returns
        -------
        - msg
            Full name.

        """
        # Recursively construct.
        if (len(self.children) > 0):
            children_names = [itr.full_name for itr in self.children]
            return "{:s}[{:s}]".format(self.name, ", ".join(children_names))
        else:
            return self.name


class ReturnDocument(TypeHintDocument):
    r"""
    Document for function arguments.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Super.
        TypeHintDocument.parse(self, code)

        # Log all parsed returns ahead of description.
        if (self.multiple):
            for itr in self.children:
                debug(
                    "{:s}, {:s} Return \033[33;4m{:s}\033[m.",
                    "{:s}.parse".format(self.__class__.__name__),
                    self.position, itr.full_name,
                )
        else:
            debug(
                "{:s}, {:s} Return \033[33;4m{:s}\033[m.",
                "{:s}.parse".format(self.__class__.__name__),
                self.position, self.full_name,
            )

    @property
    def multiple(self) -> bool:
        r"""
        Check if this is a multiple-return document.

        Args
        ----
        - self

        Returns
        -------
        - flag
            If True, this is a multiple-return document.

        """
        # Check directly.
        return self.name == "MultiReturn"


class OperateDocument(CodeDocument):
    r"""
    Document for an operation code line.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.memory = []

        # Traverse the whole line.
        while (True):
            # Check ending signal.
            if (self.code.eof() or self.code.fit(self.LEVEL, token.NEWLINE)):
                break
            else:
                pass

            # Put the whole line into token memory.
            if (self.code.top.text in ParantheseDocument.KEYS):
                # Pay attention to parantheses.
                child = ParantheseDocument(
                    self.PATH, self.LEVEL, self.HIERARCHY,
                    left=self.code.top.text,
                )
                child.parse(self.code)
                self.memory.append(child)
            else:
                # Commonly save token word to memory.
                self.memory.append(self.code.top)
                self.expect(None)
        self.expect(token.NEWLINE)


class ConditionDocument(CodeDocument):
    r"""
    Document for a conditional code line.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.position = self.code.top.position
        self.condition = None
        self.child = None

        # Fetch keyword first.
        self.expect(self.KEYWORD)

        # Parse the condition wrapped by round paranthese.
        self.condition = ParantheseDocument(
            self.PATH, self.LEVEL, self.HIERARCHY, left="(",
        )
        self.condition.parse(self.code)

        # Condition requires constant tail.
        self.expect(":", token.NEWLINE)

        # Parse deeper series of codes.
        self.child = SeriesDocument(self.PATH, self.LEVEL + 1, SHORT)
        self.child.parse(self.code)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Add children blocks.
        if (self.condition.multiple):
            notes = []
            notes.append("{:s} (".format(self.KEYWORD))
            notes.extend("".join(self.cat(self.condition.memory)).split("\n"))
            notes.append("):")
        else:
            notes = "".join(self.cat(self.condition.memory)).split("\n")
            notes[0] = "{:s} ({:s}".format(self.KEYWORD, notes[0])
            notes[-1] = "{:s}):".format(notes[-1])
        for itr in self.child.markdown():
            notes.append("    {:s}".format(itr))
        return notes


class IfDocument(ConditionDocument):
    r"""
    Document for an if-statement code line.
    """
    # Define constants.
    KEYWORD = "if"


class ElifDocument(ConditionDocument):
    r"""
    Document for an elif-statement code line.
    """
    # Define constants.
    KEYWORD = "elif"


class ElseDocument(CodeDocument):
    r"""
    Document for an else-statement code line.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.memory = []
        self.child = None

        # Fetch keyword.
        self.expect("else", ":", token.NEWLINE)

        # Parse child series of codes.
        self.child = SeriesDocument(self.PATH, self.LEVEL + 1, SHORT)
        self.child.parse(self.code)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Add children blocks.
        notes = ["else:"]
        for itr in self.child.markdown():
            notes.append("    {:s}".format(itr))
        return notes


class WhileDocument(ConditionDocument):
    r"""
    Document for a while-statement code line.
    """
    # Define constants.
    KEYWORD = "while"


class ForDocument(CodeDocument):
    r"""
    Document for a for-statement code line.
    """
    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.ptr = []
        self.buf = []
        self.child = None

        # Fetch head keyword.
        self.expect("for")

        # Fetch iterative pointers.
        while (not self.code.eof() and not self.code.fit(self.LEVEL, "in")):
            self.ptr.append(self.code.top)
            self.expect(None)

        # Fetch middle word.
        self.expect("in")

        # Fetch iteration buffer.
        while (not self.code.eof() and not self.code.fit(self.LEVEL, ":")):
            if (self.code.top.text in ParantheseDocument.KEYS):
                # Pay attention to parantheses.
                child = ParantheseDocument(
                    self.PATH, self.LEVEL, self.HIERARCHY,
                    left=self.code.top.text,
                )
                child.parse(self.code)
                self.buf.append(child)
            else:
                # Commonly save token word to memory.
                self.buf.append(self.code.top)
                self.expect(None)

        # Fetch constant tail.
        self.expect(":", token.NEWLINE)

        # Parse deeper series of codes.
        self.child = SeriesDocument(self.PATH, self.LEVEL + 1, SHORT)
        self.child.parse(self.code)

    def markdown(self) -> List[str]:
        r"""
        Generate Markdown.

        Args
        ----
        - self

        Returns
        -------
        - notes
            Markdown notes.

        """
        # Add children blocks.
        notes = "".join(self.cat(self.buf)).split("\n")
        notes[0] = "for {:s} in {:s}".format(
            "".join(self.cat(self.ptr)), notes[0],
        )
        notes[-1] = "{:s}:".format(notes[-1])
        for itr in self.child.markdown():
            notes.append("    {:s}".format(itr))
        return notes


class ParantheseDocument(CodeDocument):
    r"""
    Document for a cross-line paranthese code line.
    """
    # Define consntants.
    DICT = {
        "(": ")",
        "[": "]",
        "{": "}",
    }
    KEYS = ["(", "[", "{"]

    def __init__(self, *args, left: str) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - left
            Left paranthese.

        Returns
        -------

        """
        # Super.
        CodeDocument.__init__(self, *args)

        # Save necessary attributes.
        self.LEFT = left
        self.RIGHT = self.DICT[left]

    def parse(self, code: Code) -> None:
        r"""
        Parse content.

        Args
        ----
        - self
        - code
            Tokenized code.

        Returns
        -------

        """
        # Save necessary attributes.
        self.code = code
        self.multiple = None
        self.memory = []

        # Fetch paranthese head.
        self.expect(self.LEFT)

        # Identity if there are multiple lines.
        if (self.code.fit(self.LEVEL, token.NL)):
            self.expect(token.NL)
            self.multiple = True
        else:
            self.multiple = False

        # Shift level by multiple-line flag.
        self.LEVEL += int(self.multiple)

        # Parse each line inside the paranthese pair.
        while (True):
            # Check ending signal.
            if (self.code.eof() or self.code.fit(
                self.LEVEL - int(self.multiple), self.RIGHT,
            )):
                break
            else:
                pass

            # Put all tokens inside paranthese into memory.
            if (self.code.top.text in self.KEYS):
                # Parse deeper paranthese if necessary.
                child = ParantheseDocument(
                    self.PATH, self.LEVEL, self.HIERARCHY,
                    left=self.code.top.text,
                )
                child.parse(self.code)
                self.memory.append(child)
            elif (self.code.fit(self.LEVEL, token.NL)):
                # Deal with new lines inside parantheses only in multiple-line
                # mode.
                if (self.multiple):
                    pass
                else:
                    now = self.code.top.position
                    error(
                        "{:s}, \"{:s}\", {:s}, new lines only exist in" \
                        " multiple-line mode paranthese.",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.PATH,
                        "\033[31;1;47;1m{:s}\033[0m".format(now),
                    )
                    raise RuntimeError

                # Comma break is essential except for round paranthese.
                obj = self.code.preview(-1)
                if (isinstance(obj, Word) and obj.text == ","):
                    self.expect(token.NL)
                    self.memory.append("\n")
                    continue
                elif (self.LEFT == "("):
                    self.expect(token.NL)
                    break
                else:
                    now = obj.position
                    error(
                        "{:s}, \"{:s}\", {:s}, new lines must end by line" \
                        " break \",\".",
                        "{:s}.parse".format(self.__class__.__name__),
                        self.PATH,
                        "\033[31;1;47;1m{:s}\033[0m".format(now),
                    )
                    raise RuntimeError
            else:
                # Commonly save token word to memory.
                self.memory.append(self.code.top)
                self.expect(None)

        # Recover level by multiple-line flag.
        self.LEVEL -= int(self.multiple)

        # Fetch paranthese tail.
        self.expect(self.RIGHT)


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main Branch >>
# Main branch starts here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


def script_logger() -> logging.Logger:
    r"""
    Create script logger.

    Args
    ----

    Returns
    -------
    - logger
        Default logger.

    """
    # Set logging level.
    LEVEL = WARNING

    # Allocate logger.
    logger = logging.getLogger(__file__)
    logger.setLevel(level=LEVEL)

    # Define logging line format.
    formatter = logging.Formatter("%(message)s")

    # Define console streaming.
    console_stream = logging.StreamHandler()
    console_stream.setLevel(level=LEVEL)
    console_stream.setFormatter(formatter)

    # Add stream to logger.
    logger.addHandler(console_stream)
    return logger


def main(root: str) -> None:
    r"""
    Main branch.

    Args
    ----
    - root
        Root.

    Returns
    -------

    """
    # Reset logging level.
    update_universal_logger(script_logger())

    # Get the document.
    DirectoryDocument().parse(root)


# Main entrance.
if (__name__ == "__main__"):
    # Run the checker.
    root = os.getcwd()
    if (os.path.basename(root) == "MLRepo"):
        main(root)
    else:
        error("Must run from MLRepo root.")
        raise RuntimeError
else:
    pass