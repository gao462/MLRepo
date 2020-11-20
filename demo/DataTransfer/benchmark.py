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
import time

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


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Benchmark >>
# Benchmark run batching with different settings for several times to test the
# transfer efficiency.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class TransferBenchmark(object):
    r"""
    Benchmark for transfer efficiency.
    """
    def __init__(
        self: TransferBenchmark,
        dat: Dataset, batcls: type,
        sample_transform: Transform,
        batch_stackform: Stackform, batch_transform: Transform,
        model_transform: Transform,
        checkon: List[Tuple[int, int, int]],
        num_repeats: int,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - dat
            Dataset.
        - batcls
            Batching class.
        - sample_transform
            Sample transform.
        - batch_stackform
            Batch stackform.
        - batch_transform
            Batch transform.
        - model_transform
            Model transform.
        - checkon
            Check transfer efficency on given arguments.
        - *args
        - xargs
            Extra arguments for batching except for the initial random number
            generator.
        - xkargs
            Extra keyword arguments for batching.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        performances: Dict[Tuple[int, int, int], List[float]]

        # Get randomness
        seed = 47
        rng = getattr(torch, "Generator")()
        rng.manual_seed(47)
        rngmem = rng.get_state()

        # Collect performances and report progress.
        performances = {key: [] for key in checkon}
        info2("\"ID #Samplers #Batchers #GPUQueue\".")
        info2("\"-- --------- --------- ---------\".")
        for num_samplers, num_batchers, qmax_remotes in performances.keys():
            for i in range(1):
                # Get a benchmark and start.
                info2(
                    "\"{:s} {:s} {:s} {:s}\".",
                    "{:d}".format(i + 1).rjust(2),
                    "{:d}".format(num_samplers).rjust(9),
                    "{:d}".format(num_batchers).rjust(9),
                    "{:d}".format(qmax_remotes).rjust(9),
                )

                # Create batching.
                rng.set_state(rngmem)
                bat = batcls()
                bat.set(
                    dat, "cuda:0",
                    sample_transform=sample_transform,
                    batch_stackform=batch_stackform,
                    batch_transform=batch_transform,
                    num_samplers=num_samplers, qmax_samples=4,
                    num_batchers=num_batchers, qmax_batches=4,
                    qmax_remotes=qmax_remotes,
                    xargs=(rng,) + xargs, xkargs=xkargs,
                )
                bat.refresh(xargs=(), xkargs={})

                # Traverse an epoch and estimate time cost.
                start = time.time()
                while (True):
                    # Fetch a batch.
                    signal, batch = bat.next()

                    # Process fetched batch.
                    debug("\"\033[34;1mCompute\033[0m\".")
                    model_transform(batch)
                    debug("\"\033[32;1mDone\033[0m\".")

                    # Stop on ending signal.
                    if (signal):
                        break
                    else:
                        pass
                end = time.time()
                elapsed = end - start
                performances[
                    (num_samplers, num_batchers, qmax_remotes)
                ].append(elapsed)
        results = [
            (key, sum(val) / len(val)) for key, val in performances.items()
        ]
        results = sorted(results, key=lambda x: x[1])

        # Report.
        focus("\"ID #Samplers #Batchers #GPUQueue Time Cost\".")
        focus("\"-- --------- --------- --------- ---------\".")
        for i, ((num_samplers, num_batchers, qmax_remotes), cost) in enumerate(
            results,
        ):
            focus(
                "\"{:s} {:s} {:s} {:s} {:s}\".",
                "{:d}".format(i + 1).rjust(2),
                "{:d}".format(num_samplers).rjust(9),
                "{:d}".format(num_batchers).rjust(9),
                "{:d}".format(qmax_remotes).rjust(9),
                "{:f}".format(cost)[0:9].rjust(9),
            )