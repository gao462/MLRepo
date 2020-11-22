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
# << Message Passing Gradient Model >>
# The linear gradient model.
# The model forward function $f$ accepts a matrix of vecotr features $X$,
# directed link set $A$ and its corresponding edge features $E$.
#
# The function $f$ is applied on each node that
#
# $$
# m_{(i, j) \in A} = f_{\text{msg}} \left( X_{i}, E_{(i, j)}, X_{j} \right)
# \overline{m}_{i} = f_{\text{agg}} \left( \{ m_{(i, j) \in A} \} \right)
# y_{i} = f_{\text{update}} \left( X_{i}, \overline{m}_{i} \right)
# $$
#
# The parameter part is hidden for the ease of notation.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class MessagePass(GradModel):
    r"""
    Message Passing.
    """
    # Define main flow name.
    main = "msgpass"

    def __parse__(
        self: MessagePass,
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
        self.ky_adj: str
        self.ky_input_e: str
        self.ky_output_residuals: List[str]
        self.ky_input_src: str
        self.ky_input_dst: str
        self.ky_msg: str
        self.ky_agg: str
        self.ky_output: str

        # Fetch main input and output.
        (
            (self.ky_input_v, self.ky_adj, self.ky_input_e),
            self.ky_output_residuals,
        ) = self.IOKEYS["{:s}_graph".format(self.main)]
        self.ky_input_src = "{:s}.src".format(self.ky_input_v)
        self.ky_input_dst = "{:s}.dst".format(self.ky_input_v)
        (
            (self.ky_input_dst, self.ky_input_e, self.ky_input_src),
            (self.ky_msg,),
        ) = self.IOKEYS["{:s}_msg".format(self.main)]
        (self.ky_input_v, self.ky_msg, self.ky_adj), (self.ky_agg,) = (
            self.IOKEYS["{:s}_agg".format(self.main)]
        )
        (self.ky_input_v, self.ky_agg), (self.ky_output,) = (
            self.IOKEYS[self.main]
        )

        # Safety check.
        for ky_outres in self.ky_output_residuals:
            if (ky_outres in [self.ky_input_v, self.ky_adj, self.ky_input_e]):
                pass
            else:
                error(
                    "Graph residual key \"{:s}\" is not in graph input.",
                    ky_outres,
                )
                raise RuntimeError

    def __forward__(
        self: MessagePass,
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
            output: Dict[str, torch.Tensor]

            # Keep always-pass inputs.
            output = {}
            for key, tensor in input.items():
                if (key[0] == "$"):
                    output[key] = tensor
                else:
                    pass

            # Split input into exact graph info.
            transient = {}
            transient[self.ky_input_v] = input[self.ky_input_v]
            transient[self.ky_adj] = input[self.ky_adj]
            transient[self.ky_input_e] = input[self.ky_input_e]
            transient[self.ky_input_src] = transient[self.ky_input_v][
                transient[self.ky_adj][0]
            ]
            transient[self.ky_input_dst] = transient[self.ky_input_v][
                transient[self.ky_adj][1]
            ]

            # Collect message for each edge.
            transient[self.ky_msg] = self.message.forward(
                parameter.sub("message"), transient,
            )[self.ky_msg]

            # Aggregate collected message for each node.
            transient[self.ky_agg] = self.aggregate.forward(
                parameter.sub("aggregate"), transient,
            )[self.ky_agg]

            # Compute directly.
            output[self.ky_output] = self.update.forward(
                parameter.sub("update"), transient,
            )[self.ky_output]

            # Add residual-from-input outputs.
            for key in self.ky_output_residuals:
                output[key] = input[key]
            return output

        # Return the function.
        return f

    def __nullin__(
        self: MessagePass,
        *args: ArgT,
        **kargs: KArgT,
    ) -> NullFunction:
        r"""
        Generate null input.

        Args
        ----
        - self
        - *kargs
        - **kargs

        Returns
        -------
        - null
            Null input generation function.

        After setup, the null input to a model is fixed.
        This is helpful to understand the expectation of input.
        This is also useful when the default model output is required, for
        example, this is the sub model of RNN H-to-H model at the first time
        step.
        It has batch size 1 for robustness.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Fetch all things to local level.
        ...

        def null(
            device: str,
            *args: ArgT,
            **kargs: KArgT,
        ) -> Dict[str, torch.Tensor]:
            r"""
            Generate null input on device.

            Args
            ----
            - device
                Device.
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
            ...

            # return all-zero.
            raise NotImplementedError

        # Return the function.
        return null

    def __nullout__(
        self: MessagePass,
        *args: ArgT,
        **kargs: KArgT,
    ) -> NullFunction:
        r"""
        Generate null output.

        Args
        ----
        - self
        - *kargs
        - **kargs

        Returns
        -------
        - null
            Null output generation function.

        After setup, the null output to a model is fixed.
        This is helpful to understand the expectation of output.
        This is also useful when the default model output is required, for
        example, this is the sub model of RNN H-to-H model at the first time
        step.
        It has batch size 1 for robustness.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Fetch all things to local level.
        ...

        def null(
            device: str,
            *args: ArgT,
            **kargs: KArgT,
        ) -> Dict[str, torch.Tensor]:
            r"""
            Generate null output on device.

            Args
            ----
            - device
                Device.
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
            ...

            # return all-zero.
            return self.update.nullout(device)

        # Return the function.
        return null

    def configure(
        self: MessagePass,
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
        self.message: GradModel
        self.aggregate: GradModel
        self.update: GradModel

        # Get models for message, aggregation and update.
        self.message = xkargs["message"]
        self.aggregate = xkargs["aggregate"]
        self.update = xkargs["update"]

    def __initialize__(
        self: MessagePass,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize model parameters and sub models.

        Args
        ----
        - self
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
        self.message.initialize(
            self.rng.get_state(),
            xargs=xkargs["message"]["xargs"],
            xkargs=xkargs["message"]["xkargs"],
        )
        self.aggregate.initialize(
            self.rng.get_state(),
            xargs=xkargs["aggregate"]["xargs"],
            xkargs=xkargs["aggregate"]["xkargs"],
        )
        self.update.initialize(
            self.rng.get_state(),
            xargs=xkargs["update"]["xargs"],
            xkargs=xkargs["update"]["xkargs"],
        )