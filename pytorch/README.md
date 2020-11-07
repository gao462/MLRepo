
---

## pytorch/logging.py

- Dependent on: `typing`, `sys`, `os`, `logging`.

### Define Logging Utilities

1, Create default logger. 2, Universal logger. 3, Update universal logger by given logger. 4, Check message format. 5, Output multiple-line message.

- Block

  Different levels as integers.

- Function [**default_logger**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L45)()

  Create default logger.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > No arguments.

  > **Returns**
  > - **logger**: *logging.Logger*
  >   Default logger.

- Block

  Univeral logger and maximum number of characters.

- Function [**update_universal_logger**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L80)(*logger*)

  Update universal logger by given logger.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - **logger**: *logging.Logger*
  >   New logger.

  > **Returns**
  > No returns.

- Function [**update_max**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L98)(*val*)

  Update maximum number of characters.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - **val**: *int*
  >   Maximum.

  > **Returns**
  > No returns.

- Block

  Colorful ASCII code on ConEmu palette.

- Block

  Colorful fix-length level.

- Function [**check_format**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L145)(*level, msg*)

  Check message format.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - **level**: *int*
  >   Logging level.
  > - **msg**: *str*
  >   Message.

  > **Returns**
  > No returns.

- Function [**log**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L179)(*level, fmt, *args, **kargs*)

  Log debug message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - **level**: *int*
  >   Logging level.
  > - **fmt**: *str*
  >   Formatter.
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.

### Define Logging Operations

1, debug (10). 2, info1 (20). 3, info2 (25). 4, focus (30). 5, warning (40). 6, error (50).

- Function [**debug**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L248)(**args, **kargs*)

  Log debug message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.

- Function [**info1**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L265)(**args, **kargs*)

  Log info (dark) message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.

- Function [**info2**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L282)(**args, **kargs*)

  Log info (bright) message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.

- Function [**focus**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L299)(**args, **kargs*)

  Log focusing message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.

- Function [**warning**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L316)(**args, **kargs*)

  Log warning message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.

- Function [**error**](https://github.com/gao462/MLRepo/blob/master/pytorch/logging.py#L333)(**args, **kargs*)

  Log error message.

  > **Decorators**
  > No decorators.

  > **Arguments**
  > - ***args**
  > - ****kargs**

  > **Returns**
  > No returns.