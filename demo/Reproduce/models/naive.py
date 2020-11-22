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
        keys: Tuple[List[str], List[str]],
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
        ...

        # Save necessary attributes.
        (self.ky_output,), (self.ky_target,) = keys

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
        ...

        # Get MSE.
        return ((output[self.ky_output] - target[self.ky_target]) ** 2).sum()


class NaiveSeqDistLoss(object):
    r"""
    Naive sequence distribution loss function.
    """
    def __init__(
        self: NaiveSeqDistLoss,
        dynamic_keys: Tuple[List[str], List[str]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - dynamic_keys
            Keys to compute dynamic loss.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Save necessary attributes.
        (self.ky_dynout,), (self.ky_dyntar,) = dynamic_keys

    def __call__(
        self: NaiveSeqDistLoss,
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
        buf: List[torch.Tensor]

        # Get static MSE.
        sample_length = int(target["$batch_length"].item())
        buf = []
        for t in range(sample_length):
            buf.append(((
                output["{:s}.{:d}".format(self.ky_dynout, t)] -
                target["{:s}.{:d}".format(self.ky_dyntar, t)]
            ) ** 2).sum())
        loss = cast(torch.Tensor, sum(buf))
        return loss


