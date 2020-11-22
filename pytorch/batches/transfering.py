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
from pytorch.datasets.dataset import Dataset
from pytorch.reforms.transform import Transform
from pytorch.reforms.stackform import Stackform
from pytorch.batches.sampling import Sampling
from pytorch.batches.batching import Batching


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transfer Operations >>
# The parallelable transfer operations.
# They will mostly communicate with batching operations with a pair of batch
# requirement and response queues.
# It also sends ending signal to sampling operations.
# The sampling and batching processes will also be created here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Transfering(object):
    r"""
    Transfering to device.
    """
    def __init__(
        self: Transfering,
        dataset: Dataset, device: str,
        transfer_requires: queue.Queue[List[int]],
        transfer_responses: queue.Queue[Dict[str, torch.Tensor]],
        *args: ArgT,
        sample_transform: Transform,
        batch_stackform: Stackform, batch_transform: Transform,
        num_samplers: int, qmax_samples: int,
        num_batchers: int, qmax_batches: int,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialization.

        Args
        ----
        - self
        - dataset
            Dataset.
        - device
            Device.
        - transfer_requires.
            Transfer requirement queue.
        - transfer_responses.
            Transfer response queue.
        - *args
        - sample_transform
            Sample transform.
        - batch_stackform
            Batch Stackform.
        - batch_transform
            Transform.
        - num_samplers
            Number of samplers.
        - qmax_batches
            Queue maximum size for samples.
        - num_batchers
            Number of batchers.
        - qmax_batches
            Queue maximum size for batches.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        # Save necessary attributes.
        self.DATASET: Const = dataset
        self.DEVICE: Const = device
        self.TRANSFER_REQUIRES = transfer_requires
        self.TRANSFER_RESPONSES = transfer_responses
        self.SAMPLE_TRANFORM = sample_transform
        self.BATCH_STACKFORM = batch_stackform
        self.BATCH_TRANFORM = batch_transform
        self.NUM_SAMPLERS = num_samplers
        self.QMAX_SAMPLES = qmax_samples
        self.NUM_BATCHERS = num_batchers
        self.QMAX_BATCHES = qmax_batches

        # /
        # ANNOTATE VARIABLES
        # /
        self.sample_requires: multiprocessing.Queue[Tuple[int, int]]
        self.sample_responses: multiprocessing.Queue[
            Tuple[int, Dict[str, torch.Tensor]],
        ]
        self.batch_requires: multiprocessing.Queue[List[int]]
        self.batch_responses: multiprocessing.Queue[Dict[str, torch.Tensor]]
        self.sampling: Union[Sampling, None]
        self.batching: Union[Batching, None]

        # Get name for logging.
        self.name = "\"Transfering\", "

        # Allow calling.
        self.closed = False

        # Allocate queues.
        self.sample_requires = multiprocessing.Queue()
        self.sample_responses = multiprocessing.Queue(self.QMAX_SAMPLES)
        self.batch_requires = multiprocessing.Queue()
        self.batch_responses = multiprocessing.Queue(self.QMAX_BATCHES)

        # Define and start children sampling processes.
        self.samplers = []
        for i in range(self.NUM_SAMPLERS):
            # Create and start a children process.
            sampler = multiprocessing.Process(
                target=Sampling(
                    self.DATASET,
                    self.sample_requires, self.sample_responses,
                    transform=self.SAMPLE_TRANFORM,
                    blocking=False,
                ),
            )
            sampler.start()
            self.samplers.append(sampler)

        # Define blocking sampling operation if necessary.
        if (len(self.samplers) == 0):
            self.sampling = Sampling(
                self.DATASET,
                self.sample_requires, self.sample_responses,
                transform=self.SAMPLE_TRANFORM,
                blocking=True,
            )
        else:
            self.sampling = None

        # Define and start children batching processes.
        self.batchers = []
        for i in range(self.NUM_BATCHERS):
            # Create and start a children process.
            batcher = multiprocessing.Process(
                target=Batching(
                    self.sampling,
                    self.sample_requires, self.sample_responses,
                    self.batch_requires, self.batch_responses,
                    stackform=self.BATCH_STACKFORM,
                    transform=self.BATCH_TRANFORM,
                    blocking=False,
                ),
            )
            batcher.start()
            self.batchers.append(batcher)

        # Define blocking batching operation if necessary.
        if (len(self.batchers) == 0):
            self.batching = Batching(
                self.sampling,
                self.sample_requires, self.sample_responses,
                self.batch_requires, self.batch_responses,
                stackform=self.BATCH_STACKFORM,
                transform=self.BATCH_TRANFORM,
                blocking=False,
            )
        else:
            self.batching = None

    def __call__(
        self: Transfering,
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
        debug("{:s}\"\033[36;4;1mFork\033[0m\".", self.name)

        # Loop forever.
        while (self.call()):
            # Operations are embedded in condition.
            pass

        # Notify a new process joining to main process.
        debug("{:s}\"\033[32;4;1mJoin\033[0m\".", self.name)

    def call(
        self: Transfering,
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

        # Get a transfer requirement or ending signal.
        transfer_require = self.TRANSFER_REQUIRES.get()

        # Put a transfer response or tail element.
        if (self.ending(transfer_require)):
            self.TRANSFER_RESPONSES.put(self.fin(transfer_require))
            self.closed = True
        else:
            self.TRANSFER_RESPONSES.put(self.run(transfer_require))
            self.closed = False
        return not self.closed

    def ending(
        self: Transfering,
        input: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        Check ending signal.

        Args
        ----
        - self
        - transfer_require
            Transfer requirement.
        - *args
        - **kargs

        Returns
        -------
        - flag
            If True, this requirement is an ending signal.

        """

        # Decode input.
        chunk = input
        return len(chunk) == 0

    def run(
        self: Transfering,
        transfer_require: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Real operations.

        Args
        ----
        - self
        - transfer_require
            Transfer requirement.
        - *args
        - **kargs

        Returns
        -------
        - transfer_response
            Transfer response.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode requirement.
        chunk = transfer_require
        debug(
            "{:s}\"\033[32mBatch[{:s}] [{:s}]\033[0m\".",
            self.name, self.DEVICE.upper(),
            ", ".join([str(itr) for itr in chunk]),
        )

        # Put batch requirements and get response.
        self.batch_requires.put(chunk)
        if (self.batching is None):
            pass
        else:
            self.batching.call()
        batch = self.batch_responses.get()

        # Transfer to device without blocking.
        device = {}
        for key, val in batch.items():
            if (key[0] == "$"):
                device[key] = val.clone()
            else:
                device[key] = val.clone().to(self.DEVICE, non_blocking=True)
        del batch
        return device

    def fin(
        self: Transfering,
        transfer_require: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Final operations.

        Args
        ----
        - self
        - transfer_require
            Transfer requirement.
        - *args
        - **kargs

        Returns
        -------
        - transfer_response
            Transfer response.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode requirement.
        chunk = transfer_require
        debug(
            "{:s}\"\033[32mBatch[{:s}] [{:s}]\033[0m\" (Fin).",
            self.name, self.DEVICE.upper(),
            ", ".join([str(itr) for itr in chunk]),
        )

        # Send ending signals to sampling processes.
        for sampler in self.samplers:
            self.sample_requires.put((-1, -1))

        # Run blocking final operation explicitly for its explicit definition.
        if (self.sampling is None):
            pass
        else:
            self.sample_requires.put((-1, -1))
            self.sampling.call()

        # Send ending signals to batching processes.
        for batcher in self.batchers:
            self.batch_requires.put([])

        # Run blocking final operation explicitly for its explicit definition.
        if (self.batching is None):
            pass
        else:
            self.batch_requires.put([])
            self.batching.call()

        # Ensure samplers and batchers are terminated.
        for sampler in self.samplers:
            sampler.join()
        for batcher in self.batchers:
            batcher.join()

        # Shutdown queues explicitly.
        self.sample_requires.close()
        self.sample_requires.join_thread()
        self.sample_responses.close()
        self.sample_responses.join_thread()
        self.batch_requires.close()
        self.batch_requires.join_thread()
        self.batch_responses.close()
        self.batch_responses.join_thread()

        # Return a null element.
        return {"": torch.Tensor([0])}