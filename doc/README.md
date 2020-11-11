* Table of Content
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
  * [doc/statement.py](#docstatementpy)
    * [Statement Code Document Objects](#statement-code-document-objects)
      * [Class: CommentDocument](#class-commentdocument)
      * [Class: ImportDocument](#class-importdocument)
      * [Class: IntroDocument](#class-introdocument)
      * [Class: DescriptionDocument](#class-descriptiondocument)
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

#### Class: GlobalDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/globe.py#L267)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

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

#### Class: FileSysDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L84)

- Super: [Document](#class-document)

#### Block: Hierarchy constants.

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L117)

#### Class: CodeDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/base.py#L125)

- Super: [Document](#class-document)

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

#### Class: ImportBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/block.py#L136)

- Super: [BlockDocument](#class-blockdocument)

#### Class: ConstBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/block.py#L289)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

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

#### Class: Line

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L126)

- Super: object

#### Block: Define essential...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L348)

#### Block: Define single wor...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L353)

#### Block: Overwrite compose...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L359)

#### Block: Define not-word w...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L364)

#### Block: Define sentence w...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L370)

#### Block: Define sentence r...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L376)

#### Class: Code

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L383)

- Super: object

#### Function: line_rule_length

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L953)

#### Function: recover

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1052)

#### Function: paragraphize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1080)

#### Function: mathize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1132)

#### Function: codize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1168)

#### Function: textize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1204)

---

## doc/series.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.statement`, `doc.filesys`

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
  > from doc.code import Code, MAX
  > import doc.base
  > import doc.statement
  > import doc.filesys
  > ```

### Series Code Document Objects

Code document for a series of codes. It works as a midterm contatenation for class definitions, function definitions and code blocks with the same indent level, thus it contains nothing in memory except a list of documents attached to it.

It will mutually import with ClassDocument, FunctionDocument, OPBlockDocument. Thus, they four are aggregated together in this file.

#### Class: SeriesDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L49)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

### Class Code Document Objects

Code document for a definition of class. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: ClassDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L215)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

### Function Code Document Objects

Code document for a definition of function. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: FunctionDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L401)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

### Operation Block Code Document Objects

Code document for a block of operation code. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: OPBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/series.py#L553)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

---

## doc/statement.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.filesys`

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
  > ```

### Statement Code Document Objects

Code document for a line of statement. Different statement types have their own workflow, but they all save line of tokens belong to them for potential styled code recovery.

#### Class: CommentDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L44)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

#### Class: ImportDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L173)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

#### Class: IntroDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L487)

- Super: [CommentDocument](#class-commentdocument)

#### Class: DescriptionDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L584)

- Super: [doc.base.CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-codedocument)

#### Class: FuncDescDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/statement.py#L707)

- Super: [DescriptionDocument](#class-descriptiondocument)

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

#### Class: FileDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L259)

- Super: [doc.base.FileSysDocument](https://github.com/gao462/MLRepo/tree/main/doc/base#class-filesysdocument)

#### Function: toc

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L401)

#### Function: github_header

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/filesys.py#L447)