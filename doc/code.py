# Import future.
from __future__ import annotations

# Import typing.
from typing import Any
from typing import Tuple as MultiReturn
from typing import Union, List

# Import dependencies.
import sys
import os
import tokenize
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


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Code Objects >>
# Tokenized code for any arbitrary file is defined based on Python token
# library.
# Each tokenized code word is automatically attached with its indent level for
# later styled document check.
#
# Style related constants and utility functions are also defined.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Word(object):
    r"""
    Token word.
    """
    def set(
        self: Word, *args: object,
        val: int, text: str, row: int, column: int, **kargs: object,
    ) -> None:
        r"""
        Set word attributes.

        Args
        ----
        - self
        - *args
        - val
            Token integer.
        - text
            Token text content.
        - row
            Token row index.
        - column
            Token column index.
        - **kargs

        Returns
        -------

        """
        # Save necessary attributes.
        self.token = val
        self.token_string = token.tok_name[self.token]
        self.text = text
        self.row = row
        self.column = column

    def position(self: Word, *args: object, **kargs: object) -> str:
        r"""
        Get position string.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - msg
            Position string.

        """
        # Get indent level, line (row) and column.
        return "line {:d}, column: {:d}".format(self.row, self.column)

    def check(
        self: Word, target: Union[int, str], *args: object, **kargs: object,
    ) -> bool:
        r"""
        Check given arguments with memory.

        Args
        ----
        - self
        - target
            Target.
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, the target is satisfied by scanning memory.

        """
        # Check attribute according to target type.
        if (isinstance(target, int)):
            return self.token == target
        else:
            return self.text == target


class Line(object):
    r"""
    Line of tokens.
    """
    def set(
        self: Line, *args: object, level: int, text: str, path: str, row: int,
        **kargs: object,
    ) -> None:
        r"""
        Set line attributes.

        Args
        ----
        - self
        - *args
        - level
            Indent level.
        - text
            Raw code text.
        - path
            Path to the file of the line.
        - row
            Line row ID in the file of the line.
        - **kargs

        Returns
        -------

        """
        # Save necessary attributes.
        self.level = level
        self.implicit = False
        self.text = text
        self.path = path
        self.row = row
        self.memory: List[Word] = []

    def append(self: Line, word: Word, *args: object, **kargs: object) -> None:
        r"""
        Append a word starting from the line.

        Args
        ----
        - self
        - word
            Appending word.
        - *args
        - **kargs

        Returns
        -------

        """
        # Append directly
        self.memory.append(word)

    def reset(self: Line, *args: object, **kargs: object) -> None:
        r"""
        Reset scanning status.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Reset scanning pointer.
        self.scan = 0

    def check(
        self: Line, target: Union[int, str], *args: object, level: int,
        **kargs: object,
    ) -> bool:
        r"""
        Check given arguments with memory.

        Args
        ----
        - self
        - target
            Target.
        - *args
        - level
            Required indent level.
        - **kargs

        Returns
        -------
        - flag
            If True, the target is satisfied by scanning memory.

        """
        # Check indent level.
        if (self.level != level):
            return False
        else:
            pass

        # Check scanning word.
        return self.get().check(target)

    def match(
        self: Line, target: Union[int, str], *args: object, level: int,
        **kargs: object,
    ) -> None:
        r"""
        Match given arguments with memory.

        Args
        ----
        - self
        - target
            Target.
        - *args
        - level
            Required indent level.
        - **kargs

        Returns
        -------

        It is a more strict version of check function that target must be
        satisfied.
        Otherwise, runtime error will be reported.
        """
        # Check indent level.
        if (self.level != level):
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " wrong indent level.",
                self.path, "line {:d}".format(self.row),
            )
            raise RuntimeError
        else:
            pass

        # Match scanning.
        obj = self.get()
        if (obj.check(target)):
            pass
        elif (isinstance(target, int)):
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " expect {:s}, but get {:s}.",
                self.path, obj.position(),
                token.tok_name[target], obj.token_string,
            )
            raise RuntimeError
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " expect \"{:s}\", but get \"{:s}\".",
                self.path, obj.position(),
                repr(target)[1:-1], repr(obj.text)[1:-1],
            )
            raise RuntimeError

        # Move to next if match successfully.
        self.next()

    def get(self: Line, *args: object, **kargs: object) -> Word:
        r"""
        Get scanning word.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - word
            Scanning word.

        """
        # Get directly.
        return self.memory[self.scan]

    def next(self: Line, *args: object, **kargs: object) -> None:
        r"""
        Move pointer to next word.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Move to next non-trivial pointer.
        self.scan += 1
        while (not self.eol() and self.get().token == token.INDENT):
            self.scan += 1

    def eol(self: Line, *args: object, **kargs: object) -> bool:
        r"""
        Get EOL signal.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            Signal for EOL.

        """
        # Get directly.
        return self.scan == len(self.memory)


# Define essential constants.
UNIT = 4
MAX = 79


# Define single word regex.
NUMBER = r"[1-9][0-9]*"
INITIAL = r"([A-Z][A-Za-z]*|{:s})".format(NUMBER)
INSIDE = r"([A-Za-z]+|{:s})".format(NUMBER)


# Overwrite composed word regex.
INITIAL = r"({:s}(-{:s})*)".format(INITIAL, INSIDE)
INSIDE = r"({:s}(-{:s})*)".format(INSIDE, INSIDE)


# Define not-word word regex.
MATH = r"\$([^\n\\\$]|\\[^\n])+\$"
CODE = r"`([^\n\\`]|\\[^\n])+`"
STRING = r"\"([^\n\\\"]|\\[^\n])+\""


# Define sentence word regex.
FIRST = r"({:s}|{:s}|{:s}|{:s})".format(INITIAL, MATH, CODE, STRING)
LATER = r"({:s}|{:s}|{:s}|{:s})".format(INSIDE, MATH, CODE, STRING)
BREAK = r"( |, )"


# Define sentence regex.
PARANTHESE = r"\({:s}({:s}{:s})*\)".format(LATER, BREAK, LATER)
SENTENCE = r"^{:s}({:s}{:s}({:s}{:s})?)*.$".format(
    FIRST, BREAK, LATER, BREAK, PARANTHESE,
)


class Code(object):
    r"""
    Tokenized code with indent of a file.
    """
    def __init__(self: Code, *args: object, **kargs: object) -> None:
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
        # Nothing is requires.
        pass

    def load_file(
        self: Code, path: str, *args: object, **kargs: object,
    ) -> None:
        r"""
        Load code tokens from given file.

        Args
        ----
        - self
        - path
            File path.
        - *args
        - **kargs

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

    def load_texts(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Load text lines from given file.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Read text lines along with indent level.
        self.texts = []
        file = open(self.path, "r")
        eof = False
        for i, line in enumerate(file):
            # Should not read in anything after EOF.
            if (eof):
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " read after EOF (line w.o. tail \"\\n\").",
                    self.path, "line {:d}".format(i + 1),
                )
                raise RuntimeError
            else:
                pass

            # Exclude tail spaces except for "\n".
            rclean = line.rstrip()
            if (len(rclean) == len(line)):
                # Only the last line should have no "\n".
                eof = True
            elif (len(rclean) + 1 == len(line) and line[-1] == "\n"):
                pass
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " find tail spaces.",
                    self.path, "line {:d}".format(i + 1),
                )
                raise RuntimeError

            # Numer of spaces must fit the unit.
            lclean = rclean.lstrip()
            num_spaces = len(rclean) - len(lclean)
            if (num_spaces % UNIT == 0):
                level = num_spaces // UNIT
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " weird indent.",
                    self.path, "line {:d}".format(i + 1),
                )
                raise RuntimeError

            # Blank line is special.
            if (len(lclean) == 0):
                self.texts.append((-1, rclean))
            else:
                self.texts.append((level, rclean))
        file.close()

    def load_tokens(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Load tokens from given file.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Load tokens except indent or dedent.
        self.tokens = []
        file = open(self.path, "r")
        buf = tokenize.generate_tokens(file.readline)
        for itr in buf:
            if (itr[0] in (token.INDENT, token.DEDENT)):
                # Indent token is modified for other usage.
                pass
            else:
                self.tokens.append(itr)
        file.close()

    def rule_texts(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Check rules over text lines.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Check each text lines.
        for i, (_, text) in enumerate(self.texts):
            line_rule_length(text=text, index=i + 1, path=self.path)
            line_rule_char(text=text, index=i + 1, path=self.path)
            line_rule_break(text=text, index=i + 1, path=self.path)

    def review(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Review text lines and tokens as lines of tokens.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Define real buffer.
        self.memory = []
        self.ptrs = []
        for i, (level, text) in enumerate(self.texts):
            line = Line()
            line.set(level=level, text=text, path=self.path, row=i + 1)
            self.memory.append(line)
            self.ptrs.append(0)
        del self.texts

        # Traverse tokens and put to corresponding lines.
        scan = 0
        while (scan < len(self.tokens) - 1):
            # Get the starting token.
            val, text, head, tail, _ = self.tokens[scan]
            head_row, head_col = head
            tail_row, tail_col = tail
            scan += 1

            # Get the space ahead.
            self.clear_space_until(head_row, head_col)

            # Create word.
            word = Word()
            word.set(val=val, text=text, row=head_row, column=head_col)

            # Update line pointer in memory.
            if (val == token.STRING):
                # Update string token (multiple-line or not).
                self.clear_string(word)
            elif (head_row == tail_row):
                # Update single-line token.
                self.clear_common(word)
            else:
                error(
                    "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                    " only string allows multiple-line code.",
                    self.path,
                    "line {:d}, column: {:d}".format(head_row, head_col),
                )
                raise RuntimeError
        del self.tokens
        del self.ptrs

        # Ensure that multiple-line string only involves in definition.
        for itr in self.memory:
            if (itr.implicit and len(itr.memory) > 0):
                if (
                    len(itr.memory) == 1 and itr.memory[0].check(token.NEWLINE)
                ):
                    pass
                else:
                    error(
                        "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                        " Only end of statement can be multiple-line string.",
                        self.path, "line {:d}".format(itr.row),
                    )
                    raise RuntimeError
            else:
                pass

        # Ensure raw code is recoverable.
        self.recoverable()

    def clear_space_until(
        self: Code, row: int, column: int, *args: object, **kargs: object,
    ) -> None:
        r"""
        Clear space at given row from pointer until given column.

        Args
        ----
        - self
        - row
            Given row.
        - column
            Given column (exclusive).
        - *args
        - **kargs

        Returns
        -------

        """
        # Get information of given row.
        row -= 1
        obj = self.memory[row]
        buf = obj.memory
        line = obj.text
        ptr = self.ptrs[row]
        length = column - ptr

        # Update memory.
        if (length == 0):
            # No-space case should be ignored.
            pass
        elif (len(buf) == 0):
            # Spaces of line indent should be ignored.
            pass
        elif (length != 1):
            # Space break can at most have 1 space.
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " space break can at most have 1 space.",
                self.path,
                "line {:d}, column: {:d}".format(row + 1, ptr),
            )
            raise RuntimeError
        else:
            # Use None to represent single-space break token.
            word = Word()
            word.set(val=token.INDENT, text=" ", row=row + 1, column=ptr)
            buf.append(word)

        # Update pointer.
        self.ptrs[row] += length

    def clear_string(
        self: Code, word: Word, *args: object, **kargs: object,
    ) -> None:
        r"""
        Clear and update a possibly multiple-line string token.

        Args
        ----
        - self
        - word
            Word token.
        - *args
        - **kargs

        Returns
        -------

        """
        # Get information of the word.
        row = word.row - 1
        texts = word.text.split("\n")
        num_lines = len(texts)

        # Update memory.
        self.memory[row].append(word)
        for i in range(1, num_lines):
            # Mark as not existing except for the first line.
            if (i > 0):
                self.memory[row + i].implicit = True
            else:
                pass

        # Update pointer.
        for i, text in enumerate(texts):
            self.ptrs[row + i] += len(text)

        # Tail "\\" after string means a concatenation.
        focus = row + num_lines - 1
        ptr = self.ptrs[focus]
        if (self.memory[focus].text[ptr:] == " \\"):
            # Create extra NL word.
            word = Word()
            word.set(val=token.NL, text=" \\\n", row=focus + 1, column=ptr)
            self.memory[focus].append(word)
        else:
            pass

    def clear_common(
        self: Code, word: Word, *args: object, **kargs: object,
    ) -> None:
        r"""
        Clear and update a single-line token.

        Args
        ----
        - self
        - word
            Word token.
        - *args
        - **kargs

        Returns
        -------

        """
        # Get information of the word.
        row = word.row - 1
        length = len(word.text)

        # Update memory.
        self.memory[row].append(word)

        # Update pointer.
        self.ptrs[row] += length

    def recoverable(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Ensure raw code to be recoverable.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Traverse the memory.
        ptr = 0
        while (ptr < len(self.memory)):
            # Get tokens and raw codes.
            tokens = []
            raws = []
            position = ptr + 1
            obj = self.memory[ptr]
            level = obj.level
            tokens.extend(obj.memory)
            raws.append(obj.text)
            ptr += 1
            while (ptr < len(self.memory) and self.memory[ptr].implicit):
                obj = self.memory[ptr]
                tokens.extend(obj.memory)
                raws.append(obj.text)
                ptr += 1

            # Generate by tokens
            texts = [" " * level * UNIT]
            for word in tokens:
                if (word is None):
                    texts.append(" ")
                else:
                    texts.append(word.text)
            generates = "".join(texts).split("\n")

            # Remove trivial generation tail.
            if (len(generates[-1]) == 0):
                del generates[-1]
            else:
                pass

            # Ensure matching.
            for i in range(max(len(raws), len(generates))):
                if (raws[i] != generates[i]):
                    error(
                        "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                        " fail to recover code.",
                        self.path, "line {:d}".format(position + i),
                    )
                    raise RuntimeError
                else:
                    pass

    def reset(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Reset scanning status.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Reset scanning pointer.
        self.scan = 0

    def get(self: Code, *args: object, **kargs: object) -> Line:
        r"""
        Get scanning line.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - line
            Scanning line.

        """
        # Get directly.
        return self.memory[self.scan]

    def next(self: Code, *args: object, **kargs: object) -> None:
        r"""
        Move pointer to next line.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Move directly.
        self.scan += 1

    def eof(self: Code, *args: object, **kargs: object) -> bool:
        r"""
        Get EOF signal.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            Signal for EOF.

        """
        # Get directly.
        return self.scan == len(self.memory)

    def blank_top(
        self: Code, num: int, *args: object, **kargs: object,
    ) -> bool:
        r"""
        Get blank line signal.

        Args
        ----
        - self
        - num
            Number of blank lines.
        - *args
        - **kargs

        Returns
        -------
        - flag
            Signal for single blank line.

        """
        # Fetch lines and check if they are all blank.
        for i in range(num):
            # EOF is equivalent to any number of blank lines.
            if (self.scan + i == len(self.memory)):
                break
            else:
                pass

            # Fetch line and check.
            obj = self.memory[self.scan + i]
            if (len(obj.memory) == 1 and obj.memory[0].check(token.NL)):
                pass
            else:
                return False
        return True

    def blank_next(
        self: Code, num: int, *args: object, **kargs: object,
    ) -> None:
        r"""
        Get blank line and skip.

        Args
        ----
        - self
        - num
            Number of blank lines.
        - *args
        - **kargs

        Returns
        -------

        """
        # Check and skip.
        if (self.blank_top(num)):
            for i in range(num):
                if (self.eof()):
                    break
                else:
                    self.next()
        else:
            error(
                "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
                " expect {:d} blank lines.",
                self.path, "line {:d}".format(self.get().row), num,
            )
            raise RuntimeError


def line_rule_length(
    text: str, *args: object, index: int, path: str, **kargs: object,
) -> None:
    r"""
    Check length rule over a text line.

    Args
    ----
    - text
        Line content.
    - *args
    - index
        Line index.
    - path
        File path.
    - **kargs

    Returns
    -------

    """
    # Text length is limited.
    if (len(text) > MAX):
        error(
            "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
            " too long (>{:d}).",
            path, "line {:d}".format(index),
            MAX,
        )
        raise RuntimeError
    else:
        pass


def line_rule_char(
    text: str, *args: object, index: int, path: str, **kargs: object,
) -> None:
    r"""
    Check character rule over a text line.

    Args
    ----
    - text
        Line content.
    - *args
    - index
        Line index.
    - path
        File path.
    - **kargs

    Returns
    -------

    """
    # Some charaters are rejected.
    if (chr(39) in text):
        error(
            "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
            " invalid char \"{:s}\".",
            path, "line {:d}".format(index),
            chr(39),
        )
        raise RuntimeError
    else:
        pass


def line_rule_break(
    text: str, *args: object, index: int, path: str, **kargs: object,
) -> None:
    r"""
    Check line break rule over a text line.

    Args
    ----
    - text
        Line content.
    - *args
    - index
        Line index.
    - path
        File path.
    - **kargs

    Returns
    -------

    """
    # Line break is rejected except for strings.
    if (text[-2:] == " \\" and text[-3] != "\""):
        error(
            "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
            " line break is disabled.",
            path, "line {:s}".format(index),
        )
        raise RuntimeError
    else:
        pass


def recover(
    memory: List[Word], *args: object, level: int, **kargs: object,
) -> List[str]:
    r"""
    Recover code from given memory of tokens.

    Args
    ----
    - memory
        Memory of tokens.
    - *args
    - level
        Indent level.
    - **kargs

    Returns
    -------
    - texts
        A list of generated code lines.

    """
    # Generate directly
    texts = [" " * level * UNIT]
    for word in memory:
        texts.append(word.text)
    return "".join(texts).split("\n")


def paragraphize(
    texts: List[str], *args: object, **kargs: object,
) -> List[List[str]]:
    r"""
    Transfer a list of texts into paragraphs.

    Args
    ----
    - texts
        Texts.
    - *args
    - **kargs

    Returns
    -------
    - paragraphs
        Paragraphs.

    """
    # Empty is a special case.
    if (len(texts) == 0):
        return []
    else:
        pass

    # Attach an additional blank line as replace of EOP.
    buf = texts + [""]

    # Break texts by single blank line.
    ptr = 0
    paragraphs = []
    while (ptr < len(buf)):
        # Reject empty paragraph.
        if (len(buf[ptr]) == 0):
            error(
                "At comment line {:d}, empty paragraph is rejected.",
                ptr + 1,
            )
            raise RuntimeError
        else:
            pass

        # Take lines for decoding until a blank line.
        start = ptr
        decoding = []
        while (len(buf[ptr]) > 0):
            decoding.append(buf[ptr])
            ptr += 1

        # Decode according to different flags.
        if (decoding[0] == "$$"):
            paragraphs.extend(mathize(decoding, start=start + 1))
        elif (decoding[0][0:3] == "```"):
            paragraphs.extend(codize(decoding, start=start + 1))
        else:
            paragraphs.extend(textize(decoding, start=start + 1))

        # Go over the blank line to move to next.
        ptr += 1
    return paragraphs


def mathize(
    texts: List[str], *args: object, start: int, **kargs: object,
) -> List[List[str]]:
    r"""
    Transfer a list of texts into math block.

    Args
    ----
    - texts
        Texts.
    - *args
    - start
        Starting line in original text.
    - **kargs

    Returns
    -------
    - block
        Math block.

    """
    # Block must end properly.
    if (texts[-1] != "$$"):
        error(
            "At comment line {:d}, multiple-line math starts from" \
            " line {:d} but ends nowhere.",
            start + len(texts) - 1, start,
        )
        raise RuntimeError
    else:
        pass

    # Math block requires no decoding.
    return [[itr] for itr in texts]


def codize(
    texts: List[str], *args: object, start: int, **kargs: object,
) -> List[List[str]]:
    r"""
    Transfer a list of texts into code block.

    Args
    ----
    - texts
        Texts.
    - *args
    - start
        Starting line in original text.
    - **kargs

    Returns
    -------
    - block
        Math block.

    """
    # Block must end properly.
    if (texts[-1] != "```"):
        error(
            "At comment line {:d}, multiple-line code starts from" \
            " line {:d} but ends nowhere.",
            start + len(texts) - 1, start,
        )
        raise RuntimeError
    else:
        pass

    # Math block requires no decoding.
    return [[itr] for itr in texts]


def textize(
    texts: List[str], *args: object, start: int, **kargs: object,
) -> List[List[str]]:
    r"""
    Transfer a list of texts into text block.

    Args
    ----
    - texts
        Texts.
    - *args
    - start
        Starting line in original text.
    - **kargs

    Returns
    -------
    - block
        Math block.

    """
    # Allocate buffer.
    block = []
    buf = []

    # Decode all text in order.
    for i, itr in enumerate(texts):
        buf.append(itr)
        if (itr[-1] == "." or i == len(texts) - 1):
            # A sentence is ending, decode it and clear buffer.
            sentence = " ".join(buf)
            buf.clear()

            # Check sentence regex.
            if (re.match(SENTENCE, sentence) is None):
                error(
                    "At comment line {:d}, wrong senetence regex.\n" \
                    "\"\"\"\n{:s}\n\"\"\".",
                    start + i, sentence,
                )
                raise RuntimeError
            else:
                pass

            # Append sentence to the block.
            block.append(sentence)
        else:
            # A sentence is not ending, continue.
            pass
    return [block]