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
from pytorch.models.model import GradModel


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Recurrent Gradient Model >>
# The recurrent gradient model.
# The model forward function $f$ must be described as:
# $$
# h_{t + 1} = f(x_{t + 1}, h_{t})
# $$
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GRU(GradModel):
    r"""
    GRU Model.
    """
    def configure(
        self: GRU,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Configure model.

        Args
        ----
        - self
        - xargs
            Extra arguments to specific configuration.
        - xkargs
            Extra keyword arguments to specific configuration.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # VIRTUAL
        # \
        ...

    def initialize(
        self: GradModel,
        rng: torch._C.Generator,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize model parameters and sub models.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # VIRTUAL
        # /
        ...

    def decode(
        self: GRU,
        batch: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> MultiReturn[
        List[Dict[str, torch.Tensor]], List[Dict[str, torch.Tensor]]
    ]:
        r"""
        Decode batch.

        Args
        ----
        - self
        - batch
            Batch.
        - *args
        - **kargs

        Returns
        -------
        - input
            Batch with input parts only.
        - target
            Batch with target parts only.

        """
        # /
        # VIRTUAL
        # /
        ...