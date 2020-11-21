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
from pytorch.logging import DEBUG as LOGLV
from demo.Reproduce.datasets.vec import VectorDataset
from pytorch.batches.shuffle import ConstShuffleBatch
from pytorch.reforms.transform import IdentityTransform
from pytorch.reforms.stackform import NaiveStackform
from demo.Reproduce.models.linear import RepLinear, TarLinear
from demo.Reproduce.benchmark import BackwardBenchmark


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
    ...

    # Get randomness
    seed = 47
    rng = getattr(torch, "Generator")()
    rng.manual_seed(47)

    # Update randomness.
    rngmem = rng.get_state()

    # Generate a dataset.
    num_batches = 1
    batch_size = 4
    num_inputs = 7
    num_outputs = 5
    dat = VectorDataset(
        "../FastDataset/Reproduce",
        pin={
            "vector": None,
        },
        dtype="float32",
    )
    dat.set(
        rngmem,
        xargs=(),
        xkargs=dict(
            num_samples=num_batches * batch_size,
            num_inputs=num_inputs, num_outputs=num_outputs,
        ),
    )
    info1("Dataset is ready.")

    # Get a batching
    bat = ConstShuffleBatch()
    bat.set(
        dat, "cpu",
        sample_transform=IdentityTransform(),
        batch_stackform=NaiveStackform(["input", "target"]),
        batch_transform=IdentityTransform(),
        num_samplers=4, qmax_samples=4,
        num_batchers=1, qmax_batches=2,
        qmax_remotes=2,
        xargs=(), xkargs=dict(
            batch_size=batch_size, tail=False,
        ),
    )
    info1("Batching is ready.")

    # Create and run the benchmark.
    BackwardBenchmark(
        bat, RepLinear, TarLinear,
        [
            (
                ("weight", [(0, 5), (0, 7)]),
                ("weight", [(0, 5), (0, 7)]),
            ),
            (
                ("bias", [(0, 5)]),
                ("bias", [(0, 5)]),
            ),
        ],
        iokeys=dict(
            linear=(["input"], ["output"]),
        ),
        set_xargs=(),
        set_xkargs=dict(
            num_inputs=num_inputs, num_outputs=num_outputs, no_bias=False,
        ),
        ini_xargs=(),
        ini_xkargs=dict(
            activation="relu", negative_slope=0,
        ),
    )


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main()
else:
    pass
