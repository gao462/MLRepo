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

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from pytorch.transforms.transform import BatchTransform


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transform Stacking Objects >>
# Transforms that stacking a batch of tensors with the same keyword into a
# single tensor with the same keyword.
# It is still a list to list operation.
# It should compress a list of N dicts of K-dim tensors into a list of 1 dict
# of (K+1)-dim tensors.
# The first dimension is extended as batch dimension.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class StackBatchTransform(BatchTransform):
    r"""
    Data transform processing stacking tensors together in a tensor.
    """
    def __init__(
        self: StackBatchTransform,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Nothing is required.
        pass

    def call(
        self: StackBatchTransform,
        raw: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> List[Dict[str, torch.Tensor]]:
        r"""
        Call as function.

        Args
        ----
        - self
        - raw
            Raw data before processing.
        - *args
        - **kargs

        Returns
        -------
        - processed
            Processed data.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        processed: Dict[str, torch.Tensor]
        buf: List[torch.Tensor]

        # Concatenate given keywords.
        processed = {
            key: torch.stack([sample[key] for sample in raw])
            for key in raw[0].keys()
        }
        return [processed]
