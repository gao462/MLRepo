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
from demo.Reproduce.models.gru import RepGRU, TarGRU
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
    *args: ArgT,
    **kargs: KArgT,
) -> bool:
    r"""
    Main branch.

    Args
    ----
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
    linear_ihs: Dict[str, Linear]
    linear_hhs: Dict[str, Linear]

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
        dat, "cpu",
        sample_transform=IdentityTransform(),
        batch_stackform=SeqStackform(["input", "target"]),
        batch_transform=IdentityTransform(),
        num_samplers=4, qmax_samples=4,
        num_batchers=1, qmax_batches=2,
        qmax_remotes=2,
        xargs=(), xkargs=dict(
            batch_size=batch_size, tail=False,
        ),
    )
    info1("Batching is ready.")

    # Create gate and cell sub models.
    linear_ihs = {}
    linear_hhs = {}
    for section in ["reset", "update", "cell"]:
        # Create I-to-H sub model.
        ih = Linear(
            "../FastModel/Reproduce",
            sub=True, dtype="float32",
            iokeys={
                "linear": (["input"], ["agg_{:s}_i".format(section)]),
            },
        ).set(
            xargs=(), xkargs=dict(
                num_inputs=num_inputs, num_outputs=num_outputs, no_bias=False,
            ),
        )

        # Create H-to-H sub model.
        hh = Linear(
            "../FastModel/Reproduce",
            sub=True, dtype="float32",
            iokeys={
                "linear": (["hidden"], ["agg_{:s}_h".format(section)]),
            },
        ).set(
            xargs=(), xkargs=dict(
                num_inputs=num_outputs, num_outputs=num_outputs, no_bias=False,
            ),
        )

        # Save to dict.
        linear_ihs[section] = cast(Linear, ih)
        linear_hhs[section] = cast(Linear, hh)

    # Create and run the benchmark.
    benchmark = BackwardBenchmark(
        bat, RepGRU, TarGRU,
        [
            (
                ("reset_isub.weight", [(0, 5), (0, 7)]),
                ("weight_ih", [(0, 5), (0, 7)]),
            ),
            (
                ("reset_isub.bias", [(0, 5)]),
                ("bias_ih", [(0, 5)]),
            ),
            (
                ("reset_hsub.weight", [(0, 5), (0, 5)]),
                ("weight_hh", [(0, 5), (0, 5)]),
            ),
            (
                ("reset_hsub.bias", [(0, 5)]),
                ("bias_hh", [(0, 5)]),
            ),
            (
                ("update_isub.weight", [(0, 5), (0, 7)]),
                ("weight_ih", [(5, 10), (0, 7)]),
            ),
            (
                ("update_isub.bias", [(0, 5)]),
                ("bias_ih", [(5, 10)]),
            ),
            (
                ("update_hsub.weight", [(0, 5), (0, 5)]),
                ("weight_hh", [(5, 10), (0, 5)]),
            ),
            (
                ("update_hsub.bias", [(0, 5)]),
                ("bias_hh", [(5, 10)]),
            ),
            (
                ("cell_isub.weight", [(0, 5), (0, 7)]),
                ("weight_ih", [(10, 15), (0, 7)]),
            ),
            (
                ("cell_isub.bias", [(0, 5)]),
                ("bias_ih", [(10, 15)]),
            ),
            (
                ("cell_hsub.weight", [(0, 5), (0, 5)]),
                ("weight_hh", [(10, 15), (0, 5)]),
            ),
            (
                ("cell_hsub.bias", [(0, 5)]),
                ("bias_hh", [(10, 15)]),
            ),
        ],
        iokeys=dict(
            gru_reset_agg=(["agg_reset_i", "agg_reset_h"], ["reset"]),
            gru_update_agg=(["agg_update_i", "agg_update_h"], ["update"]),
            gru_cell_agg=(["agg_cell_i", "reset", "agg_cell_h"], ["cell"]),
            gru_aggregate=(["update", "hidden", "cell"], ["hidden"]),
            gru=(["hidden"], ["output"]),
        ),
        set_xargs=(),
        set_xkargs=dict(
            reset_isub=linear_ihs["reset"],
            reset_hsub=linear_hhs["reset"],
            update_isub=linear_ihs["update"],
            update_hsub=linear_hhs["update"],
            cell_isub=linear_ihs["cell"],
            cell_hsub=linear_hhs["cell"],
            num_inputs=num_inputs, num_outputs=num_outputs, no_bias=False,
        ),
        ini_xargs=(),
        ini_xkargs={
            "gate": dict(
                xargs=(),
                xkargs=dict(
                    activation="sigmoid", negative_slope=0,
                ),
            ),
            "cell": dict(
                xargs=(),
                xkargs=dict(
                    activation="tanh", negative_slope=0,
                ),
            ),
        },
    )
    return benchmark.accept


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main()
else:
    pass
