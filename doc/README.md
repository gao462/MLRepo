## Table Of Content

* [doc/globe.py](#docglobepy)
  * [Global Code Document Objects](#global-code-document-objects)
    * [Class: ModuleDocument](#class-moduledocument)
    * [Class: GlobalDocument](#class-globaldocument)
* [doc/base.py](#docbasepy)
  * [Document Objects](#document-objects)
    * [Class: Document](#class-document)
    * [Class: FileSysDocument](#class-filesysdocument)
    * [Block: Hierarchy constants.](#block-hierarchy-constants)
    * [Class: CodeDocument](#class-codedocument)
* [doc/main.py](#docmainpy)
  * [Main](#main)
    * [Block: Generate all notes.](#block-generate-all-notes)
* [doc/block.py](#docblockpy)
  * [Block Code Document Objects](#block-code-document-objects)
    * [Class: BlockDocument](#class-blockdocument)
    * [Class: ImportBlockDocument](#class-importblockdocument)
    * [Class: ConstBlockDocument](#class-constblockdocument)
* [doc/code.py](#doccodepy)
  * [Code Objects](#code-objects)
    * [Class: Word](#class-word)
    * [Class: Line](#class-line)
    * [Block: Define essential...](#block-define-essential)
    * [Block: Define single wor...](#block-define-single-wor)
    * [Block: Overwrite compose...](#block-overwrite-compose)
    * [Block: Define not-word w...](#block-define-not-word-w)
    * [Block: Define sentence w...](#block-define-sentence-w)
    * [Block: Define sentence r...](#block-define-sentence-r)
    * [Class: Code](#class-code)
    * [Function: line_rule_length](#function-line_rule_length)
    * [Function: line_rule_char](#function-line_rule_char)
    * [Function: line_rule_break](#function-line_rule_break)
    * [Function: recover](#function-recover)
    * [Function: paragraphize](#function-paragraphize)
    * [Function: mathize](#function-mathize)
    * [Function: codize](#function-codize)
    * [Function: textize](#function-textize)
* [doc/series.py](#docseriespy)
  * [Series Code Document Objects](#series-code-document-objects)
    * [Class: SeriesDocument](#class-seriesdocument)
  * [Class Code Document Objects](#class-code-document-objects)
    * [Class: ClassDocument](#class-classdocument)
  * [Function Code Document Objects](#function-code-document-objects)
    * [Class: FunctionDocument](#class-functiondocument)
  * [Operation Block Code Document Objects](#operation-block-code-document-objects)
    * [Class: OPBlockDocument](#class-opblockdocument)
* [doc/func.py](#docfuncpy)
  * [Function Code Document Objects](#function-code-document-objects)
    * [Class: TypeHintDocument](#class-typehintdocument)
    * [Class: ArgumentDocument](#class-argumentdocument)
* [doc/statement.py](#docstatementpy)
  * [Statement Code Document Objects](#statement-code-document-objects)
    * [Class: CommentDocument](#class-commentdocument)
    * [Class: ImportDocument](#class-importdocument)
    * [Class: IntroDocument](#class-introdocument)
    * [Class: DescriptionDocument](#class-descriptiondocument)
    * [Class: ClassDescDocument](#class-classdescdocument)
    * [Class: FuncDescDocument](#class-funcdescdocument)
* [doc/filesys.py](#docfilesyspy)
  * [File System Document Objects](#file-system-document-objects)
    * [Class: DirectoryDocument](#class-directorydocument)
    * [Class: FileDocument](#class-filedocument)
    * [Function: toc](#function-toc)
    * [Function: github_header](#function-github_header)

---

## doc/globe.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.block`, `doc.statement`, `doc.series`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Dict, Tuple
  >
  > # Import dependencies.
  > import sys
  > import os
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code
  > import doc.base
  > import doc.block
  > import doc.statement
  > import doc.series
  > ```

### Global Code Document Objects

Code document on global level. It contains module import document which traces all imported modules and identifiers and broadcasts them to deeper code documents.

#### Class: ModuleDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/globe.py#L43)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for module imports.

#### Class: GlobalDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/globe.py#L266)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for global level codes.

---

## doc/base.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `pytorch.logging`, `doc.code`, `doc.filesys`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Union
  >
  > # Import dependencies.
  > import sys
  > import os
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code
  > import doc.filesys
  > ```

### Document Objects

Prototype of document. It also includes prototype for file system document and real code document.

#### Class: Document

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L39)

- Super: object

Document prototype.

#### Class: FileSysDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L83)

- Super: [Document](#class-document)

Document for file system prototype.

#### Block: Hierarchy constants.

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L116)
> ```python
> # Hierarchy constants.
> GLOBAL = 0
> CLASS = 1
> FUNCTION = 2
> BLOCK = 3
> BRANCH = 4
> ```

[[TOC]](#table-of-content)

#### Class: CodeDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L124)

- Super: [Document](#class-document)

Document for code prototype.

---

## doc/main.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `pytorch.logging`, `doc.filesys`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  >
  > # Import dependencies.
  > import sys
  > import os
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.filesys import DirectoryDocument
  > ```

### Main

Main branch starts from here.

#### Block: Generate all notes.

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L36)
> ```python
> # Generate all notes.
> doc = DirectoryDocument(os.path.abspath("."), rootdoc=None)
> doc.parse()
> ```

[[TOC]](#table-of-content)

---

## doc/block.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.statement`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Dict, Union
  >
  > # Import dependencies.
  > import sys
  > import os
  > import token
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code, Line, UNIT
  > import doc.base
  > import doc.statement
  > ```

### Block Code Document Objects

Code document on block level. There are several kinds of block documents, but they all share the same workflow.

A block often start with several comments lines, except that in a branch with only one block, it may have no comments.

#### Class: BlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/block.py#L45)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a block of code prototype.

#### Class: ImportBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/block.py#L138)

- Super: [BlockDocument](#class-blockdocument)

Document for a block of import code.

#### Class: ConstBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/block.py#L288)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a block of constant code.

---

## doc/code.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `tokenize`, `token`, `re`, `pytorch.logging`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import Union, List
  >
  > # Import dependencies.
  > import sys
  > import os
  > import tokenize
  > import token
  > import re
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > ```

### Code Objects

Tokenized code for any arbitrary file is defined based on Python token library. Each tokenized code word is automatically attached with its indent level for later styled document check.

Style related constants and utility functions are also defined.

#### Class: Word

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L44)

- Super: object

Token word.

#### Class: Line

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L126)

- Super: object

Line of tokens.

#### Block: Define essential...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L348)
> ```python
> # Define essential constants.
> UNIT = 4
> MAX = 79
> ```

[[TOC]](#table-of-content)

#### Block: Define single wor...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L353)
> ```python
> # Define single word regex.
> NUMBER = r"[1-9][0-9]*"
> INITIAL = r"([A-Z][A-Za-z]*|{:s})".format(NUMBER)
> INSIDE = r"([A-Za-z]+|{:s})".format(NUMBER)
> ```

[[TOC]](#table-of-content)

#### Block: Overwrite compose...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L359)
> ```python
> # Overwrite composed word regex.
> INITIAL = r"({:s}(-{:s})*)".format(INITIAL, INSIDE)
> INSIDE = r"({:s}(-{:s})*)".format(INSIDE, INSIDE)
> ```

[[TOC]](#table-of-content)

#### Block: Define not-word w...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L364)
> ```python
> # Define not-word word regex.
> MATH = r"\$([^\n\\\$]|\\[^\n])+\$"
> CODE = r"`([^\n\\`]|\\[^\n])+`"
> STRING = r"\"([^\n\\\"]|\\[^\n])+\""
> ```

[[TOC]](#table-of-content)

#### Block: Define sentence w...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L370)
> ```python
> # Define sentence word regex.
> FIRST = r"({:s}|{:s}|{:s}|{:s})".format(INITIAL, MATH, CODE, STRING)
> LATER = r"({:s}|{:s}|{:s}|{:s})".format(INSIDE, MATH, CODE, STRING)
> BREAK = r"( |, )"
> ```

[[TOC]](#table-of-content)

#### Block: Define sentence r...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L376)
> ```python
> # Define sentence regex.
> PARANTHESE = r"\({:s}({:s}{:s})*\)".format(LATER, BREAK, LATER)
> SENTENCE = r"^{:s}({:s}{:s}({:s}{:s})?)*.$".format(
>     FIRST, BREAK, LATER, BREAK, PARANTHESE,
> )
> ```

[[TOC]](#table-of-content)

#### Class: Code

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L383)

- Super: object

Tokenized code with indent of a file.

#### Function: line_rule_length

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L953)

Check length rule over a text line.

> **Arguments**

> **Returns**

> ```python
> # Text length is limited.
> if (len(text) > MAX):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " too long (>{:d}).",
>         path, "line {:d}".format(index),
>         MAX,
>     )
>     raise RuntimeError
> else:
>     pass
> ```

[[TOC]](#table-of-content)

#### Function: line_rule_char

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L987)

Check character rule over a text line.

> **Arguments**

> **Returns**

> ```python
> # Some charaters are rejected.
> if (chr(39) in text):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " invalid char \"{:s}\".",
>         path, "line {:d}".format(index),
>         chr(39),
>     )
>     raise RuntimeError
> else:
>     pass
> ```

[[TOC]](#table-of-content)

#### Function: line_rule_break

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1021)

Check line break rule over a text line.

> **Arguments**

> **Returns**

> ```python
> # Line break is rejected except for strings.
> if (text[-2:] == " \\" and text[-3] != "\""):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " line break is disabled.",
>         path, "line {:s}".format(index),
>     )
>     raise RuntimeError
> else:
>     pass
> ```

[[TOC]](#table-of-content)

#### Function: recover

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1054)

Recover code from given memory of tokens.

> **Arguments**

> **Returns**

> ```python
> # Generate directly
> texts = [" " * level * UNIT]
> for word in memory:
>     texts.append(word.text)
> return "".join(texts).split("\n")
> ```

[[TOC]](#table-of-content)

#### Function: paragraphize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1082)

Transfer a list of texts into paragraphs.

> **Arguments**

> **Returns**

> ```python
> # Empty is a special case.
> if (len(texts) == 0):
>     return []
> else:
>     pass
>
> # Attach an additional blank line as replace of EOP.
> buf = texts + [""]
>
> # Break texts by single blank line.
> ptr = 0
> paragraphs = []
> while (ptr < len(buf)):
>     # Reject empty paragraph.
>     if (len(buf[ptr]) == 0):
>         error(
>             "At comment line {:d}, empty paragraph is rejected.",
>             ptr + 1,
>         )
>         raise RuntimeError
>     else:
>         pass
>
>     # Take lines for decoding until a blank line.
>     start = ptr
>     decoding = []
>     while (len(buf[ptr]) > 0):
>         decoding.append(buf[ptr])
>         ptr += 1
>
>     # Decode according to different flags.
>     if (decoding[0] == "$$"):
>         paragraphs.extend(mathize(decoding, start=start + 1))
>     elif (decoding[0][0:3] == "```"):
>         paragraphs.extend(codize(decoding, start=start + 1))
>     else:
>         paragraphs.extend(textize(decoding, start=start + 1))
>
>     # Go over the blank line to move to next.
>     ptr += 1
> return paragraphs
> ```

[[TOC]](#table-of-content)

#### Function: mathize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1144)

Transfer a list of texts into math block.

> **Arguments**

> **Returns**

> ```python
> # Block must end properly.
> if (texts[-1] != "$$"):
>     error(
>         "At comment line {:d}, multiple-line math starts from" \
>         " line {:d} but ends nowhere.",
>         start + len(texts) - 1, start,
>     )
>     raise RuntimeError
> else:
>     pass
>
> # Math block requires no decoding.
> return [[itr] for itr in texts]
> ```

[[TOC]](#table-of-content)

#### Function: codize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1180)

Transfer a list of texts into code block.

> **Arguments**

> **Returns**

> ```python
> # Block must end properly.
> if (texts[-1] != "```"):
>     error(
>         "At comment line {:d}, multiple-line code starts from" \
>         " line {:d} but ends nowhere.",
>         start + len(texts) - 1, start,
>     )
>     raise RuntimeError
> else:
>     pass
>
> # Math block requires no decoding.
> return [[itr] for itr in texts]
> ```

[[TOC]](#table-of-content)

#### Function: textize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1216)

Transfer a list of texts into text block.

> **Arguments**

> **Returns**

> ```python
> # Allocate buffer.
> block = []
> buf = []
>
> # Decode all text in order.
> for i, itr in enumerate(texts):
>     buf.append(itr)
>     if (itr[-1] == "." or i == len(texts) - 1):
>         # A sentence is ending, decode it and clear buffer.
>         sentence = " ".join(buf)
>         buf.clear()
>
>         # Check sentence regex.
>         if (re.match(SENTENCE, sentence) is None):
>             error(
>                 "At comment line {:d}, wrong senetence regex.\n" \
>                 "\"\"\"\n{:s}\n\"\"\".",
>                 start + i, sentence,
>             )
>             raise RuntimeError
>         else:
>             pass
>
>         # Append sentence to the block.
>         block.append(sentence)
>     else:
>         # A sentence is not ending, continue.
>         pass
> return [block]
> ```

[[TOC]](#table-of-content)

---

## doc/series.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.statement`, `doc.filesys`, `doc.func`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Union
  >
  > # Import dependencies.
  > import sys
  > import os
  > import token
  > import re
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code, MAX, UNIT
  > import doc.base
  > import doc.statement
  > import doc.filesys
  > import doc.func
  > ```

### Series Code Document Objects

Code document for a series of codes. It works as a midterm contatenation for class definitions, function definitions and code blocks with the same indent level, thus it contains nothing in memory except a list of documents attached to it.

It will mutually import with ClassDocument, FunctionDocument, OPBlockDocument. Thus, they four are aggregated together in this file.

#### Class: SeriesDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L50)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a series of code.

### Class Code Document Objects

Code document for a definition of class. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: ClassDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L218)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a definition of class.

### Function Code Document Objects

Code document for a definition of function. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: FunctionDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L407)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a definition of function.

### Operation Block Code Document Objects

Code document for a block of operation code. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: OPBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L602)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a block of operation code.

---

## doc/func.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.statement`, `doc.filesys`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Tuple, Union
  >
  > # Import dependencies.
  > import sys
  > import os
  > import token
  > import re
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code, MAX
  > import doc.base
  > import doc.statement
  > import doc.filesys
  > ```

### Function Code Document Objects

Code document for function related codes. This only contains elements of a function, for example, arguments, returns. The function document itself is defined in series module.

#### Class: TypeHintDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/func.py#L44)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for type hint definition.

#### Class: ArgumentDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/func.py#L174)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for argument definition.

---

## doc/statement.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.filesys`, `doc.func`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import Union, List, Dict
  >
  > # Import dependencies.
  > import sys
  > import os
  > import token
  > import re
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code, Line, paragraphize, UNIT, MAX, FIRST
  > from doc.code import paragraphize
  > import doc.base
  > import doc.filesys
  > import doc.func
  > ```

### Statement Code Document Objects

Code document for a line of statement. Different statement types have their own workflow, but they all save line of tokens belong to them for potential styled code recovery.

#### Class: CommentDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L45)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a line of comment statement.

#### Class: ImportDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L173)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a line of import statement.

#### Class: IntroDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L486)

- Super: [CommentDocument](#class-commentdocument)

Document for an introduction statement.

#### Class: DescriptionDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L582)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

Document for a description statement prototype.

#### Class: ClassDescDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L700)

- Super: [DescriptionDocument](#class-descriptiondocument)

Document for a description of class statement.

#### Class: FuncDescDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L736)

- Super: [DescriptionDocument](#class-descriptiondocument)

Document for a description of function statement.

---

## doc/filesys.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.globe`, `doc.series`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Tuple, Union, Dict
  >
  > # Import dependencies.
  > import sys
  > import os
  > import re
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  > from pytorch.logging import debug, info1, info2, focus, warning, error
  >
  > # Import dependencies.
  > from doc.code import Code
  > import doc.base
  > import doc.globe
  > import doc.series
  > ```

### File System Document Objects

Documentize tokenized code files, and check style rules in the meanwhile.

In this level, a document directory controller will traverse every folder in MLRepo. At each folder, controller will identify all python files, and generate their markdown notes by their file controllers. Generated notes is then merged into README file inside current directory.

In the README file, super links to exact Github code position are also created for global or global-class level classes, functions, and blocks. Styled code snaps for those parts are also attached with them.

For function or class inside a function, local-class or branch-of-block, it will be compressed into its name definition. Arguments or codes of it will be replaced by "..." which can be used as python ellipsis for code.

After the generation, a strict description matching is applied on classes with inheritance relationships so that inherited classes only extends function argument names and description details of inheriting classes. This also autofills the exact Github code positions for module imports and classes.

#### Class: DirectoryDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L62)

- Super: [doc.base.FileSysDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-filesysdocument)

Document for a directory.

#### Class: FileDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L258)

- Super: [doc.base.FileSysDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-filesysdocument)

Document for a file.

#### Function: toc

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L399)

Generate table of content from given notes.

> **Arguments**

> **Returns**

> ```python
> # Registrate all headers by Github header reference behavior.
> headers: List[Tuple[int, str, str]] = []
> for itr in notes:
>     # Header level matters.
>     level = 0
>     while (level < len(itr) and itr[level] == "#"):
>         level += 1
>     if (level == 0):
>         continue
>     else:
>         pass
>
>     # Get header text.
>     text = itr[level + 1:]
>     refer = text
>
>     # Github reference ignores colorful ASCII even in console.
>     refer = re.sub(r"\033\[[^m]+m", "", refer)
>     headers.append((level, text, github_header(refer)))
>
> # Generate TOC.
> toc = ["## Table Of Content", ""]
> for level, text, refer in headers:
>     indent = "  " * (level - 2)
>     link = "{:s}* [{:s}](#{:s})".format(indent, text, refer)
>     toc.append(link)
> return toc
> ```

[[TOC]](#table-of-content)

#### Function: github_header

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L445)

Get a Github header reference.

> **Arguments**

> **Returns**

> ```python
> # Github reference ignores "." or "/".
> refer = text
> refer = re.sub(r"(\.|/)", "", refer).strip()
>
> # Github reference should be lower case concatenated by "-".
> refer = re.sub(r"[^\w]+", "-", refer.lower())
> return refer
> ```

[[TOC]](#table-of-content)