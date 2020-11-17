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
from pytorch.batches.paralf import FunctionalProcess
from pytorch.batches.sampling import Sampling
from pytorch.logging import POSITION


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Batching Operations >>
# The batching operations.
# They are parallelable.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Batching(FunctionalProcess[
    List[int], Dict[str, List[torch.Tensor]],
]):
    r"""
    Batching from dataset.
    """
    def init(
        self: Batching,
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
        self.requires: multiprocessing.Queue[Tuple[int, int]]
        self.responses: multiprocessing.Queue[
            Tuple[int, Dict[str, torch.Tensor]],
        ]
        self.samplers: List[multiprocessing.Process]

        # Get batching transform.
        self.transform = xargs[2]

        # Allocate queues.
        self.requires = multiprocessing.Queue()
        self.responses = multiprocessing.Queue(xkargs["qmax_samples"])

        # Define and start children sampling processes.
        self.samplers = []
        for i in range(xkargs["num_samplers"]):
            # Define children PID.
            if (self.PID == "0"):
                pid = "{:d}".format(i + 1)
            else:
                pid = "{:s}.{:d}".format(self.PID, i + 1)

            # Create and start a children process.
            sampler = multiprocessing.Process(
                target=Sampling(
                    pid=pid, inputs=self.requires, outputs=self.responses,
                    xargs=(xargs[0], xargs[1]),
                    xkargs=dict(),
                ),
                args=(), kwargs={}, daemon=False,
            )
            sampler.start()
            self.samplers.append(sampler)

        # Define blocking operation.
        if (len(self.samplers) == 0):
            self.blocking = Sampling(
                pid=self.PID, inputs=self.requires, outputs=self.responses,
                xargs=(xargs[0], xargs[1]), xkargs={},
            )
        else:
            pass

    def ending(
        self: Batching,
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
        self: Batching,
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
        memory: List[Tuple[int, Dict[str, torch.Tensor]]]
        ordering: Callable[[Tuple[int, Dict[str, torch.Tensor]]], int]
        raw: Dict[str, List[torch.Tensor]]

        # Decode input.
        chunk = input
        debug(
            "{:s}\"\033[32mBatch [{:s}]\033[0m\".",
            self.name, ", ".join([str(itr) for itr in chunk]),
        )

        # Put decoded requirements.
        for dst, src in enumerate(chunk):
            self.requires.put((src, dst))

        # Get enough responses to memory.
        memory = []
        while (len(memory) < len(chunk)):
            # Run blocking operation explicitly if necessary.
            if (len(self.samplers) == 0):
                self.blocking.call()
            else:
                pass

            # Fetch a response.
            slot, sample = self.responses.get()

            # Use clone as PyTorch suggested.
            clone = {key: val.clone() for key, val in sample.items()}
            del sample

            # Save to batch memory.
            memory.append((slot, clone))

        # Recover requirement order.
        ordering = lambda x: x[0]
        memory = sorted(memory, key=ordering)

        # Process raw memory into proper batch form.
        raw = {key: [] for key in memory[0][1].keys()}
        for slot, clone in memory:
            for key, val in clone.items():
                raw[key].append(val)

        # Some additional transforms on the loaded batch.
        try:
            obj = self.transform(raw)
            return cast(Dict[str, List[torch.Tensor]], obj)
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
            "{:s}\"\033[32mBatch [{:s}]\033[0m\" (Fin).",
            self.name, ", ".join([str(itr) for itr in chunk]),
        )

        # Send ending signals to sampling processes.
        for sampler in self.samplers:
            self.requires.put((-1, -1))
        for sampler in self.samplers:
            self.responses.get()

        # Run blocking final operation explicitly for its explicit definition.
        if (len(self.samplers) == 0):
            self.requires.put((-1, -1))
            self.blocking.call()
            self.responses.get()
        else:
            pass

        # Return a null element.
        return {"": []}