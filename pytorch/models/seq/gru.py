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
from pytorch.models.model import ForwardFunction, Parameter
from pytorch.models.seq.rnn import RNN


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << GRU Gradient Model >>
# The GRU gradient model.
# The model forward function $f$ must be described as:
#
# $$
# r_{t + 1} = f_{\text{reset}} \left(
#     \theta_{\text{reset}}, x_{t + 1}, h_{t}
# \right)
# u_{t + 1} = f_{\text{update}} \left(
#     \theta_{\text{update}}, x_{t + 1}, h_{t}
# \right)
# c_{t + 1} = f_{\text{cell}} \left(
#     \theta_{\text{cell}}, x_{t + 1}, h_{t}, r_{t + 1}
# \right)
# h_{t + 1} = f_{\text{output}} \left(
#     \theta_{\text{output}}, x_{t + 1}, h_{t}, u_{t + 1}
# \right)
# $$
#
# where inputs are $x_{t + 1}$ and $h_{t}$, output is $y = h_{t + 1}$.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GRU(GradModel):
    r"""
    GRU.
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
        # ANNOTATE VARIABLES
        # \
        self.reset_sub: RNN
        self.update_sub: RNN
        self.cell_isub: GradModel
        self.cell_hsub: GradModel

        # Get gate models.
        self.reset_sub = xkargs["reset_sub"]
        self.update_sub = xkargs["update_sub"]

        # Get cell models.
        self.cell_isub = xkargs["cell_isub"]
        self.cell_hsub = xkargs["cell_hsub"]

    def initialize(
        self: GRU,
        rng: torch._C.Generator,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize model parameters and sub models.

        Args
        ----
        - self
        - rng
            Random number generator.
        - *args
        - xargs
            Extra arguments to specific initialization.
        - xkargs
            Extra keyword arguments to specific initialization.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Initialize recursively.
        self.reset_sub.initialize(
            rng, xargs=xkargs["gate"], xkargs=xkargs["gate"],
        )
        self.update_sub.initialize(
            rng, xargs=xkargs["gate"], xkargs=xkargs["gate"],
        )
        self.cell_isub.initialize(
            rng, xargs=xkargs["isub"], xkargs=xkargs["hsub"],
        )
        self.cell_hsub.initialize(
            rng, xargs=xkargs["isub"], xkargs=xkargs["hsub"],
        )

    def set_forward(
        self: GRU,
        *args: ArgT,
        **kargs: KArgT,
    ) -> ForwardFunction:
        r"""
        Set forward function.

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
        y = f(\theta, x)
        $$

        where $y$ is output, $\theta$ is parameter and $x$ is input.

        In GRU, the function $f$ is further abstracted into four steps:
        $$
        r_{t + 1} = f_{\text{reset}} \left(
            \theta_{\text{reset}}, x_{t + 1}, h_{t}
        \right)
        u_{t + 1} = f_{\text{update}} \left(
            \theta_{\text{update}}, x_{t + 1}, h_{t}
        \right)
        c_{t + 1} = f_{\text{cell}} \left(
            \theta_{\text{cell}}, x_{t + 1}, h_{t}, r_{t + 1}
        \right)
        h_{t + 1} = f_{\text{output}} \left(
            \theta_{\text{output}}, x_{t + 1}, h_{t}, u_{t + 1}
        \right)
        $$

        where $f_{\text{reset}}$ and $f_{\text{update}}$ are gate forward
        functions.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        def f(
            parameter: Parameter,
            input: Dict[str, torch.Tensor],
            *args: ArgT,
            **kargs: KArgT,
        ) -> Dict[str, torch.Tensor]:
            r"""
            Forward a batch input.

            Args
            ----
            - parameter
                Parameter.
            - input
                Input.
            - *args
            - **kargs

            Returns
            -------
            - output
                Output.

            """
            # /
            # ANNOTATE VARIABLES
            # /
            cell: Dict[str, torch.Tensor]
            output: Dict[str, torch.Tensor]

            # Get reset gate.
            rgate = self.reset_sub.forward(parameter.sub("reset_sub"), input)

            # Get update gate.
            ugate = self.update_sub.forward(
                parameter.sub("update_sub"), input,
            )

            # Get cell state.
            xbuf = self.cell_isub.forward(parameter.sub("cell_isub"), input)
            hbuf = self.cell_hsub.forward(parameter.sub("cell_hsub"), input)
            cell = {}
            transform = getattr(torch, "tanh")
            (inkey,), (outkey,) = self.IOKEYS["cell"]
            cell[outkey] = (xbuf[inkey] + rgate[inkey] * hbuf[inkey])

            # Get output.
            output = {}
            (inkey,), (outkey,) = self.IOKEYS["output"]
            output[outkey] = (
                ugate[inkey] * input[inkey] + (1 - ugate[inkey]) * cell[inkey]
            )
            return output

        # Return the function.
        return f