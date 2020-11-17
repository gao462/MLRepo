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
from pytorch.transforms.transform import SampleTransform
from pytorch.transforms.transform import BatchTransform


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transform Objects >>
# A transform processing meaningless operations.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class WasteSampleTransform(SampleTransform):
    r"""
    Meaningless data transform processing on samples.

    On samples, it is assumed that only simple operations such as add,
    substract, multiple and divide is adopted, for example, normalization.
    """
    def __init__(
        self: WasteSampleTransform,
        num: int, sec: float,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - num
            Number of repeating times.
        - sec
            Minimum seconds spending in this transform.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.NUM: Const = num
        self.SEC: Const = sec

    def __call__(
        self: WasteSampleTransform,
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

        # Do a bench of meaningless operations.
        start = time.time()
        mat = raw["input"]
        for _ in range(self.NUM):
            # Basic arithmetic.
            mat = mat * 5
            mat = mat + 2
            mat = mat - 3
            mat = mat / 4
            mmx = getattr(torch, "max")(mat)
            mmn = getattr(torch, "min")(mat)
            mat = (mat - mmn) / (mmx - mmn)
        end = time.time()
        elapsed = end - start

        # Sleep for enough time.
        time.sleep(max(self.SEC - elapsed, 0))
        return {"input": mat}


class WasteBatchTransform(BatchTransform):
    r"""
    Meaningless data transform processing on batches.

    On batches, it is assumed that operations including reshape, split,
    concatentation are adopted besides sample operations.
    """
    def __init__(
        self: WasteBatchTransform,
        num: int, sec: float,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - num
            Number of repeating times.
        - sec
            Minimum seconds spending in this transform.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.NUM: Const = num
        self.SEC: Const = sec

    def __call__(
        self: WasteBatchTransform,
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
        ...

        # Do a bench of meaningless operations.
        start = time.time()
        processed = []
        for sample in raw:
            mat = sample["input"]
            for _ in range(self.NUM):
                # Shape tricks.
                num_rows, num_cols = mat.size()
                mat = mat.view(num_cols, num_rows)
                buf = []
                for i in range(len(mat)):
                    buf.append(mat[i])
                mat = getattr(torch, "stack")(buf)
                mat = mat.view(num_rows, num_cols)

                # Basic arithmetic.
                mat = mat * 5
                mat = mat + 2
                mat = mat - 3
                mat = mat / 4
                mmx = getattr(torch, "max")(mat)
                mmn = getattr(torch, "min")(mat)
                mat = (mat - mmn) / (mmx - mmn)
            processed.append({"input": mat})
        end = time.time()
        elapsed = end - start

        # Sleep for enough time.
        time.sleep(max(self.SEC - elapsed, 0))
        return processed


class WasteModelTransform(BatchTransform):
    r"""
    Meaningless data transform processing on models.

    On models, besides operations on samples and batches, it also extends with
    matrix multiplication, element-wise multiplication, activation, and
    softmax.
    """
    def __init__(
        self: WasteModelTransform,
        num: int, sec: float,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - num
            Number of repeating times.
        - sec
            Minimum seconds spending in this transform.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.NUM: Const = num
        self.SEC: Const = sec

    def __call__(
        self: WasteModelTransform,
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
        ...

        # Do a bench of meaningless operations.
        start = time.time()
        processed = []
        for sample in raw:
            mat = sample["input"]
            for _ in range(self.NUM):
                # Matrix operations.
                dupl = mat
                dupr = mat.t()
                attn = getattr(torch, "mm")(dupl, dupr)
                attn = getattr(torch, "sigmoid")(attn)
                mat = attn * mat
                mat = getattr(torch, "softmax")(mat, dim=1)

                # Shape tricks.
                num_rows, num_cols = mat.size()
                mat = mat.view(num_cols, num_rows)
                buf = []
                for i in range(len(mat)):
                    buf.append(mat[i])
                mat = getattr(torch, "stack")(buf)
                mat = mat.view(num_rows, num_cols)

                # Basic arithmetic.
                mat = mat * 5
                mat = mat + 2
                mat = mat - 3
                mat = mat / 4
                mmx = getattr(torch, "max")(mat)
                mmn = getattr(torch, "min")(mat)
                mat = (mat - mmn) / (mmx - mmn)
            processed.append({"input": mat})
        end = time.time()
        elapsed = end - start

        # Sleep for enough time.
        time.sleep(max(self.SEC - elapsed, 0))
        return processed
