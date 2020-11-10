* Table of Content
  * [doc/globe.py](#doc-globepy)
    * [Global Code Document Objects](#global-code-document-objects)
      * [Class: ModuleDocument](#class-moduledocument)
      * [Class: GlobalDocument](#class-globaldocument)
  * [doc/base.py](#doc-basepy)
    * [Document Prototype Objects](#document-prototype-objects)
      * [Class: Document](#class-document)
      * [Block: Hierarchy constants.](#block-hierarchy-constants)
      * [Class: FileSysDocument](#class-filesysdocument)
      * [Class: CodeDocument](#class-codedocument)
  * [doc/main.py](#doc-mainpy)
    * [Main](#main)
      * [Block: Generate all notes.](#block-generate-all-notes)
  * [doc/block.py](#doc-blockpy)
    * [Block Code Document Objects](#block-code-document-objects)
      * [Class: BlockDocument](#class-blockdocument)
      * [Class: ImportBlockDocument](#class-importblockdocument)
      * [Class: ConstBlockDocument](#class-constblockdocument)
  * [doc/code.py](#doc-codepy)
    * [Code Objects](#code-objects)
      * [Class: Word](#class-word)
      * [Class: Line](#class-line)
      * [Block: Define essential ...](#block-define-essential)
      * [Block: Define single wor...](#block-define-single-wor)
      * [Block: Overwrite compose...](#block-overwrite-compose)
      * [Block: Define not-word w...](#block-define-not-word-w)
      * [Block: Define sentence w...](#block-define-sentence-w)
      * [Block: Define sentence r...](#block-define-sentence-r)
      * [Class: Code](#class-code)
      * [Function: line_rule_length](#function-line_rule_length)
      * [Function: recover](#function-recover)
      * [Function: paragraphize](#function-paragraphize)
  * [doc/series.py](#doc-seriespy)
    * [Series Code Document Objects](#series-code-document-objects)
      * [Class: SeriesDocument](#class-seriesdocument)
    * [Class Code Document Objects](#class-code-document-objects)
      * [Class: ClassDocument](#class-classdocument)
    * [Function Code Document Objects](#function-code-document-objects)
      * [Class: FunctionDocument](#class-functiondocument)
    * [Operation Block Code Document Objects](#operation-block-code-document-objects)
      * [Class: OPBlockDocument](#class-opblockdocument)
  * [doc/statement.py](#doc-statementpy)
    * [Statement Code Document Objects](#statement-code-document-objects)
      * [Class: CommentDocument](#class-commentdocument)
      * [Class: ImportDocument](#class-importdocument)
      * [Class: ConstDocument](#class-constdocument)
      * [Class: IntroDocument](#class-introdocument)
  * [doc/filesys.py](#doc-filesyspy)
    * [File System Document Objects](#file-system-document-objects)
      * [Class: DirectoryDocument](#class-directorydocument)
      * [Class: FileDocument](#class-filedocument)
      * [Function: toc](#function-toc)

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
  > from typing import List, Dict
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
  > from doc.base import CodeDocument
  > from doc.block import ImportBlockDocument, ConstBlockDocument
  > from doc.statement import IntroDocument
  > from doc.series import SeriesDocument
  > ```

### Global Code Document Objects

Code document on global level. It contains module import document which traces all imported modules and identifiers and broadcasts them to deeper code documents.

#### Class: ModuleDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

#### Class: GlobalDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

---

## doc/base.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `pytorch.logging`, `doc.code`

  > ```python
  > # Import future.
  > from __future__ import annotations
  >
  > # Import typing.
  > from typing import Any
  > from typing import Tuple as MultiReturn
  > from typing import List, Union, Dict
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
  > ```

### Document Prototype Objects

Document prototypes are defined.

Document is overall prototype, and is used for file system related things. CodeDocument is an inheritance of Document, but it works on tokenized code of an arbitrary file rather than file system.

#### Class: Document

- Super: object

#### Block: Hierarchy constants.

#### Class: FileSysDocument

- Super: [Document](#class-document)

#### Class: CodeDocument

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
  > from doc.code import Code
  > from doc.base import CodeDocument, Document, BRANCH, FileSysDocument
  > from doc.statement import CommentDocument, ImportDocument, ConstDocument
  > ```

### Block Code Document Objects

Code document on block level. There are several kinds of block documents, but they all share the same workflow.

A block often start with several comments lines, except that in a branch with only one block, it may have no comments.

#### Class: BlockDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

#### Class: ImportBlockDocument

- Super: [BlockDocument](#class-blockdocument)

#### Class: ConstBlockDocument

- Super: [BlockDocument](#class-blockdocument)

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

- Super: object

#### Class: Line

- Super: object

#### Block: Define essential ...

#### Block: Define single wor...

#### Block: Overwrite compose...

#### Block: Define not-word w...

#### Block: Define sentence w...

#### Block: Define sentence r...

#### Class: Code

- Super: object

#### Function: line_rule_length

#### Function: recover

#### Function: paragraphize

---

## doc/series.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`, `doc.statement`

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
  > from doc.base import CodeDocument, GLOBAL, CLASS, FUNCTION
  > from doc.statement import CommentDocument
  > ```

### Series Code Document Objects

Code document for a series of codes. It works as a midterm contatenation for class definitions, function definitions and code blocks with the same indent level, thus it contains nothing in memory except a list of documents attached to it.

It will mutually import with ClassDocument, FunctionDocument, OPBlockDocument. Thus, they four are aggregated together in this file.

#### Class: SeriesDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

### Class Code Document Objects

Code document for a definition of class. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: ClassDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

### Function Code Document Objects

Code document for a definition of function. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: FunctionDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

### Operation Block Code Document Objects

Code document for a block of operation code. It can mutually import with SeriesDocument, thus it is put in this file.

#### Class: OPBlockDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

---

## doc/statement.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `token`, `re`, `pytorch.logging`, `doc.code`, `doc.base`

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
  > from doc.base import CodeDocument, Document, BRANCH, FileSysDocument
  > ```

### Statement Code Document Objects

Code document for a line of statement. Different statement types have their own workflow, but they all save line of tokens belong to them for potential styled code recovery.

#### Class: CommentDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

#### Class: ImportDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

#### Class: ConstDocument

- Super: [CodeDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-codedocument)

#### Class: IntroDocument

- Super: [CommentDocument](#class-commentdocument)

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
  > from typing import List
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
  > from doc.base import FileSysDocument, GLOBAL
  > from doc.globe import ModuleDocument, GlobalDocument
  > from doc.series import ClassDocument
  > ```

### File System Document Objects

Documentize tokenized code files, and check style rules in the meanwhile.

In this level, a document directory controller will traverse every folder in MLRepo. At each folder, controller will identify all python files, and generate their markdown notes by their file controllers. Generated notes is then merged into README file inside current directory.

In the README file, super links to exact Github code position are also created for global or global-class level classes, functions, and blocks. Styled code snaps for those parts are also attached with them.

For function or class inside a function, local-class or branch-of-block, it will be compressed into its name definition. Arguments or codes of it will be replaced by "..." which can be used as python ellipsis for code.

After the generation, a strict description matching is applied on classes with inheritance relationships so that inherited classes only extends function argument names and description details of inheriting classes. This also autofills the exact Github code positions for module imports and classes.

#### Class: DirectoryDocument

- Super: [FileSysDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-filesysdocument)

#### Class: FileDocument

- Super: [FileSysDocument](https://github.com/gao462/MLRepo/tree/main/doc#class-filesysdocument)

#### Function: toc