## Table Of Content

* [pytorch/logging.py](#pytorchloggingpy)
  * [Define Logging Utilities](#define-logging-utilities)
    * [Block: Different levels...](#block-different-levels)
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

#### Block: Different levels...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L39)
> ```python
> # Different levels as integers.
> DEBUG = 10
> INFO1 = 20
> INFO2 = 25
> FOCUS = 30
> WARNING = 40
> ERROR = 50
> ```

[[TOC]](#table-of-content)

#### Function: default_logger

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L48)

Create default logger.

> **Arguments**

> **Returns**

> ```python
> # Allocate logger.
> logger = logging.getLogger("default_logger")
> logger.setLevel(level=DEBUG)
>
> # Define logging line format.
> formatter = logging.Formatter("%(message)s")
>
> # Define console streaming.
> console_stream = logging.StreamHandler()
> console_stream.setLevel(level=DEBUG)
> console_stream.setFormatter(formatter)
>
> # Add stream to logger.
> logger.addHandler(console_stream)
> return logger
> ```

[[TOC]](#table-of-content)

#### Block: Univeral logger a...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L80)
> ```python
> # Univeral logger and maximum number of characters.
> UNIVERSAL_LOGGER = default_logger()
> MAX = 10 + 79
> ```

[[TOC]](#table-of-content)

#### Function: update_universal_logger

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L85)

Update universal logger by given logger.

> **Arguments**

> **Returns**

> ```python
> # Replace directly.
> global UNIVERSAL_LOGGER
> UNIVERSAL_LOGGER = logger
> ```

[[TOC]](#table-of-content)

#### Function: update_max

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L107)

Update maximum number of characters.

> **Arguments**

> **Returns**

> ```python
> # Replace directly.
> global MAX
> MAX = val
> ```

[[TOC]](#table-of-content)

#### Block: Colorful ASCII co...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L127)
> ```python
> # Colorful ASCII code on ConEmu palette.
> CLR_BLACK = "30"
> CLR_ORANGE = "31"
> CLR_TEAL = "32"
> CLR_OLIVE = "33"
> CLR_CADET = "34"
> CLR_PURPLE = "35"
> CLR_NAVY = "36"
> CLR_PALE = "37"
> CLR_GRAY = "30;1"
> CLR_RED = "31;1"
> CLR_GREEN = "32;1"
> CLR_YELLOW = "33;1"
> CLR_BLUE = "34;1"
> CLR_PINK = "35;1"
> CLR_CYAN = "36;1"
> CLR_WHITE = "37;1"
> ```

[[TOC]](#table-of-content)

#### Block: Colorful fix-leng...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L146)
> ```python
> # Colorful fix-length level.
> CLRFIX = {}
> CLRFIX[DEBUG] = "\033[{:s}mDEBUG   \033[0m".format(CLR_YELLOW)
> CLRFIX[INFO1] = "\033[{:s}mINFO    \033[0m".format(CLR_CYAN)
> CLRFIX[INFO2] = "\033[{:s}mINFO    \033[0m".format(CLR_BLUE)
> CLRFIX[FOCUS] = "\033[{:s}mINFO    \033[0m".format(CLR_GREEN)
> CLRFIX[WARNING] = "\033[{:s}mWARNING \033[0m".format(CLR_PINK)
> CLRFIX[ERROR] = "\033[{:s}mERROR   \033[0m".format(CLR_RED)
> ```

[[TOC]](#table-of-content)

#### Function: check_format

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L156)

Check message format.

> **Arguments**

> **Returns**

> ```python
> # Message must start with a captial character.
> if (msg[0].isdigit() or msg[0].isupper()):
>     pass
> else:
>     warning(
>         "Message should start with a captial char.",
>     )
>
> # Message must end with dot.
> if (msg[-1] == "."):
>     pass
> else:
>     warning(
>         "Message should end with \".\".",
>     )
> ```

[[TOC]](#table-of-content)

#### Function: log

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L190)

Log debug message.

> **Arguments**

> **Returns**

> ```python
> # Get message string.
> msg = fmt.format(*args, **kargs)
> check_format(level=level, msg=msg)
>
> # Use universal logger for multiple-line logging.
> global UNIVERSAL_LOGGER
> global MAX
> first = True
> previous = "\033[0m"
> for buf in msg.split("\n"):
>     while (len(buf) > 0):
>         # Get maximum pure characters and the latest style.
>         ptr = 0
>         cnt = 0
>         style = previous
>         while (ptr < len(buf) and cnt < MAX):
>             if (buf[ptr] == "\033"):
>                 style = "\033"
>                 while (buf[ptr] != "m"):
>                     style = style + buf[ptr]
>                     ptr += 1
>                 style = style + "m"
>             else:
>                 cnt += 1
>             ptr += 1
>
>         # Log at most maximum characters with previous styles.
>         if (first):
>             lead = "{:s}| {:s}".format(CLRFIX[level], previous)
>             first = False
>         else:
>             lead = "\033[0m        | {:s}".format(previous)
>         UNIVERSAL_LOGGER.log(level, lead + buf[:ptr] + "\033[0m")
>         buf = buf[ptr:]
>         previous = style
> ```

[[TOC]](#table-of-content)

### Define Logging Operations

Operations are just `log` function with fixed logging level integer. The corresponding values are given in the paranthese. 1, `debug` (10). 2, `info1` (20). 3, `info2` (25). 4, `focus` (30). 5, `warning` (40). 6, `error` (50).

#### Function: debug

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L261)

Log debug message.

> **Arguments**

> **Returns**

> ```python
> # Send message to universal logger.
> log(DEBUG, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content)

#### Function: info1

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L280)

Log info (dark) message.

> **Arguments**

> **Returns**

> ```python
> # Send message to universal logger.
> log(INFO1, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content)

#### Function: info2

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L299)

Log info (bright) message.

> **Arguments**

> **Returns**

> ```python
> # Send message to universal logger.
> log(INFO2, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content)

#### Function: focus

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L318)

Log focusing message.

> **Arguments**

> **Returns**

> ```python
> # Send message to universal logger.
> log(FOCUS, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content)

#### Function: warning

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L337)

Log warning message.

> **Arguments**

> **Returns**

> ```python
> # Send message to universal logger.
> log(WARNING, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content)

#### Function: error

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L356)

Log error message.

> **Arguments**

> **Returns**

> ```python
> # Send message to universal logger.
> log(ERROR, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content)