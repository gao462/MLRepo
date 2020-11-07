
---

## pytorch/logging.py

- Dependent on: `typing`, `sys`, `os`, `logging`.

### Define Logging Utilities

1, Create default logger. 2, Universal logger. 3, Update universal logger by given logger. 4, Check message format. 5, Output multiple-line message.

- [Block](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L36)

  Different levels as integers.
  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**default_logger**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L45)(*\*args, \*\*kargs*)

  Create default logger.

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
  ```

- [Block](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L77)

  Univeral logger and maximum number of characters.
  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**update_universal_logger**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L82)(*\*args, logger, \*\*kargs*)

  Update universal logger by given logger.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *logger*: `logging.Logger`
  >   New logger.
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**update_max**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L102)(*\*args, val, \*\*kargs*)

  Update maximum number of characters.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *val*: `int`
  >   Maximum.
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- [Block](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L122)

  Colorful ASCII code on ConEmu palette.
  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- [Block](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L141)

  Colorful fix-length level.
  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**check_format**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L151)(*\*args, level, msg, \*\*kargs*)

  Check message format.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *level*: `int`
  >   Logging level.
  > - *msg*: `str`
  >   Message.
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**log**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L187)(*level, fmt, \*args, \*\*kargs*)

  Log debug message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *level*: `int`
  >   Logging level.
  > - *fmt*: `str`
  >   Formatter.
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.

  # Code Styled Copy (CSC) is not implemented.
  ```

### Define Logging Operations

1, debug (10). 2, info1 (20). 3, info2 (25). 4, focus (30). 5, warning (40). 6, error (50).

- Function [**debug**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L256)(*\*args, \*\*kargs*)

  Log debug message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**info1**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L273)(*\*args, \*\*kargs*)

  Log info (dark) message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**info2**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L290)(*\*args, \*\*kargs*)

  Log info (bright) message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**focus**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L307)(*\*args, \*\*kargs*)

  Log focusing message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**warning**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L324)(*\*args, \*\*kargs*)

  Log warning message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```

- Function [**error**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L341)(*\*args, \*\*kargs*)

  Log error message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - *\*args*
  > - *\*\*kargs*

  > **Returns**
  > No returns.

  ```python
  # Code Styled Copy (CSC) is not implemented.
  ```