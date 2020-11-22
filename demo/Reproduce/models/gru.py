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
from pytorch.models.model import LossFunction
from pytorch.models.seq.gru import GRU, __GRU__
from demo.Reproduce.models.naive import NaiveSeqDistLoss


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << GRU Gradient Model Naive Distribution >>
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class RepGRU(GRU):
    r"""
    Reproduced GRU.
    """
    def __train__(
        self: RepGRU,
        *args: ArgT,
        **kargs: KArgT,
    ) -> LossFunction:
        r"""
        Set training loss function.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - function
            Forward function.

        It must of defined a function $f$ by form:
        $$
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # return the function.
        return NaiveSeqDistLoss((["output"], ["target"]))

    def __evaluate__(
        self: RepGRU,
        *args: ArgT,
        **kargs: KArgT,
    ) -> LossFunction:
        r"""
        Set evaluating loss function.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - function
            Forward function.

        It must of defined a function $f$ by form:
        $$
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Return the function.
        return NaiveSeqDistLoss((["output"], ["target"]))


class TarGRU(__GRU__):
    r"""
    Target GRU.
    """
    def __train__(
        self: TarGRU,
        *args: ArgT,
        **kargs: KArgT,
    ) -> LossFunction:
        r"""
        Set training loss function.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - function
            Forward function.

        It must of defined a function $f$ by form:
        $$
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # return the function.
        return NaiveSeqDistLoss((["output"], ["target"]))

    def __evaluate__(
        self: TarGRU,
        *args: ArgT,
        **kargs: KArgT,
    ) -> LossFunction:
        r"""
        Set evaluating loss function.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - function
            Forward function.

        It must of defined a function $f$ by form:
        $$
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Return the function.
        return NaiveSeqDistLoss((["output"], ["target"]))