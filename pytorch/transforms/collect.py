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
from pytorch.transforms.transform import SampleTransform
from pytorch.transforms.transform import BatchTransform


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transform Collection Objects >>
# Transforms that are collections of transforms.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class SampleTransformSeq(SampleTransform):
    r"""
    A sequence of data transform processing on sample level.
    """
    def __init__(
        self: SampleTransformSeq,
        transforms: List[SampleTransform],
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
        # Save necessary attributes.
        self.TRANSFORMS: Const = transforms

    def __call__(
        self: SampleTransformSeq,
        raw: Dict[str, torch.Tensor],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
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
        ...

        # Process in order.
        processed = raw
        for transform in self.TRANSFORMS:
            processed = transform(processed)
        return processed


class BatchTransformSeq(BatchTransform):
    r"""
    A sequence of data transform processing on batch level.
    """
    def __init__(
        self: BatchTransformSeq,
        transforms: List[BatchTransform],
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
        # Save necessary attributes.
        self.TRANSFORMS: Const = transforms

    def __call__(
        self: BatchTransformSeq,
        raw: Dict[str, List[torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, List[torch.Tensor]]:
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
        ...

        # Process in order.
        processed = raw
        for transform in self.TRANSFORMS:
            processed = transform(processed)
        return processed
