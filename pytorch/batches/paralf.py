# Import future.
from __future__ import annotations

# Import typing.
from typing import Any as ArgT
from typing import Any as KArgT
from typing import Any as Naive
from typing import Final as Const
from typing import Tuple as MultiReturn
from typing import Type, Protocol
from typing import TextIO, BinaryIO
from typing import Union, Tuple, List, Dict, Set, Callable
from typing import TypeVar, Generic
from typing import cast

# Import dependencies.
import sys
import os
import abc
import multiprocessing
import queue

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Parallelable Operations >>
# The virtual operations which is parallelable.
# The definition should support two usage.
# First is parallel usage by multiprocesssing or threading when it is used as a
# forever-loop wrapped function (__call__).
# Second is blocking usage by explicitly using a step of the function (call).
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# /
# GENERIC TYPES
# /
# Define generic process IO types.
INPUT = TypeVar("INPUT")
OUTPUT = TypeVar("OUTPUT")


class FunctionalParallel(Generic[INPUT, OUTPUT]):
    r"""
    A process or thread running parallel with main process which is defined as
    a function.
    """
    @abc.abstractmethod
    def init(
        self: FunctionalParallel[INPUT, OUTPUT],
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Specific initialization.

        Args
        ----
        - self
        - xargs
            Extra arguments to specific initialization.
        - xkargs
            Extra keyword arguments to specific initialization.
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def call(
        self: FunctionalParallel[INPUT, OUTPUT],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        An explicit step of blocking running flow.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, the step should never be called again.

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def ending(
        self: FunctionalParallel[INPUT, OUTPUT],
        input: INPUT,
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        Check ending signal.

        Args
        ----
        - self
        - input
            Input.
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def run(
        self: FunctionalParallel[INPUT, OUTPUT],
        input: INPUT,
        *args: ArgT,
        **kargs: KArgT,
    ) -> OUTPUT:
        r"""
        Real operations.

        Args
        ----
        - self
        - input
            Input.
        - *args
        - **kargs

        Returns
        -------
        - output
            Output.

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def fin(
        self: FunctionalParallel[INPUT, OUTPUT],
        input: INPUT,
        *args: ArgT,
        **kargs: KArgT,
    ) -> OUTPUT:
        r"""
        Final operations.

        Args
        ----
        - self
        - input
            Input.
        - *args
        - **kargs

        Returns
        -------
        - output
            Output.

        """
        # /
        # VIRTUAL
        # /
        ...


class FunctionalProcess(FunctionalParallel[INPUT, OUTPUT]):
    r"""
    A process running parallel with main process which is defined as a
    function.
    """
    def __init__(
        self: FunctionalProcess[INPUT, OUTPUT],
        *args: ArgT,
        pid: str, inputs: multiprocessing.Queue[INPUT],
        outputs: multiprocessing.Queue[OUTPUT],
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - *args
        - pid
            Process identifier string.
        - inputs
            Input queue.
        - outputs
            Output queue.
        - xargs
            Extra arguments to specific initialization.
        - xkargs
            Extra keyword arguments to specific initialization.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        # Save necessary attributes.
        self.PID: Const = pid
        self.INPUTS: Const = inputs
        self.OUTPUTS: Const = outputs

        # Get name as constant.
        if (self.PID == "0"):
            self.name = ""
        else:
            self.name = "\"Process [{:s}]\", ".format(self.PID)

        # Allow calling.
        self.closed = False

        # Prcoess or thread specific initialization
        self.init(xargs, xkargs)

    def __call__(
        self: FunctionalProcess[INPUT, OUTPUT],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Call as function.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Notify a new process forking from main process.
        debug("{:s}\"\033[36;4;1mDuplicate\033[0m\".".format(self.name))

        # Loop forever.
        while (self.call()):
            # Operations are embedded in condition.
            pass

        # Notify a new process joining to main process.
        debug("{:s}\"\033[32;4;1mTerminate\033[0m\".".format(self.name))

    def call(
        self: FunctionalProcess[INPUT, OUTPUT],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        An explicit step of blocking running flow.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, the forever run is approaching termination.
            If False, the step should never be called again.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Reject closed calling.
        if (self.closed):
            error("{:s} operates a closed parallelable function.", self.name)
            raise RuntimeError
        else:
            pass

        # Get an input or ending signal.
        input = self.INPUTS.get()

        # Put an output or tail element.
        if (self.ending(input)):
            self.OUTPUTS.put(self.fin(input))
            self.closed = True
        else:
            self.OUTPUTS.put(self.run(input))
            self.closed = False
        return not self.closed


class FunctionalThread(FunctionalParallel[INPUT, OUTPUT]):
    r"""
    A thread running parallel with main process which is defined as a function.
    """
    def __init__(
        self: FunctionalThread[INPUT, OUTPUT],
        *args: ArgT,
        pid: str, inputs: queue.Queue[INPUT], outputs: queue.Queue[OUTPUT],
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - *args
        - pid
            Process identifier string.
        - inputs
            Input queue.
        - outputs
            Output queue.
        - xargs
            Extra arguments to specific initialization.
        - xkargs
            Extra keyword arguments to specific initialization.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        # Save necessary attributes.
        self.PID: Const = pid
        self.INPUTS: Const = inputs
        self.OUTPUTS: Const = outputs

        # Get name.
        if (self.PID == "0"):
            self.name = ""
        else:
            self.name = "\"Process [{:s}]\", ".format(self.PID)

        # Allow calling.
        self.closed = False

        # Prcoess or thread specific initialization
        self.init(xargs, xkargs)

    def __call__(
        self: FunctionalThread[INPUT, OUTPUT],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Call as function.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # Notify a new process forking from main process.
        debug("{:s}\"\033[36;4;1mFork\033[0m\".".format(self.name))

        # Loop forever.
        while (self.call()):
            # Operations are embedded in condition.
            pass

        # Notify a new process joining to main process.
        debug("{:s}\"\033[32;4;1mJoin\033[0m\".".format(self.name))

    def call(
        self: FunctionalThread[INPUT, OUTPUT],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        An explicit step of blocking running flow.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, the forever run is approaching termination.
            If False, the step should never be called again.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Reject closed calling.
        if (self.closed):
            error("{:s} operates a closed parallelable function.", self.name)
            raise RuntimeError
        else:
            pass

        # Get an input or ending signal.
        input = self.INPUTS.get()

        # Put an output or tail element.
        if (self.ending(input)):
            self.OUTPUTS.put(self.fin(input))
            self.closed = True
        else:
            self.OUTPUTS.put(self.run(input))
            self.closed = False
        return not self.closed