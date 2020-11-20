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

        # Fetch all things to local level.
        (vexkey, adjkey, lnkkey), _ = (
            self.IOKEYS["{:s}_graph".format(self.main)]
        )
        (msg_dstkey, msg_lnkkey, msg_srckey), (msg_outkey,) = (
            self.IOKEYS["{:s}_msg".format(self.main)]
        )
        (agg_msgkey, agg_adjkey, agg_vexkey), (agg_outkey,) = (
            self.IOKEYS["{:s}_agg".format(self.main)]
        )
        (vexkey, aggkey), (outkey,) = self.IOKEYS[self.main]
        msg_forward = self.message.forward
        agg_forward = self.aggregate.forward
        update_forward = self.update.forward

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

            # Split input into exact graph info.
            adj_buf = input[adjkey]
            src_buf = input[vexkey][adj_buf[0]]
            dst_buf = input[vexkey][adj_buf[1]]
            lnk_buf = input[lnkkey]

            # Collect message for each edge.
            msg_buf = msg_forward(parameter.sub("message"), {
                msg_dstkey: dst_buf,
                msg_lnkkey: lnk_buf,
                msg_srckey: src_buf,
            })

            # Aggregate collected message for each node.
            agg_buf = agg_forward(parameter.sub("aggregate"), {
                agg_msgkey: msg_buf[agg_msgkey],
                agg_adjkey: adj_buf,
                agg_vexkey: input[agg_vexkey],
            })

            # Compute directly.
            output = {}
            update_buf = update_forward(parameter.sub("update"), {
                vexkey: input[vexkey],
                aggkey: agg_buf[aggkey],
            })
            output[outkey] = update_buf[outkey]
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
            raise NotImplementedError

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

        # Save necessary attributes.
        ...

        # Get models for message, aggregation and update.
        self.message = xkargs["message"]
        self.aggregate = xkargs["aggregate"]
        self.update = xkargs["update"]

    def __initialize__(
        self: MessagePass,
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
        self.message.initialize(
            rng,
            xargs=xkargs["message"]["xargs"],
            xkargs=xkargs["message"]["xkargs"],
        )
        self.aggregate.initialize(
            rng,
            xargs=xkargs["aggregate"]["xargs"],
            xkargs=xkargs["aggregate"]["xkargs"],
        )
        self.update.initialize(
            rng,
            xargs=xkargs["update"]["xargs"],
            xkargs=xkargs["update"]["xkargs"],
        )