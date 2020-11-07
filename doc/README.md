
---

## doc/main.py

- Dependent on: `typing`, `sys`, `os`, `tokenize`, `token`, `re`, `logging`, `pytorch.logging`.

### Code Objects

Tokenized code for any arbitrary file is defined based on Python token library. Each tokenized code word is automatically attached with its indent level for later styled document check.

A scanner over tokenized code is also defined for the ease of check. Essential and shared utility functions related to code words are integrated.

- Class [**Word**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L44)(*object*)

  Token word.

  - Function [**set**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L48)(*self, val, text, row, level, column*)

    Set word attributes.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **val**: *int*
    >   Token integer.
    > - **text**: *str*
    >   Token text content.
    > - **row**: *int*
    >   Token row index.
    > - **level**: *Union[int, None]*
    >   Token indent level.
    > - **column**: *int*
    >   Token column index.

    > **Returns**
    > No returns.

  - Function [**position**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L82)(*self*)

    Position string.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - **self**

    > **Returns**
    > - **msg**: *str*
    >   Position string.

- Class [**Code**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L101)(*object*)

  Tokenized code with indent of a file.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L105)(*self*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**__len__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L138)(*self*)

    Length.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **length**: *int*
    >   Length of remaining memory.

  - Function [**load_file**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L155)(*self, path*)

    Load code tokens from given file.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **path**: *str*
    >   File path.

    > **Returns**
    > No returns.

  - Function [**load_texts**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L182)(*self*)

    Load text lines from given file.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**load_tokens**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L209)(*self*)

    Load tokens from given file.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**rule_texts**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L232)(*self*)

    Check rules over text lines.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**line_rule_length**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L250)(*self, index, line*)

    Check length rule over a text line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **index**: *int*
    >   Line index.
    > - **line**: *str*
    >   Line content.

    > **Returns**
    > No returns.

  - Function [**line_rule_char**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L279)(*self, index, line*)

    Check character rule over a text line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **index**: *int*
    >   Line index.
    > - **line**: *str*
    >   Line content.

    > **Returns**
    > No returns.

  - Function [**line_rule_break**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L308)(*self, index, line*)

    Check line break rule over a text line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **index**: *int*
    >   Line index.
    > - **line**: *str*
    >   Line content.

    > **Returns**
    > No returns.

  - Function [**review**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L336)(*self*)

    Review text lines and tokens as lines of tokens.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**reset**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L406)(*self*)

    Reset scanning status.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**next**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L421)(*self*)

    Move to next scanning status.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**top**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L436)(*self*)

    Get the first focusing word.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - **self**

    > **Returns**
    > - **word**: *Word*
    >   Top word.

  - Function [**preview**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L454)(*self, shift*)

    Get the preview of word shifted from first focusing word.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **shift**: *int*
    >   Shifting offset.

    > **Returns**
    > - **word**: *Word*
    >   Shifted word.

  - Function [**fit**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L473)(*self, level, target*)

    Check if scanning token fits the target.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **level**: *int*
    >   Targe token indent level.
    > - **target**: *Union[int, str, None]*
    >   Target token ID or text. If None, it means anything.

    > **Returns**
    > - **flag**: *bool*
    >   If True, target is satisfied by current token.

  - Function [**eof**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L500)(*self*)

    Get EOF signal.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **flag**: *bool*
    >   EOF signal.

  - Function [**paragraphs**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L517)(*self, contents*)

    Break given content into list of paragraphs.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **contents**: *List[str]*
    >   Given contents.

    > **Returns**
    > - **texts**: *List[List[str]]*
    >   Text of contents as list of paragraphs. Each paragraph is a list of regular sentence.

### Document Objects

Documentize tokenized code files, and check style rules in the meanwhile.

- Class [**Document**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L600)(*object*)

  Document prototype.

  - Block

    Define constants.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L607)(*self*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L623)(*self, *args, **kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - ***args**
    > - ****kargs**

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L641)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**DirectoryDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L660)(*Document*)

  Document for a directory.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L664)(*self*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L679)(*self, root*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **root**: *str*
    >   Root of the project.

    > **Returns**
    > No returns.

- Class [**FileDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L741)(*Document*)

  Document for a file.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L745)(*self*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L760)(*self, path*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **path**: *str*
    >   Path of documentizing file.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L786)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Block

  Hierarchy constants.

- Class [**CodeDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L817)(*Document*)

  Document prototype for code.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L821)(*self, path, level, hierarchy*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **path**: *str*
    >   Path of its file document.
    > - **level**: *int*
    >   Indent level.
    > - **hierarchy**: *int*
    >   Hierarchy order.

    > **Returns**
    > No returns.

  - Function [**expect**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L844)(*self, *args*)

    Expect next several code words to be the arguments.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - ***args**

    > **Returns**
    > No returns.

### Global Code Document Objects

Code document on global level.

- Class [**ModuleDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L908)(*CodeDocument*)

  Document for module imports.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L912)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**append**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1006)(*self, module, identifier*)

    Append an import opertation.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **module**: *str*
    >   Module name.
    > - **identifier**: *Union[str, None]*
    >   Identifier name.

    > **Returns**
    > No returns.

  - Function [**append_until**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1044)(*self*)

    Append import operations until a blank line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1065)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**GlobalDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1087)(*CodeDocument*)

  Document for global level codes.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1091)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1117)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**IntroductionDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1144)(*CodeDocument*)

  Document for introduction codes.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1148)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1248)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**SeriesDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1272)(*CodeDocument*)

  Document for a series of codes (any hierarchy).

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1276)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1370)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

### Class Code Document Objects

Code document for class definition.

- Class [**ClassDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1417)(*CodeDocument*)

  Document for a class definition.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1421)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1498)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

### Function Code Document Objects

Code document for function definition.

- Class [**FunctionDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1550)(*CodeDocument*)

  Document for a function definition.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1554)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**validate**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1721)(*self*)

    Validate description with arguments and returns.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1809)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

### Block Code Document Objects

Code document on block level. This document will deal with a series of consecutive code lines (without any blank lines or dedent) starting with or without comment descriptions.

- Class [**BlockDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1916)(*CodeDocument*)

  Document for a block of code lines.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1920)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

### Line Code Document Objects

Code document on line level. These documents will memorize essential information inside a single code line. They also deal with other cases, e.g., arguments, return type hints and so on.

A single code line may corresponds to multiple text lines, e.g., multiple lines between a pair of parantheses. Slash line break for too long text lines is forbidden except for strings.

- Class [**ImportDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2044)(*CodeDocument*)

  Document for an import code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2048)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**parse_name**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2078)(*self*)

    Parse name.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

  - Function [**parse_identifiers**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2101)(*self*)

    Parse identifiers.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > No returns.

- Class [**ConstDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2124)(*CodeDocument*)

  Document for a constant code line.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2128)(*self, *args, constants*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - ***args**
    > - **constants**: *List[Union[int, str]]*
    >   Constant words in the code line.

    > **Returns**
    > No returns.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2149)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

- Class [**DocStringDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2168)(*CodeDocument*)

  Document for a document string for class/function.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2172)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

- Class [**ClassDocDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2243)(*DocStringDocument*)

  Document for a document string for class.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2247)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

- Class [**FunctionDocDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2268)(*DocStringDocument*)

  Document for a document string for function.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2272)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**parse_args**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2334)(*self, part*)

    Parse argument description.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **part**: *List[str]*
    >   Text content of argument description.

    > **Returns**
    > - **desc**: *List[Tuple[str, List[List[str]]]]*
    >   A list of argument names and their description paragraphs.

  - Function [**parse_returns**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2397)(*self, part*)

    Parse return description.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **part**: *List[str]*
    >   Text content of return description.

    > **Returns**
    > - **desc**: *List[Tuple[str, List[List[str]]]]*
    >   A list of return names and their description paragraphs.

- Class [**DecorateDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2453)(*CodeDocument*)

  Document for a function decorator line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2457)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

- Class [**ArgumentDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2492)(*CodeDocument*)

  Document for function arguments.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2496)(*self, *args, multiple*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - ***args**
    > - **multiple**: *bool*
    >   If True, the arguments are cross-line.

    > **Returns**
    > No returns.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2517)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

- Class [**TypeHintDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2594)(*CodeDocument*)

  Document for a type hint.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2598)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**full_name**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2657)(*self*)

    Get full name including all children for the type hint.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - **self**

    > **Returns**
    > - **msg**: *str*
    >   Full name.

- Class [**ReturnDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2680)(*TypeHintDocument*)

  Document for function arguments.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2684)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**multiple**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2716)(*self*)

    Check if this is a multiple-return document.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - **self**

    > **Returns**
    > - **flag**: *bool*
    >   If True, this is a multiple-return document.

- Class [**OperateDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2735)(*CodeDocument*)

  Document for an operation code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2739)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

- Class [**ConditionDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2782)(*CodeDocument*)

  Document for a conditional code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2786)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2822)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**IfDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2851)(*ConditionDocument*)

  Document for an if-statement code line.

  - Block

    Define constants.

- Class [**ElifDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2859)(*ConditionDocument*)

  Document for an elif-statement code line.

  - Block

    Define constants.

- Class [**ElseDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2867)(*CodeDocument*)

  Document for an else-statement code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2871)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2897)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**WhileDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2918)(*ConditionDocument*)

  Document for a while-statement code line.

  - Block

    Define constants.

- Class [**ForDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2926)(*CodeDocument*)

  Document for a for-statement code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2930)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2983)(*self*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**

    > **Returns**
    > - **notes**: *List[str]*
    >   Markdown notes.

- Class [**ParantheseDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3008)(*CodeDocument*)

  Document for a cross-line paranthese code line.

  - Block

    Define consntants.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3020)(*self, *args, left*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - ***args**
    > - **left**: *str*
    >   Left paranthese.

    > **Returns**
    > No returns.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3042)(*self, code*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - **self**
    > - **code**: *Code*
    >   Tokenized code.

    > **Returns**
    > No returns.

### Main Branch

Main branch starts here.

- Function [**script_logger**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3150)()

  Create script logger.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > No arguments.

  > **Returns**
  > - **logger**: *logging.Logger*
  >   Default logger.

- Function [**main**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3183)(*root*)

  Main branch.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - **root**: *str*
  >   Root.

  > **Returns**
  > No returns.

- Block

  Main entrance.