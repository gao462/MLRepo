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
from pytorch.logging import update_universal_logger, default_logger
from pytorch.logging import INFO1 as LOGLV
from demo.DataTransfer.datasets.waste import WasteDataset
from pytorch.reforms.stackform import NaiveStackform
from demo.DataTransfer.transforms.waste import WasteTransform
from pytorch.batches.shuffle import ConstShuffleBatch


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main Branch >>
# Main brank starts here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Benchmark(object):
    r"""
    Benchmark as a function.
    """
    def __init__(
        self: Benchmark,
        dataset: WasteDataset, device: str,
        sample_transform: WasteTransform,
        batch_stackform: NaiveStackform, batch_transform: WasteTransform,
        model_transform: WasteTransform,
        *args: ArgT,
        num_samplers: int, qmax_samples: int,
        num_batchers: int, qmax_batches: int,
        qmax_remotes: int,
        rng: torch._C.Generator, batch_size: int,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - dataset
            Dataset.
        - device
            Device.
        - rng
            Random generator.
        - sample_transform
            Sample transform.
        - batch_stackform
            Batch stackform.
        - batch_transform
            Batch transform.
        - model_transform
            Model transform.
        - *args
        - num_samplers
            Number of samplers.
        - qmax_batches
            Queue maximum size for samples.
        - num_batchers
            Number of batchers.
        - qmax_batches
            Queue maximum size for batches.
        - qmax_remotes
            Number of remote slots.
        - rng
            Random generator.
        - batch_size
            Batch size
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Save random dataset and schedule.
        self.dataset = dataset
        self.device = device

        # Get transforms.
        self.sample_transform = sample_transform
        self.batch_stackform = batch_stackform
        self.batch_transform = batch_transform
        self.model_transform = model_transform

        # Get batching
        self.bat = ConstShuffleBatch()
        self.bat.set(
            self.dataset, self.device,
            sample_transform=self.sample_transform,
            batch_stackform=self.batch_stackform,
            batch_transform=self.batch_transform,
            num_samplers=num_samplers, qmax_samples=qmax_samples,
            num_batchers=num_batchers, qmax_batches=qmax_batches,
            qmax_remotes=qmax_remotes,
            xargs=(rng,), xkargs=dict(
                batch_size=batch_size, tail=False,
            ),
        )
        self.bat.refresh(xargs=(), xkargs={})

    def __call__(
        self: Benchmark,
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
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Traverse an epoch.
        while (True):
            # Fetch a batch.
            signal, batch = self.bat.next()

            # Process fetched batch.
            debug("\"\033[34;1mCompute\033[0m\".")
            self.model_transform(batch)
            debug("\"\033[32;1mDone\033[0m\".")

            # Stop on ending signal.
            if (signal):
                break
            else:
                pass


def main(
    *args: ArgT,
    **kargs: KArgT,
) -> None:
    r"""
    Main branch.

    Args
    ----
    - *args
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

    # Get dataset.
    batch_size = 16
    num_batches = 16
    dat = WasteDataset(
        "../FastDataset/DataTransfer",
        pin={
            "waste": None,
        },
        dtype="float64",
    )
    dat.set(
        xargs=(rng,),
        xkargs=dict(
            num_samples=num_batches * batch_size,
            sample_size=128,
        ),
    )
    rngmem = rng.get_state()
    info1("Datasets are ready.")

    # Get simulation transforms.
    sample_transform = WasteTransform(1, 0, True, False, False)
    batch_stackform = NaiveStackform(["input"])
    batch_transform = WasteTransform(10, 0, True, True, True)
    model_transform = WasteTransform(10, 0, True, True, True)
    info1("Transforms are ready.")

    # Collect performances.
    import os
    performances = {
        (0, 0, 1): [],
        (0, 1, 1): [],
        (4, 0, 1): [],
        (4, 1, 1): [],
        (0, 0, 4): [],
        (0, 1, 4): [],
        (4, 0, 4): [],
        (4, 1, 4): [],
    }
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
            rng.set_state(rngmem)
            benchmark = Benchmark(
                dat, "cpu",
                sample_transform, batch_stackform, batch_transform,
                model_transform,
                num_samplers=num_samplers, qmax_samples=4,
                num_batchers=num_batchers, qmax_batches=4,
                qmax_remotes=qmax_remotes,
                rng=rng, batch_size=batch_size,
            )
            start = time.time()
            benchmark()
            end = time.time()
            elapsed = end - start
            performances[
                (num_samplers, num_batchers, qmax_remotes)
            ].append(elapsed)
    results = [(key, sum(val) / len(val)) for key, val in performances.items()]
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


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main()
else:
    pass
