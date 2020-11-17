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
from pytorch.batches.paralf import FunctionalThread
from pytorch.batches.batching import Batching


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transfering Operations >>
# The transfering operations.
# They are parallelable.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Transfering(FunctionalThread[
    List[int], Dict[str, List[torch.Tensor]],
]):
    r"""
    Transfering to device.
    """
    def init(
        self: Transfering,
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
        # ANNOTATE VARIABLES
        # /
        self.requires: multiprocessing.Queue[List[int]]
        self.responses: multiprocessing.Queue[Dict[str, List[torch.Tensor]]]
        self.batchers: List[multiprocessing.Process]

        # Get device.
        self.device = xargs[3]

        # Allocate queues.
        self.requires = multiprocessing.Queue()
        self.responses = multiprocessing.Queue(xkargs["qmax_batches"])

        # Define and start children batching processes.
        self.batchers = []
        for i in range(xkargs["num_batchers"]):
            # Define children PID.
            if (self.PID == "0"):
                pid = "{:d}".format(i + 1)
            else:
                pid = "{:s}.{:d}".format(self.PID, i + 1)

            # Create and start a children process.
            batcher = multiprocessing.Process(
                target=Batching(
                    pid=pid, inputs=self.requires, outputs=self.responses,
                    xargs=(xargs[0], xargs[1], xargs[2]),
                    xkargs=dict(
                        num_samplers=xkargs["num_samplers"],
                        qmax_samples=xkargs["qmax_samples"],
                    ),
                ),
                args=(), kwargs={}, daemon=False,
            )
            batcher.start()
            self.batchers.append(batcher)

        # Define blocking operation.
        if (len(self.batchers) == 0):
            self.blocking = Batching(
                pid=self.PID, inputs=self.requires, outputs=self.responses,
                xargs=(xargs[0], xargs[1], xargs[2]),
                xkargs=dict(
                    num_samplers=xkargs["num_samplers"],
                    qmax_samples=xkargs["qmax_samples"],
                ),
            )
        else:
            pass

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
        - input
            Input.
        - *args
        - **kargs

        Returns
        -------

        """

        # Decode input.
        chunk = input
        return len(chunk) == 0

    def run(
        self: Transfering,
        input: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, List[torch.Tensor]]:
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
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode input directly as requirement.
        chunk = input
        debug(
            "{:s}\"\033[32mBatch[{:s}] [{:s}]\033[0m\".",
            self.name, self.device.upper(),
            ", ".join([str(itr) for itr in chunk]),
        )

        # Ask and fetch a batch.
        self.requires.put(chunk)
        if (len(self.batchers) == 0):
            self.blocking.call()
        else:
            pass
        batch = self.responses.get()

        # Transfer to device without blocking.
        clonedev = {
            key: [
                itr.clone().to(self.device, non_blocking=True)
                for itr in val
            ]
            for key, val in batch.items()
        }
        del batch
        return clonedev

    def fin(
        self: Transfering,
        input: List[int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, List[torch.Tensor]]:
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
        # ANNOTATE VARIABLES
        # /
        ...

        # Decode input.
        chunk = input
        debug(
            "{:s}\"\033[32mBatch[{:s}] [{:s}]\033[0m\" (Fin).",
            self.name, self.device, ", ".join([str(itr) for itr in chunk]),
        )

        # Send ending signals to batching processes.
        for batcher in self.batchers:
            self.requires.put([])
        for batcher in self.batchers:
            self.responses.get()

        # Run blocking final operation explicitly for its explicit definition.
        if (len(self.batchers) == 0):
            self.requires.put([])
            self.blocking.call()
            self.responses.get()
        else:
            pass

        # Return a null element.
        return {"": []}