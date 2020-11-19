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
from pytorch.models.model import Parameter


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Naive Distribution Loss Function >>
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class NaiveDistLoss(object):
    r"""
    Naive distribution loss function.
    """
    def __init__(
        self: NaiveDistLoss,
        iokeys: Tuple[List[str], List[str]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - keys
            Keys to compute loss.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.IOKEYS: Const = iokeys

    def __call__(
        self: NaiveDistLoss,
        parameter: Parameter,
        output: Dict[str, torch.Tensor],
        target: Dict[str, torch.Tensor],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Call as function.

        Args
        ----
        - self
        - parameter
            Parameter.
        - output
            Output.
        - target
            Target.
        - *args
        - **kargs

        Returns
        -------
        - loss
            Evaluating loss.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        loss: torch.Tensor

        # Get MSE.
        (inkey,), (outkey,) = self.IOKEYS
        return ((output[inkey] - target[outkey]) ** 2).sum()


