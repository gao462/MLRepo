# Import future.
from __future__ import annotations

# Import typing.
from typing import Any as VarArg
from typing import Final as Const
from typing import Tuple as MultiReturn
from typing import Type, Protocol
from typing import TextIO, BinaryIO
from typing import Union, Tuple, List, Dict, Set, Callable

# Import dependencies.
import sys
import os
import abc
import torch

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


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Dataset Virtual Objects >>
# The virtual dataset protoype for any dataset types.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Batch(abc.ABC):
    r"""
    Virtual class for batching.
    """
    def set(
        self: Batch,
        dataset: Dataset,
        *args: VarArg,
        num_data_threads: int, transform_thread: bool,
        config: Dict[str, VarArg],
        **kargs: VarArg,
    ) -> None:
        r"""
        Settle down batching by given configuration.

        Args
        ----
        - self
        - *args
        - num_data_threads
            Number of threads loading a sample from dataset to batch.
            If it is 0, batching will block to wait for data loading.
        - transfer_thread
            If True, an additional thread is created to transform the whole
            batch, e.g., changing device, reshaping batch.
            Otherwise, batching will block to wait for transform.
        - config
            Configuration dict.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Configure batching with given arguments.
        self.configure(config)
        raise NotImplementedError

    @abc.abstractmethod
    def configure(
        self: Dataset,
        config: Dict[str, VarArg],
        *args: VarArg,
        **kargs: VarArg,
    ) -> None:
        r"""
        Configure dataset.

        Args
        ----
        - self
        - config
            Configuration dict.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def refresh(
        self: Batch,
        *args: VarArg,
        **kargs: VarArg,
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
        # \
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def next(
        self: Batch,
        *args: VarArg,
        **kargs: VarArg,
    ) -> MultiReturn[bool, Dict[torch.Tensor]]:
        """
        Save dataset memory.

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
        # VIRTUAL
        # \
        ...