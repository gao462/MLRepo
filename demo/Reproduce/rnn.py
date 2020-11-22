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
from demo.Reproduce.datasets.seq import SeqDataset
from pytorch.batches.shuffle import ConstShuffleBatch
from pytorch.reforms.transform import IdentityTransform
from pytorch.reforms.stackform import SeqStackform
from demo.Reproduce.models.rnn import RepRNN, TarRNN
from pytorch.models.linear import Linear
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
        Device
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
    sample_length = 3
    num_inputs = 7
    num_outputs = 5
    dat = SeqDataset(
        "../FastDataset/Reproduce",
        pin={
            "sequence": None,
        },
        dtype="float32",
    )
    dat.set(
        rngmem,
        xargs=(),
        xkargs=dict(
            num_samples=num_batches * batch_size,
            sample_length=sample_length, num_inputs=num_inputs,
            num_outputs=num_outputs,
        ),
    )
    info1("Dataset is ready.")

    # Get a batching
    bat = ConstShuffleBatch()
    bat.set(
        dat, device,
        sample_transform=IdentityTransform(),
        batch_stackform=SeqStackform([], ["input", "target"]),
        batch_transform=IdentityTransform(),
        num_samplers=4, qmax_samples=4,
        num_batchers=1, qmax_batches=2,
        qmax_remotes=2,
        xargs=(), xkargs=dict(
            batch_size=batch_size, tail=False,
        ),
    )
    info1("Batching is ready.")

    # Create I-to-H sub model.
    linear_ih = Linear(
        "../FastModel/Reproduce",
        sub=True, dtype="float32",
        iokeys={
            "linear": (["input"], ["agg_hidden_i"]),
        },
    ).set(
        device,
        xargs=(), xkargs=dict(
            num_inputs=num_inputs, num_outputs=num_outputs, no_bias=False,
        ),
    )

    # Create H-to-H sub model.
    linear_hh = Linear(
        "../FastModel/Reproduce",
        sub=True, dtype="float32",
        iokeys={
            "linear": (["hidden"], ["agg_hidden_h"]),
        },
    ).set(
        device,
        xargs=(), xkargs=dict(
            num_inputs=num_outputs, num_outputs=num_outputs, no_bias=False,
        ),
    )

    # Create and run the benchmark.
    benchmark = BackwardBenchmark(
        device, bat, RepRNN, TarRNN,
        [
            (
                ("isub.weight", [(0, 5), (0, 7)]),
                ("weight_ih", [(0, 5), (0, 7)]),
            ),
            (
                ("isub.bias", [(0, 5)]),
                ("bias_ih", [(0, 5)]),
            ),
            (
                ("hsub.weight", [(0, 5), (0, 5)]),
                ("weight_hh", [(0, 5), (0, 5)]),
            ),
            (
                ("hsub.bias", [(0, 5)]),
                ("bias_hh", [(0, 5)]),
            ),
        ],
        iokeys=dict(
            rnn_static=([], ["hidden"]),
            rnn_dynamic=(["input"], ["output"]),
            rnn_aggregate=(["agg_hidden_i", "agg_hidden_h"], ["hidden"]),
            rnn=(["hidden"], ["output"]),
        ),
        set_xargs=(),
        set_xkargs=dict(
            transform="tanh",
            isub=linear_ih, hsub=linear_hh,
            num_inputs=num_inputs, num_outputs=num_outputs, no_bias=False,
        ),
        ini_xargs=(),
        ini_xkargs=dict(
            activation="tanh", negative_slope=0,
        ),
    )
    return benchmark.accept


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main("cuda:0")
else:
    pass
