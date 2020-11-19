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
from pytorch.reforms.stackform import Stackform
from pytorch.batches.sampling import Sampling
from pytorch.logging import POSITION


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Batching Operations >>
# The parallelable batching operations.
# They will communicate with both sampling and transfering operations with a
# pair of sample requirement and response queues and a pair of batch requirment
# and response queues.
# It will automatically stack a list of samples into intergrated batch.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Batching(object):
    r"""
    Batching from dataset.
    """
    def __init__(
        self: Batching,
        sample_blocking: Union[Sampling, None],
        sample_requires: multiprocessing.Queue[Tuple[int, int]],
        sample_responses: multiprocessing.Queue[
            Tuple[int, Dict[str, torch.Tensor]],
        ],
        batch_requires: multiprocessing.Queue[List[int]],
        batch_responses: multiprocessing.Queue[Dict[str, torch.Tensor]],
        *args: ArgT,
        stackform: Stackform, transform: Transform,
        blocking: bool,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialization.

        Args
        ----
        - self
        - sample_blocking
            Blocking interface for sampling.
            If it is None, it is assumed that sampling is non-blocking.
        - sample_requires.
            Sample requirement queue.
        - sample_responses.
            Sample response queue.
        - batch_requires.
            Batch requirement queue.
        - batch_responses.
            Batch response queue.
        - *args
        - stackform
            Stackform.
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
        self.SAMPLE_BLOCKING: Const = sample_blocking
        self.SAMPLE_REQUIRES: Const = sample_requires
        self.SAMPLE_RESPONSES: Const = sample_responses
        self.BATCH_REQUIRES: Const = batch_requires
        self.BATCH_RESPONSES: Const = batch_responses
        self.STACKFORM: Const = stackform
        self.TRANSFORM: Const = transform
        self.BLOCKING: Const = blocking

        # Get name for logging.
        self.name = "\"Batching{:s}\", ".format(
            "" if self.BLOCKING else " [{:d}]".format(self.PID)
        )

        # Allow calling.
        self.closed = False

    def __call__(
        self: Batching,
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
        self: Batching,
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

        # Get a batch requirement or ending signal.
        batch_require = self.BATCH_REQUIRES.get()

        # Put a batch response or tail element.
        if (self.ending(batch_require)):
            self.BATCH_RESPONSES.put(self.fin(batch_require))
            self.closed = True
        else:
            self.BATCH_RESPONSES.put(self.run(batch_require))
            self.closed = False
        return not self.closed

    def ending(
        self: Batching,
        batch_require: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        Check ending signal.

        Args
        ----
        - self
        - batch_require
            Batch requirement.
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, this requirement is an ending signal.

        """

        # Decode requirement.
        chunk = batch_require
        return len(chunk) == 0

    def run(
        self: Batching,
        batch_require: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Real operations.

        Args
        ----
        - self
        - batch_require
            Batch requirement.
        - *args
        - **kargs

        Returns
        -------
        - batch_response
            Batch response.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        memory: List[Tuple[int, Dict[str, torch.Tensor]]]
        ordering: Callable[[Tuple[int, Dict[str, torch.Tensor]]], int]
        batch: Dict[str, torch.Tensor]

        # Decode requirement.
        chunk = batch_require
        debug(
            "{:s}\"\033[32mBatch [{:s}]\033[0m\".",
            self.name, ", ".join([str(itr) for itr in chunk]),
        )

        # Put sample requirements based on requiring chunk.
        for dst, src in enumerate(chunk):
            self.SAMPLE_REQUIRES.put((src, dst))

        # Get enough sample responses to memory.
        memory = []
        while (len(memory) < len(chunk)):
            # Run blocking operation explicitly if necessary.
            if (self.SAMPLE_BLOCKING is None):
                pass
            else:
                self.SAMPLE_BLOCKING.call()

            # Get a sample response.
            slot, sample = self.SAMPLE_RESPONSES.get()

            # Use cloned sample as PyTorch suggested.
            clone = {key: val.clone() for key, val in sample.items()}
            del sample

            # Save to batch memory.
            memory.append((slot, clone))

        # Recover requiring chunk order.
        ordering = lambda x: x[0]
        memory = sorted(memory, key=ordering)

        # Stack samples into batch and transform.
        try:
            batch = self.STACKFORM([clone for _, clone in memory])
            batch = self.TRANSFORM(batch)
            return batch
        except:
            error(
                "{:s}Fail to transform \"{:s}\".",
                self.name,
                POSITION.format("Batch [{:s}]".format(
                    ", ".join([str(itr) for itr in chunk])
                )),
            )
            raise RuntimeError

    def fin(
        self: Batching,
        batch_require: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Final operations.

        Args
        ----
        - self
        - batch_require
            Batch requirement.
        - *args
        - **kargs

        Returns
        -------
        - batch_response
            Batch response.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode requirement.
        chunk = batch_require
        debug(
            "{:s}\"\033[32mBatch [{:s}]\033[0m\" (Fin).",
            self.name, ", ".join([str(itr) for itr in chunk]),
        )

        # Return a null element.
        return {"": torch.Tensor([0])}