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
from demo.Reproduce.datasets.embedding import EmbeddingDataset
from pytorch.batches.shuffle import ConstShuffleBatch
from pytorch.reforms.transform import IdentityTransform
from pytorch.reforms.stackform import NaiveStackform
from demo.Reproduce.models.embedding import RepEmbedding, TarEmbedding
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
    num_embeddings = 3
    num_features = 5
    dat = EmbeddingDataset(
        "../FastDataset/Reproduce",
        pin={
            "embedding": None,
        },
        dtype="float32",
    )
    dat.set(
        rngmem,
        xargs=(),
        xkargs=dict(
            num_samples=num_batches * batch_size,
            num_embeddings=num_embeddings, num_features=num_features,
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
    benchmark = BackwardBenchmark(
        bat, RepEmbedding, TarEmbedding,
        [
            (
                ("embedding", [(0, 3), (0, 5)]),
                ("embedding", [(0, 3), (0, 5)]),
            ),
        ],
        iokeys=dict(
            embedding=(["input"], ["output"]),
        ),
        set_xargs=(),
        set_xkargs=dict(
            num_embeddings=num_embeddings, num_features=num_features,
        ),
        ini_xargs=(),
        ini_xkargs=dict(),
    )
    return benchmark.accept


# Main branch.
if (__name__ == '__main__'):
    # Update logging status and run.
    update_universal_logger(default_logger(__file__, LOGLV))
    main()
else:
    pass
