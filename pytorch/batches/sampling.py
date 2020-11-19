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
import torch
import multiprocessing

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from pytorch.datasets.dataset import Dataset
from pytorch.reforms.transform import Transform
from pytorch.logging import POSITION


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Sampling Operations >>
# The parallelable sampling operations.
# They will only communicate with batching operations with a single pair of
# requirement and response queues.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Sampling(object):
    r"""
    Sampling from dataset.
    """
    def __init__(
        self: Sampling,
        dataset: Dataset,
        sample_requires: multiprocessing.Queue[Tuple[int, int]],
        sample_responses: multiprocessing.Queue[
            Tuple[int, Dict[str, torch.Tensor]],
        ],
        *args: ArgT,
        transform: Transform, blocking: bool,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialization.

        Args
        ----
        - self
        - dataset
            Dataset.
        - sample_requires.
            Sample requirement queue.
        - sample_responses.
            Sample response queue.
        - *args
        - transform
            Transform.
        - blocking
            If True, it should be used as blocking way.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        # Save necessary attributes.
        self.PID: Const = os.getpid()
        self.DATASET: Const = dataset
        self.SAMPLE_REQUIRES: Const = sample_requires
        self.SAMPLE_RESPONSES: Const = sample_responses
        self.TRANSFORM: Const = transform
        self.BLOCKING: Const = blocking

        # Get name for logging.
        self.name = "\"Sampling{:s}\", ".format(
            "" if self.BLOCKING else " [{:d}]".format(self.PID)
        )

        # Allow calling.
        self.closed = False

    def __call__(
        self: Sampling,
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
        debug("{:s}\"\033[36;4;1mDuplicate\033[0m\".", self.name)

        # Loop forever.
        while (self.call()):
            # Operations are embedded in condition.
            pass

        # Notify a new process joining to main process.
        debug("{:s}\"\033[32;4;1mTerminate\033[0m\".", self.name)

    def call(
        self: Sampling,
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

        # Get a sample requirement or ending signal.
        sample_require = self.SAMPLE_REQUIRES.get()

        # Put a sample response or tail element.
        if (self.ending(sample_require)):
            self.SAMPLE_RESPONSES.put(self.fin(sample_require))
            self.closed = True
        else:
            self.SAMPLE_RESPONSES.put(self.run(sample_require))
            self.closed = False
        return not self.closed

    def ending(
        self: Sampling,
        sample_require: Tuple[int, int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        Check ending signal.

        Args
        ----
        - self
        - sample_require
            Sample requirement.
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, this requirement is an ending signal.

        """

        # Decode requirement.
        src, dst = sample_require
        return src < 0 or dst < 0

    def run(
        self: Sampling,
        sample_require: Tuple[int, int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Tuple[int, Dict[str, torch.Tensor]]:
        r"""
        Real operations.

        Args
        ----
        - self
        - sample_require
            Sample requirement.
        - *args
        - **kargs

        Returns
        -------
        - sample_response
            Sample response.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode requirement.
        src, dst = sample_require

        # Get from disk.
        debug(
            "{:s}\"\033[33mDataset [{:d}]\033[0m ==>" \
            " \033[33mBatch [{:d}]\033[0m\".",
            self.name, src, dst,
        )

        # Load from dataset and transform.
        try:
            sample = self.TRANSFORM(self.DATASET[src])
            return (dst, sample)
        except:
            error(
                "{:s}Fail to transform \"{:s}\".",
                self.name, POSITION.format("Dataset [{:d}]".format(src)),
            )
            raise RuntimeError

    def fin(
        self: Sampling,
        sample_require: Tuple[int, int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Tuple[int, Dict[str, torch.Tensor]]:
        r"""
        Final operations.

        Args
        ----
        - self
        - sample_require
            Sample requirement.
        - *args
        - **kargs

        Returns
        -------
        - sample_response
            Sample response.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode requirement.
        src, dst = sample_require
        debug("{:s}\"\033[33mDataset [{:d}]\033[0m\" (Fin).", self.name, src)

        # Return a null element.
        return (-1, {})