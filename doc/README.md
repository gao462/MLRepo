
---

## doc/main.py

- Dependent on: `typing`, `sys`, `os`, `tokenize`, `token`, `re`, `logging`, `pytorch.logging`.

### Code Objects

Tokenized code for any arbitrary file is defined based on Python token library. Each tokenized code word is automatically attached with its indent level for later styled document check.

A scanner over tokenized code is also defined for the ease of check. Essential and shared utility functions related to code words are integrated.

- Class [**Word**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L44)(*object*)

  Token word.

  - Function [**set**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L48)(*self, \*args, val, text, row, level, column, \*\*kargs*)

    Set word attributes.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *val*: `int`
    >   Token integer.
    > - *text*: `str`
    >   Token text content.
    > - *row*: `int`
    >   Token row index.
    > - *level*: `Union[int, None]`
    >   Token indent level.
    > - *column*: `int`
    >   Token column index.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**position**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L84)(*self, \*args, \*\*kargs*)

    Position string.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *msg*: `str`
    >   Position string.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**Code**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L105)(*object*)

  Tokenized code with indent of a file.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L109)(*self, \*args, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**__len__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L144)(*self, \*args, \*\*kargs*)

    Length.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *length*: `int`
    >   Length of remaining memory.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**load_file**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L163)(*self, path, \*args, \*\*kargs*)

    Load code tokens from given file.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *path*: `str`
    >   File path.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**load_texts**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L192)(*self, \*args, \*\*kargs*)

    Load text lines from given file.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**load_tokens**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L221)(*self, \*args, \*\*kargs*)

    Load tokens from given file.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**rule_texts**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L246)(*self, \*args, \*\*kargs*)

    Check rules over text lines.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**line_rule_length**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L266)(*self, \*args, index, line, \*\*kargs*)

    Check length rule over a text line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *index*: `int`
    >   Line index.
    > - *line*: `str`
    >   Line content.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**line_rule_char**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L297)(*self, \*args, index, line, \*\*kargs*)

    Check character rule over a text line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *index*: `int`
    >   Line index.
    > - *line*: `str`
    >   Line content.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**line_rule_break**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L328)(*self, \*args, index, line, \*\*kargs*)

    Check line break rule over a text line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *index*: `int`
    >   Line index.
    > - *line*: `str`
    >   Line content.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**review**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L358)(*self, \*args, \*\*kargs*)

    Review text lines and tokens as lines of tokens.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**reset**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L436)(*self, \*args, \*\*kargs*)

    Reset scanning status.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**next**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L453)(*self, \*args, \*\*kargs*)

    Move to next scanning status.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**top**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L470)(*self, \*args, \*\*kargs*)

    Get the first focusing word.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *word*: `Word`
    >   Top word.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**preview**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L490)(*self, shift, \*args, \*\*kargs*)

    Get the preview of word shifted from first focusing word.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *shift*: `int`
    >   Shifting offset.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *word*: `Word`
    >   Shifted word.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**fit**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L511)(*self, level, target, \*args, \*\*kargs*)

    Check if scanning token fits the target.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *level*: `int`
    >   Targe token indent level.
    > - *target*: `Union[int, str, None]`
    >   Target token ID or text. If None, it means anything.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *flag*: `bool`
    >   If True, target is satisfied by current token.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**eof**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L542)(*self, \*args, \*\*kargs*)

    Get EOF signal.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *flag*: `bool`
    >   EOF signal.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**paragraphs**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L561)(*self, contents, \*args, \*\*kargs*)

    Break given content into list of paragraphs.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *contents*: `List[str]`
    >   Given contents.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *texts*: `List[List[str]]`
    >   Text of contents as list of paragraphs. Each paragraph is a list of regular sentence.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

### Document Objects

Documentize tokenized code files, and check style rules in the meanwhile.

In this level, a document directory controller will traverse every folder in MLRepo. At each folder, controller will identify all python files, and generate their markdown notes by their file controllers. Generated notes is then merged into README file inside current directory.

In the README file, super links to exact Github code position are also created for global or in-global-class level classes, functions, and blocks. Styled code snaps for those parts are also attached with them.

After the generation, a strict description matching is applied on classes with inheritance relationships so that inherited classes only extends function argument names and description details of inheriting classes.

- Class [**Document**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L661)(*object*)

  Document prototype.

  - [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L665)

    Define constants.
    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L668)(*self, \*args, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L686)(*self, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L704)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**DirectoryDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L725)(*Document*)

  Document for a directory.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L729)(*self, \*args, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L746)(*self, root, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *root*: `str`
    >   Root of the project.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**fetch**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L810)(*self, dirdoc, \*args, \*\*kargs*)

    Fetch class inheritance from given directory document.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *dirdoc*: `Document`
    >   Directory document.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *mapping*: `Dict[str, str]`
    >   Inheritance mapping.
    > - *loaded*: `Dict[str, Dict[str, Document]]`
    >   Loaded class documents.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**match**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L885)(*self, \*args, \*\*kargs*)

    Match class inheritance.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**FileDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L978)(*Document*)

  Document for a file.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L982)(*self, \*args, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L999)(*self, path, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *path*: `str`
    >   Path of documentizing file.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1027)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1052)

  Hierarchy constants.
  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Class [**CodeDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1060)(*Document*)

  Document prototype for code.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1064)(*self, path, level, hierarchy, \*args, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *path*: `str`
    >   Path of its file document.
    > - *level*: `int`
    >   Indent level.
    > - *hierarchy*: `int`
    >   Hierarchy order.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**expect**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1091)(*self, \*args, \*\*kargs*)

    Expect next several code words to be the arguments.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

### Global Code Document Objects

Code document on global level.

- Class [**ModuleDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1156)(*CodeDocument*)

  Document for module imports.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1160)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**append**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1256)(*self, module, identifier, \*args, \*\*kargs*)

    Append an import opertation.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *module*: `str`
    >   Module name.
    > - *identifier*: `Union[str, None]`
    >   Identifier name.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**append_until**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1298)(*self, \*args, \*\*kargs*)

    Append import operations until a blank line.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1321)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**GlobalDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1345)(*CodeDocument*)

  Document for global level codes.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1349)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1377)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**IntroductionDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1406)(*CodeDocument*)

  Document for introduction codes.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1410)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1512)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**SeriesDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1538)(*CodeDocument*)

  Document for a series of codes (any hierarchy).

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1542)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1638)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

### Class Code Document Objects

Code document for class definition.

- Class [**ClassDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1695)(*CodeDocument*)

  Document for a class definition.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1699)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1778)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

### Function Code Document Objects

Code document for function definition.

- Class [**FunctionDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1832)(*CodeDocument*)

  Document for a function definition.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1836)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**validate**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2005)(*self, \*args, \*\*kargs*)

    Validate description with arguments and returns.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2095)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

### Block Code Document Objects

Code document on block level. This document will deal with a series of consecutive code lines (without any blank lines or dedent) starting with or without comment descriptions.

- Class [**BlockDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2225)(*CodeDocument*)

  Document for a block of code lines.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2229)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2338)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

### Line Code Document Objects

Code document on line level. These documents will memorize essential information inside a single code line. They also deal with other cases, e.g., arguments, return type hints and so on.

A single code line may corresponds to multiple text lines, e.g., multiple lines between a pair of parantheses. Slash line break for too long text lines is forbidden except for strings.

- Class [**ImportDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2374)(*CodeDocument*)

  Document for an import code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2378)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse_name**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2410)(*self, \*args, \*\*kargs*)

    Parse name.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse_identifiers**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2435)(*self, \*args, \*\*kargs*)

    Parse identifiers.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ConstDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2460)(*CodeDocument*)

  Document for a constant code line.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2464)(*self, \*args, constants, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *constants*: `List[Union[int, str]]`
    >   Constant words in the code line.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2488)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**DocStringDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2509)(*CodeDocument*)

  Document for a document string for class/function.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2513)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ClassDocDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2586)(*DocStringDocument*)

  Document for a document string for class.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2590)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**FunctionDocDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2613)(*DocStringDocument*)

  Document for a document string for function.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2617)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse_args**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2681)(*self, part, \*args, \*\*kargs*)

    Parse argument description.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *part*: `List[str]`
    >   Text content of argument description.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *desc*: `List[Tuple[str, List[List[str]]]]`
    >   A list of argument names and their description paragraphs.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse_returns**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2748)(*self, part, \*args, \*\*kargs*)

    Parse return description.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *part*: `List[str]`
    >   Text content of return description.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *desc*: `List[Tuple[str, List[List[str]]]]`
    >   A list of return names and their description paragraphs.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**DecorateDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2806)(*CodeDocument*)

  Document for a function decorator line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2810)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ArgumentDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2847)(*CodeDocument*)

  Document for function arguments.

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2851)(*self, \*args, multiple, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *multiple*: `bool`
    >   If True, the arguments are cross-line.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2873)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**TypeHintDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2972)(*CodeDocument*)

  Document for a type hint.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2976)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**full_name**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3041)(*self, \*args, \*\*kargs*)

    Get full name including all children for the type hint.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *msg*: `str`
    >   Full name.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ReturnDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3066)(*TypeHintDocument*)

  Document for function arguments.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3070)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**multiple**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3104)(*self, \*args, \*\*kargs*)

    Check if this is a multiple-return document.

    > **Decorators**
    > 1. property

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *flag*: `bool`
    >   If True, this is a multiple-return document.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**OperateDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3125)(*CodeDocument*)

  Document for an operation code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3129)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ConditionDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3174)(*CodeDocument*)

  Document for a conditional code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3178)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3216)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**IfDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3247)(*ConditionDocument*)

  Document for an if-statement code line.

  - [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3251)

    Define constants.
    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ElifDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3255)(*ConditionDocument*)

  Document for an elif-statement code line.

  - [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3259)

    Define constants.
    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ElseDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3263)(*CodeDocument*)

  Document for an else-statement code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3267)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3295)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**WhileDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3318)(*ConditionDocument*)

  Document for a while-statement code line.

  - [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3322)

    Define constants.
    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ForDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3326)(*CodeDocument*)

  Document for a for-statement code line.

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3330)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**markdown**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3385)(*self, \*args, \*\*kargs*)

    Generate Markdown.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > - *notes*: `List[str]`
    >   Markdown notes.

    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

- Class [**ParantheseDocument**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3412)(*CodeDocument*)

  Document for a cross-line paranthese code line.

  - [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3416)

    Define consntants.
    ```python
    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**__init__**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3424)(*self, \*args, left, \*\*kargs*)

    Initialize.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *\*args*
    > - *left*: `str`
    >   Left paranthese.
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

  - Function [**parse**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3447)(*self, code, \*args, \*\*kargs*)

    Parse content.

    > **Decorators**
    > No decorators.

    > **Arguments**
    > - *self*
    > - *code*: `Code`
    >   Tokenized code.
    > - *\*args*
    > - *\*\*kargs*

    > **Returns**
    > No returns.

    ```python
    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.

    # Code Styled Copy (CSC) is not implemented.
    ```

### Main Branch

Main branch starts here.

- Function [**script_logger**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3564)(*\*args, \*\*kargs*)

  Create script logger.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > - *logger*: `logging.Logger`
  >   Default logger.

  ```python
  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**main**](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3599)(*root, \*args, \*\*kargs*)

  Main branch.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *root*: `str`
  >   Root.
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.
  ```

- [Block](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3623)

  Main entrance.
  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```