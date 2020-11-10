* Table of Content
  * [pytorch/logging.py](#pytorch-loggingpy)
    * [Define Logging Utilities](#define-logging-utilities)
      * [Block: Different levels ...](#block-different-levels)
      * [Function: default_logger](#function-default_logger)
      * [Block: Univeral logger a...](#block-univeral-logger-a)
      * [Function: update_universal_logger](#function-update_universal_logger)
      * [Function: update_max](#function-update_max)
      * [Block: Colorful ASCII co...](#block-colorful-ascii-co)
      * [Block: Colorful fix-leng...](#block-colorful-fix-leng)
      * [Function: check_format](#function-check_format)
      * [Function: log](#function-log)
    * [Define Logging Operations](#define-logging-operations)
      * [Function: debug](#function-debug)
      * [Function: info1](#function-info1)
      * [Function: info2](#function-info2)
      * [Function: focus](#function-focus)
      * [Function: warning](#function-warning)
      * [Function: error](#function-error)

---

## pytorch/logging.py

- Dependent on: `__future__`, `typing`, `sys`, `os`, `logging`

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
  > import logging
  >
  > # Add development library to path.
  > if (os.path.basename(os.getcwd()) == "MLRepo"):
  >     sys.path.append(os.path.join("."))
  > else:
  >     print("Code must strictly work in \"MLRepo\".")
  >     exit()
  >
  > # Import logging.
  >
  > # Import dependencies.
  > ```

### Define Logging Utilities

1, Create default logger. 2, Universal logger. 3, Update universal logger by given logger. 4, Check message format. 5, Output multiple-line message.

#### Block: Different levels ...

#### Function: default_logger

#### Block: Univeral logger a...

#### Function: update_universal_logger

#### Function: update_max

#### Block: Colorful ASCII co...

#### Block: Colorful fix-leng...

#### Function: check_format

#### Function: log

### Define Logging Operations

Operations are just `log` function with fixed logging level integer. The corresponding values are given in the paranthese. 1, `debug` (10). 2, `info1` (20). 3, `info2` (25). 4, `focus` (30). 5, `warning` (40). 6, `error` (50).

#### Function: debug

#### Function: info1

#### Function: info2

#### Function: focus

#### Function: warning

#### Function: error