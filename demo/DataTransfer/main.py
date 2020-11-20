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
from demo.DataTransfer.benchmark import TransferBenchmark


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main Branch >>
# Main brank starts here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


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
        dtype="float32",
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
    batch_transform = WasteTransform(5, 0, True, True, False)
    model_transform = WasteTransform(10, 0, True, True, True)
    info1("Transforms are ready.")

    # Run benchmark on given case.
    TransferBenchmark(
        dat, ConstShuffleBatch,
        sample_transform, batch_stackform, batch_transform, model_transform,
        [
            (0, 0, 1),
            (0, 1, 1),
            (4, 0, 1),
            (4, 1, 1),
            (0, 0, 4),
            (0, 1, 4),
            (4, 0, 4),
            (4, 1, 4),
        ],
        10,
        xargs=(), xkargs=dict(
            batch_size=batch_size,
            tail=False,
        ),
    )


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main()
else:
    pass
