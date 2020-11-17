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
import queue
import torch
import threading

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
from pytorch.transforms.transform import SampleTransform, BatchTransform
from pytorch.batches.transfering import Transfering


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Batching Virtual Objects >>
# The virtual batching protoype for any batching types.
# It will create a relative small buffer (list) with respect to dataset for
# the memory efficency.
#
# It also adopts hierarchy pipelines for efficient loading.
# PyTorch default DataLoader is not used here for a better bottom-level
# understanding and customization.
# It has two levels controlled by multiple processes which is independent from
# main forward and backward computation flow.
#
# One level is sampling processes piping a dataset sample to a batch CPU memroy
# slot.
# It is similar to worker design as in PyTorch DataLoader.
# Several independent processes will be created to fetch a data sample from
# dataset, do some single-sample-only preprocessing and put to corresponding
# location in batch CPU memory.
# This extends PyTorch data loader by direct interface for variable batch size,
# and forward and backward dependent batch requires, for example, active
# learning.
#
# The other level is batching process processing loaded batches.
# This level is higher than sampling, and each batching process will controll
# its own sampling processes.
# This can include aggregating a list of tensor into a single batch tensor,
# collecting batch-level features.
# This is still CPU level.
#
# After two levels, a thread, not process, is created from main flow just to
# transfer processed batch to target GPU.
# Since it is still tough to use CUDA tensors with multiprocessing, especially
# on putting a CUDA tensor into multiprocessing queue, only thread is used.
# When device memory is relatively sufficient, you can cache multiple batches
# on GPU for more efficiency.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Batch(abc.ABC):
    r"""
    Virtual class for batching.
    """
    def set(
        self: Batch,
        dataset: Dataset, sample_transform: SampleTransform,
        batch_transform: BatchTransform, device: str,
        *args: ArgT,
        num_samplers: int, qmax_samples: int,
        num_batchers: int, qmax_batches: int,
        qmax_remotes: int,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Settle down batching by given configuration.

        Args
        ----
        - self
        - dataset
            Dataset.
        - sample_transform
            Sample transform.
        - batch_transform
            Batch transform
        - device
            Target device.
        - *args
        - num_samplers
            Number of sampling process.
        - qmax_samples
            Maximum queue size for samples.
        - num_batchers
            Number of batching process.
        - qmax_batches
            Maximum queue size for batches.
        - qmax_device
            Maximum queue size on remote device.
        - xargs
            Extra arguments to specific configuration.
        - xkargs
            Extra keyword arguments to specific configuration.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Save necessary attributes.
        self.dataset = dataset
        self.sample_transform = sample_transform
        self.batch_transform = batch_transform
        self.device = device
        self.num_samplers = num_samplers
        self.qmax_samples = qmax_samples
        self.num_batchers = num_batchers
        self.qmax_batches = qmax_batches
        self.qmax_remotes = qmax_remotes

        # Safety check.
        if (self.qmax_remotes == 0):
            error("Can not set device queue as infinite (0).")
            raise RuntimeError
        else:
            pass

        # Configure batching with given arguments.
        self.configure(xargs, xkargs)

    @abc.abstractmethod
    def configure(
        self: Batch,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Configure batching.

        Args
        ----
        - self
        - xargs
            Extra arguments to specific configuration.
        - xkargs
            Extra keyword arguments to specific configuration.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # VIRTUAL
        # \
        ...

    def refresh(
        self: Batch,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Refresh batching progress.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        self.schedules: queue.Queue[List[int]]
        self.caches: queue.Queue[Dict[str, List[torch.Tensor]]]

        # Set schedule tracer.
        self.schedule_max = 0
        self.schedule_ptr = 0

        # Allocate queues.
        self.schedules = queue.Queue()
        self.caches = queue.Queue(self.qmax_remotes)

        # Define loading thread.
        self.thread = threading.Thread(
            target=Transfering(
                pid="0", inputs=self.schedules, outputs=self.caches,
                xargs=(
                    self.dataset, self.sample_transform, self.batch_transform,
                    self.device,
                ),
                xkargs=dict(
                    num_samplers=self.num_samplers,
                    qmax_samples=self.qmax_samples,
                    num_batchers=self.num_batchers,
                    qmax_batches=self.qmax_batches,
                ),
            ),
            args=(), kwargs={},
        )
        self.thread.start()

        # Put schedule chunks.
        chunks = self.refresh_schedule(xargs, xkargs)
        self.schedule_max += len(chunks)
        for chunk in chunks:
            self.schedules.put(chunk)

    @abc.abstractmethod
    def refresh_schedule(
        self: Batch,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> List[List[int]]:
        r"""
        Refresh batching schedule.

        Args
        ----
        - self
        - xargs
            Extra arguments to specific configuration.
        - xkargs
            Extra keyword arguments to specific configuration.
        - *args
        - **kargs

        Returns
        -------
        - chunks
            A list of refreshed schedule chunks.

        """
        # /
        # VIRTUAL
        # /
        ...

    def update(
        self: Batch,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Refresh batching progress.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        This is designed for the case when batching is determined by model
        performance, for example, active learning.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Update schedule chunks.
        chunks = self.update_schedule(xargs, xkargs)
        self.schedule_max += len(chunks)
        for chunk in chunks:
            self.schedules.put(chunk)

    @abc.abstractmethod
    def update_schedule(
        self: Batch,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> List[List[int]]:
        r"""
        Update batching schedule.

        Args
        ----
        - self
        - xargs
            Extra arguments to specific configuration.
        - xkargs
            Extra keyword arguments to specific configuration.
        - *args
        - **kargs

        Returns
        -------
        - chunks
            A list of refreshed schedule chunks.

        """
        # /
        # VIRTUAL
        # /
        ...

    def next(
        self: Batch,
        *args: ArgT,
        **kargs: KArgT,
    ) -> MultiReturn[bool, Dict[str, List[torch.Tensor]]]:
        """
        Fetch batched object from memory.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - signal
            If True, the batching progress is finished, and a refresh is
            expected.
        - obj
            Batch objecg as a dict of tensors.
            If there is a scalar value, translate it into tensor.

        This function is required to return an epoch end signal besides batch
        object.
        The end signal is used to inform upper level that all batches scheduled
        for current epoch has been traversed. In other words, batching has
        traversed essential samples from dataset once.
        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Update schedule tracer.
        self.schedule_ptr += 1

        # Fetch a batch.
        batch = self.caches.get()

        # Shutdown thread if necessary.
        if (self.schedule_ptr == self.schedule_max):
            self.schedules.put([])
            self.caches.get()
        else:
            pass
        return self.schedule_ptr == self.schedule_max, batch