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
import abc
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


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transform Virtual Objects >>
# The virtual transform protoype to process a raw sample data in dataset or
# already-batched data in batching.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


# /
# GENERIC TYPES
# /
# Define generic process IO types.
DATA = TypeVar("DATA")


class Transform(Generic[DATA]):
    r"""
    Virtual class for data transform processing.
    """
    @abc.abstractmethod
    def __init__(
        self: Transform[DATA],
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
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def __call__(
        self: Transform[DATA],
        raw: DATA,
        *args: ArgT,
        **kargs: KArgT,
    ) -> DATA:
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
        # VIRTUAL
        # \
        ...


class SampleTransform(Transform[Dict[str, torch.Tensor]]):
    r"""
    Virtual class for data transform processing on sample level.
    """
    # Nothing is required.
    pass


class BatchTransform(Transform[Dict[str, List[torch.Tensor]]]):
    r"""
    Virtual class for data transform processing on sample level.
    """
    # Nothing is required.
    pass


class IdentitySampleTransform(SampleTransform):
    r"""
    Identity data transform processing on sample level.
    """
    def __init__(
        self: IdentitySampleTransform,
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

    def __call__(
        self: IdentitySampleTransform,
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
        # VIRTUAL
        # \
        ...

        # Return what it gets.
        return raw


class IdentityBatchTransform(BatchTransform):
    r"""
    Identity data transform processing on batch level.
    """
    def __init__(
        self: IdentityBatchTransform,
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

    def __call__(
        self: IdentityBatchTransform,
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
        # VIRTUAL
        # \
        ...

        # Return what it gets.
        return raw