# Import future.
from __future__ import annotations

# Import typing.
from typing import Any as VarArg
from typing import Final as Const
from typing import Tuple as MultiReturn
from typing import Type, Protocol
from typing import TextIO, BinaryIO
from typing import Union, Tuple, List, Dict, Set, Callable

# Import dependencies.
import sys
import os
import torch

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from demo.DataTransfer.datasets.waste import WasteDataset


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Main Branch >>
# Main brank starts here.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# Get dataset.
seed = 47
rng = getattr(torch, "Generator")()
rng.manual_seed(47)
dat = WasteDataset(
    "../FastIO/DataTransfer",
    pin={
        "waste": "f3d3157ef66371de70229528e7628a40",
    },
    dtype="float64",
)
dat.set(config={
    "rng": rng,
    "num_samples": 128,
    "num_inputs": 128,
})

print(dat.memory[0]["input"].size())