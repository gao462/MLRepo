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
from torch_geometric.nn import GINConv # type: ignore

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
from pytorch.models.graph.update import Update
from pytorch.models.linear import Linear
from pytorch.models.graph.msgpass import MessagePass
from pytorch.models.graph.message import ConcatMessage
from pytorch.models.graph.aggregate import SumNeighborAgg


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << GIN Gradient Model >>
# The GIN gradient model.
# This is implementation of "Graph Isomorphism Network".
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GINUpdate(Update):
    r"""
    GIN update.
    """
    # Define main flow name.
    main = "gin_update"

    def __forward__(
        self: GINUpdate,
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

            # Get epsilon scaled update.
            eps = 0
            tensor = (1 + eps) * input[self.ky_input_v] + input[self.ky_agg]

            # Transfer it by dual linear
            transient = {self.ky_output: tensor}
            transient = self.linear1.forward(
                parameter.sub("linear1"), transient,
            )
            transient[self.ky_output] = getattr(torch.nn.functional, "relu")(
                transient[self.ky_output],
            )
            transient = self.linear2.forward(
                parameter.sub("linear2"), transient,
            )
            output = {self.ky_output: transient[self.ky_output]}
            return output

        # Return the function.
        return f

    def __nullin__(
        self: GINUpdate,
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

            # Get linear inputs applied on destination and aggregation.
            return {
                self.ky_input_v: self.linear1.nullin(device)[self.ky_output],
                self.ky_agg: self.linear1.nullin(device)[self.ky_output],
            }

        # Return the function.
        return null

    def __nullout__(
        self: GINUpdate,
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


            # Get linear input directly.
            return self.linear2.nullout(device)

        # Return the function.
        return null

    def configure(
        self: GINUpdate,
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
        ...

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]

        # Create dual linear layers.
        _, (key,) = self.IOKEYS["gin_update"]
        self.linear1 = Linear(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                linear=([key], [key]),
            )
        ).set(
            xargs=(),
            xkargs=dict(
                num_inputs=self.num_inputs, num_outputs=self.num_outputs,
                no_bias=False,
            ),
        )
        self.linear2 = Linear(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                linear=([key], [key]),
            )
        ).set(
            xargs=(),
            xkargs=dict(
                num_inputs=self.num_outputs, num_outputs=self.num_outputs,
                no_bias=False,
            ),
        )

    def __initialize__(
        self: GINUpdate,
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
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Initialize recursively.
        self.linear1.initialize(
            rng,
            xargs=xkargs["bilin"]["xargs"], xkargs=xkargs["bilin"]["xkargs"],
        )
        self.linear2.initialize(
            rng,
            xargs=xkargs["bilin"]["xargs"], xkargs=xkargs["bilin"]["xkargs"],
        )


class GIN(MessagePass):
    r"""
    GIN.
    """
    # Define main flow name.
    main = "gin"

    def __nullin__(
        self: GIN,
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

            # GIN has no null definition.
            raise NotImplementedError

        # Return the function.
        return null

    def __nullout__(
        self: GIN,
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

            # Get linear input directly.
            return self.update.nullout(device)

        # Return the function.
        return null

    def configure(
        self: GIN,
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
        ...

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]

        # Create message layers.
        self.message = ConcatMessage(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                concat_msg=self.IOKEYS["{:s}_msg".format(self.main)],
            )
        ).set(xargs=(), xkargs=dict())

        # Create aggregation layers.
        self.aggregate = SumNeighborAgg(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                sum_neighbor_agg=self.IOKEYS["{:s}_agg".format(self.main)],
            )
        ).set(xargs=(), xkargs=dict())

        # Create update layers.
        self.update = GINUpdate(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                gin_update=self.IOKEYS[self.main],
            )
        ).set(
            xargs=(),
            xkargs=dict(
                num_inputs=self.num_inputs, num_outputs=self.num_outputs,
            ),
        )

    def __initialize__(
        self: GIN,
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
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Initialize recursively.
        self.message.initialize(rng, xargs=xargs, xkargs=xkargs)
        self.aggregate.initialize(rng, xargs=xargs, xkargs=xkargs)
        self.update.initialize(rng, xargs=xargs, xkargs=xkargs)


class __GIN__(GIN):
    r"""
    PyTorch GIN.
    """
    def __forward__(
        self: __GIN__,
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

            # Compute directly.
            output = {}
            output[self.ky_output] = self.pytorch.forward(
                input[self.ky_input_v], input[self.ky_adj],
            )
            return output

        # Return the function.
        return f

    def configure(
        self: __GIN__,
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
        ...

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]

        # Super.
        GIN.configure(self, xargs, xkargs)

        # Allocate parameters.
        self.pytorch = GINConv(
            torch.nn.Sequential(
                torch.nn.Linear(
                    in_features=self.num_inputs,
                    out_features=self.num_outputs,
                    bias=True,
                ),
                torch.nn.ReLU(),
                torch.nn.Linear(
                    in_features=self.num_outputs,
                    out_features=self.num_outputs,
                    bias=True,
                ),
            ),
            eps=0, train_eps=False,
        )
        self.weight1 = self.pytorch.nn[0].weight
        self.weight2 = self.pytorch.nn[2].weight
        self.bias1 = self.pytorch.nn[0].bias
        self.bias2 = self.pytorch.nn[2].bias

    def __initialize__(
        self: __GIN__,
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

        # Super.
        GIN.__initialize__(self, rng, xargs=xargs, xkargs=xkargs)

        # Copy data to correct place.
        self.update = cast(GINUpdate, self.update)
        self.weight1.data.copy_(cast(Linear, self.update.linear1).weight.data)
        self.weight2.data.copy_(cast(Linear, self.update.linear2).weight.data)
        self.bias1.data.copy_(cast(Linear, self.update.linear1).bias.data)
        self.bias2.data.copy_(cast(Linear, self.update.linear2).bias.data)

        # Remove from registration.
        del self.parameter.submodels["message"]
        del self.parameter.submodels["aggregate"]
        del self.parameter.submodels["update"]
        del self.message
        del self.aggregate
        del self.update