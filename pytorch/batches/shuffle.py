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
from pytorch.batches.batch import Batch


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Shuffle Batching Objects >>
# The batching by shuffling dataset indices.
# This type of batching is mostly used for stochastic gradient, and requires
# that dataset indices is fixed and random-accessible (not too large) before
# an epoch.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ConstShuffleBatch(Batch):
    r"""
    Batching by shuffling with constant batch size.
    """
    def configure(
        self: ConstShuffleBatch,
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
        # ANNOTATE VARIABLES
        # \
        ...

        # Get batch size.
        self.rng = xargs[0]
        self.batch_size = xkargs["batch_size"]
        self.tail = xkargs["tail"]

    def refresh_schedule(
        self: ConstShuffleBatch,
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
        # \
        # ANNOTATE VARIABLES
        # \
        aranged: List[List[int]]

        # Get number of completely batched samples.
        num_batches = len(self.dataset) // self.batch_size
        num_completes = num_batches * self.batch_size

        # Get a random schedule.
        indices = getattr(torch, "randperm")(
            len(self.dataset), generator=self.rng,
        )

        # Get completely batched chunks.
        aranged = indices[0:num_completes].view(
            num_batches, self.batch_size,
        ).tolist()

        # Determine tail.
        if (num_completes < len(self.dataset) and self.tail):
            aranged.append(indices[num_completes:].tolist())
        else:
            pass
        return aranged

    def update_schedule(
        self: ConstShuffleBatch,
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
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Can not update anything.
        error("Constant-sized shuffling batching can not update.")
        raise RuntimeError