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
from demo.Reproduce.datasets.graph import GraphDataset
from pytorch.batches.shuffle import ConstShuffleBatch
from pytorch.reforms.transform import IdentityTransform
from pytorch.reforms.stackform import GraphStackform
from demo.Reproduce.models.gin import RepGIN, TarGIN
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

    # Generate a dataset.
    min_nodes = 10
    max_nodes = 15
    num_node_inputs = 7
    num_edge_inputs = 0
    num_node_outputs = 5
    er_p = 0.5
    dat = GraphDataset(
        "../FastDataset/Reproduce",
        pin={
            "graph": None,
        },
        dtype="float32",
    )
    dat.set(
        rng,
        xargs=(),
        xkargs=dict(
            min_nodes=min_nodes, max_nodes=max_nodes,
            num_node_inputs=num_node_inputs, num_edge_inputs=num_edge_inputs,
            num_node_outputs=num_node_outputs,
            er_p=er_p,
        ),
    )
    rngmem = rng.get_state()
    info1("Dataset is ready.")

    # Get a batching
    bat = ConstShuffleBatch()
    bat.set(
        dat, "cpu", rng,
        sample_transform=IdentityTransform(),
        batch_stackform=GraphStackform(
            ["node_input", "edge_input", "node_target"],
            vertex="node_input", adjacency="adj_input",
        ),
        batch_transform=IdentityTransform(),
        num_samplers=4, qmax_samples=4,
        num_batchers=1, qmax_batches=2,
        qmax_remotes=2,
        xargs=(), xkargs=dict(
            batch_size=max_nodes - min_nodes, tail=False,
        ),
    )
    info1("Batching is ready.")

    # Create and run the benchmark.
    BackwardBenchmark(
        bat, RepGIN, TarGIN,
        [
            (
                ("update.linear1.weight", [(0, 5), (0, 7)]),
                ("weight1", [(0, 5), (0, 7)]),
            ),
            (
                ("update.linear1.bias", [(0, 5)]),
                ("bias1", [(0, 5)]),
            ),
            (
                ("update.linear2.weight", [(0, 5), (0, 5)]),
                ("weight2", [(0, 5), (0, 5)]),
            ),
            (
                ("update.linear2.bias", [(0, 5)]),
                ("bias2", [(0, 5)]),
            ),
        ],
        iokeys=dict(
            gin_graph=(
                ["node_input", "adj_input", "edge_input"],
                [],
            ),
            gin_msg=(
                ["node_input.src"],
                ["msg"],
            ),
            gin_agg=(
                ["node_input", "msg", "adj_input"],
                ["agg"],
            ),
            gin=(
                ["node_input", "agg"],
                ["node_output"],
            ),
        ),
        set_xargs=(),
        set_xkargs=dict(
            num_inputs=num_node_inputs, num_outputs=num_node_outputs,
            keep=dict(
                node_input_dst=False,
                edge_input=False,
                node_input_src=True,
            ),
        ),
        ini_xargs=(),
        ini_xkargs=dict(
            bilin=dict(
                xargs=(),
                xkargs=dict(
                    activation="relu", negative_slope=0,
                ),
            ),
        ),
    )


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main()
else:
    pass
