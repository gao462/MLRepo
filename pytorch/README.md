## Table Of Content

* [File: pytorch/logging.py](#file-pytorchloggingpy)
* [Section: Define Logging Utilities](#section-define-logging-utilities)
* [Block: pytorch.logging: Different levels...](#block-pytorchlogging-different-levels)
* [Function: pytorch.logging.default\_logger](#function-pytorchloggingdefault_logger)
* [Block: pytorch.logging: Univeral logger a...](#block-pytorchlogging-univeral-logger-a)
* [Function: pytorch.logging.update\_universal\_logger](#function-pytorchloggingupdate_universal_logger)
* [Function: pytorch.logging.update\_max](#function-pytorchloggingupdate_max)
* [Block: pytorch.logging: Colorful ASCII co...](#block-pytorchlogging-colorful-ascii-co)
* [Block: pytorch.logging: Colorful fix-leng...](#block-pytorchlogging-colorful-fix-leng)
* [Function: pytorch.logging.check\_format](#function-pytorchloggingcheck_format)
* [Function: pytorch.logging.log](#function-pytorchlogginglog)
* [Section: Define Logging Operations](#section-define-logging-operations)
* [Function: pytorch.logging.debug](#function-pytorchloggingdebug)
* [Function: pytorch.logging.info1](#function-pytorchlogginginfo1)
* [Function: pytorch.logging.info2](#function-pytorchlogginginfo2)
* [Function: pytorch.logging.focus](#function-pytorchloggingfocus)
* [Function: pytorch.logging.warning](#function-pytorchloggingwarning)
* [Function: pytorch.logging.error](#function-pytorchloggingerror)

---

## File: pytorch/logging.py

* [Section: Define Logging Utilities](#section-define-logging-utilities)
* [Block: pytorch.logging: Different levels...](#block-pytorchlogging-different-levels)
* [Function: pytorch.logging.default\_logger](#function-pytorchloggingdefault_logger)
* [Block: pytorch.logging: Univeral logger a...](#block-pytorchlogging-univeral-logger-a)
* [Function: pytorch.logging.update\_universal\_logger](#function-pytorchloggingupdate_universal_logger)
* [Function: pytorch.logging.update\_max](#function-pytorchloggingupdate_max)
* [Block: pytorch.logging: Colorful ASCII co...](#block-pytorchlogging-colorful-ascii-co)
* [Block: pytorch.logging: Colorful fix-leng...](#block-pytorchlogging-colorful-fix-leng)
* [Function: pytorch.logging.check\_format](#function-pytorchloggingcheck_format)
* [Function: pytorch.logging.log](#function-pytorchlogginglog)
* [Section: Define Logging Operations](#section-define-logging-operations)
* [Function: pytorch.logging.debug](#function-pytorchloggingdebug)
* [Function: pytorch.logging.info1](#function-pytorchlogginginfo1)
* [Function: pytorch.logging.info2](#function-pytorchlogginginfo2)
* [Function: pytorch.logging.focus](#function-pytorchloggingfocus)
* [Function: pytorch.logging.warning](#function-pytorchloggingwarning)
* [Function: pytorch.logging.error](#function-pytorchloggingerror)

## Section: Define Logging Utilities

1, Create default logger. 2, Universal logger. 3, Update universal logger by given logger. 4, Check message format. 5, Output multiple-line message.

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Block: pytorch.logging: Different levels...

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

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.default\_logger

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L48)

Create default logger.

> **Arguments**
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**
> - **logger**: *logging.Logger*
>
>   Default logger.

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

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Block: pytorch.logging: Univeral logger a...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L80)

> ```python
> # Univeral logger and maximum number of characters.
> UNIVERSAL_LOGGER = default_logger()
> MAX = 10 + 79
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.update\_universal\_logger

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L85)

Update universal logger by given logger.

> **Arguments**
> - **\*args**: *object*
>
> - **logger**: *logging.Logger*
>
>   New logger.
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Replace directly.
> global UNIVERSAL_LOGGER
> UNIVERSAL_LOGGER = logger
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.update\_max

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L107)

Update maximum number of characters.

> **Arguments**
> - **\*args**: *object*
>
> - **val**: *int*
>
>   Maximum.
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Replace directly.
> global MAX
> MAX = val
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Block: pytorch.logging: Colorful ASCII co...

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

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Block: pytorch.logging: Colorful fix-leng...

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

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.check\_format

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L156)

Check message format.

> **Arguments**
> - **\*args**: *object*
>
> - **level**: *int*
>
>   Logging level.
>
> - **msg**: *str*
>
>   Message.
>
> - **\*\*kargs**: *object*

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

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.log

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L190)

Log debug message.

> **Arguments**
> - **level**: *int*
>
>   Logging level.
>
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

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

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

## Section: Define Logging Operations

Operations are just `log` function with fixed logging level integer. The corresponding values are given in the paranthese. 1, `debug` (10). 2, `info1` (20). 3, `info2` (25). 4, `focus` (30). 5, `warning` (40). 6, `error` (50).

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.debug

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L261)

Log debug message.

> **Arguments**
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Send message to universal logger.
> log(DEBUG, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.info1

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L280)

Log info (dark) message.

> **Arguments**
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Send message to universal logger.
> log(INFO1, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.info2

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L299)

Log info (bright) message.

> **Arguments**
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Send message to universal logger.
> log(INFO2, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.focus

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L318)

Log focusing message.

> **Arguments**
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Send message to universal logger.
> log(FOCUS, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.warning

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L337)

Log warning message.

> **Arguments**
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Send message to universal logger.
> log(WARNING, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)

---

## Function: pytorch.logging.error

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L356)

Log error message.

> **Arguments**
> - **fmt**: *str*
>
>   Formatter.
>
> - **\*args**: *object*
>
> - **\*\*kargs**: *object*

> **Returns**

> ```python
> # Send message to universal logger.
> log(ERROR, fmt, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-pytorchloggingpy)