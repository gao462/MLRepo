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
from demo.Reproduce.models.linseq import RepLinearSeq, TarLinearSeq
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
    device: str,
    *args: ArgT,
    **kargs: KArgT,
) -> bool:
    r"""
    Main branch.

    Args
    ----
    - device
        Device.
    - *args
    - **kargs

    Returns
    -------
    - flag
        If True, the benchwork is accepted.

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
    rngmem = rng.get_state()
    info1("Dataset is ready.")

    # Get a batching
    bat = ConstShuffleBatch()
    bat.set(
        dat, device,
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
    benchmark = BackwardBenchmark(
        device, bat, RepLinearSeq, TarLinearSeq,
        [
            (
                ("seq.0.weight", [(0, 5), (0, 7)]),
                ("weight1", [(0, 5), (0, 7)]),
            ),
            (
                ("seq.0.bias", [(0, 5)]),
                ("bias1", [(0, 5)]),
            ),
            (
                ("seq.2.weight", [(0, 5), (0, 5)]),
                ("weight2", [(0, 5), (0, 5)]),
            ),
            (
                ("seq.2.bias", [(0, 5)]),
                ("bias2", [(0, 5)]),
            ),
        ],
        iokeys=dict(),
        set_xargs=(),
        set_xkargs=dict(
            num_inputs=num_inputs, num_outputs=num_outputs,
        ),
        ini_xargs=(
            dict(
                xargs=(),
                xkargs=dict(
                    activation="relu", negative_slope=0,
                ),
            ),
            dict(
                xargs=(),
                xkargs=dict(
                    activation="relu", negative_slope=0,
                ),
            )
        ),
        ini_xkargs=dict(),
    )
    return benchmark.accept


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main("cuda:0")
else:
    pass
