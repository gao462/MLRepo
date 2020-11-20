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
import math

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
from pytorch.models.model import Parameter, ForwardFunction, NullFunction


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Node Update Gradient Model >>
# The node update gradient model.
# The model forward function $f$ accepts a old node feature $X$, and aggregated
# messages from all their neighbors $\overline{M}$, then update them together
# into new node feature $X'$.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Update(GradModel):
    r"""
    Node update.
    """
    # Define main flow name.
    main = "update"

    def __parse__(
        self: Update,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Parse computation IO keys.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        self.ky_input_v: str
        self.ky_agg: str
        self.ky_output: str

        # Fetch main input and output.
        (self.ky_input_v, self.ky_agg), (self.ky_output,) = (
            self.IOKEYS[self.main]
        )