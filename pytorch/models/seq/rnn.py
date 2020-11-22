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
from pytorch.models.linear import Linear
from pytorch.models.join import AddJoin
from pytorch.models.activation import Activation


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Recurrent Gradient Model >>
# The recurrent gradient model.
# The model forward function $f$ must be described as:
#
# $$
# y = f \left(
#     f_{\text{input}} \left(
#         \theta_{\text{input}}, x_{\text{input}},
#     \right) + f_{\text{hidden}} \left(
#         \theta_{\text{hidden}}, x_{\text{hidden}},
#     \right)
# \right)
# $$
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class RNN(GradModel):
    r"""
    RNN.
    """
    # Define main flow name.
    main = "rnn"

    def __parse__(
        self: RNN,
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
        self.ky_stains: List[str]
        self.ky_staouts: List[str]
        self.ky_dynins: List[str]
        self.ky_dynouts: List[str]
        self.ky_aggin_i: str
        self.ky_aggin_h: str
        self.ky_aggout: str
        self.ky_output: str

        # Fetch main input and output.
        self.ky_stains, self.ky_staouts = (
            self.IOKEYS["{:s}_static".format(self.main)]
        )
        self.ky_dynins, self.ky_dynouts = (
            self.IOKEYS["{:s}_dynamic".format(self.main)]
        )
        (self.ky_aggin_i, self.ky_aggin_h), (self.ky_aggout,) = (
            self.IOKEYS["{:s}_aggregate".format(self.main)]
        )
        (self.ky_aggout,), (self.ky_output,) = self.IOKEYS[self.main]

    def __forward__(
        self: RNN,
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

        In RNN, the function $f$ is further abstracted into:

        $$
        y = f \left(
            f_{\text{input}} \left(
                \theta_{\text{input}}, x_{\text{input}},
            \right) + f_{\text{hidden}} \left(
                \theta_{\text{hidden}}, x_{\text{hidden}},
            \right)
        \right)
        $$

        where $f_{\text{input}}$ and $f_{\text{hidden}}$ are sub models for raw
        input and hidden state, $f$ is the aggregation transform function.
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
            Get a gate.

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

            # Get essential sequence info.
            sample_length = cast(int, input["$batch_length"].item())
            batch_size = cast(int,input["$batch_size"].item())

            # Get essential recurrent transient buffer and expand batch
            # dimension by batch size.
            transient = {}
            tensor = self.hsub.nullout(self.device)[self.ky_aggin_h]
            shape = list(tensor.size())[1:]
            transient[self.ky_aggout] = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                # Put current static and dynamic inputs into transient buffer.
                for key in self.ky_stains:
                    transient[key] = input[key]
                for key in self.ky_dynins:
                    transient[key] = input["{:s}.{:d}".format(key, t)]

                # Join raw input and hidden state input.
                buf = {}
                buf.update(
                    self.isub.forward(parameter.sub("isub"), transient),
                )
                buf.update(
                    self.hsub.forward(parameter.sub("hsub"), transient),
                )
                buf.update(
                    self.join.forward(parameter.sub("join"), buf),
                )
                transient.update(
                    self.act.forward(parameter.sub("act"), buf),
                )

                # Get dynamic output.
                transient["{:s}.{:d}".format(self.ky_output, t)] = (
                    transient[self.ky_aggout]
                )

            # Fetch static and dynamic outputs.
            for key in self.ky_staouts:
                output[key] = transient[key]
            for t in range(sample_length):
                for key in self.ky_dynouts:
                    output["{:s}.{:d}".format(key, t)] = (
                        transient["{:s}.{:d}".format(key, t)]
                    )
            return output

        # Return the function.
        return f

    def __nullin__(
        self: RNN,
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

        It also assumes sequence length 1 for robustness.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        def null(
            *args: ArgT,
            **kargs: KArgT,
        ) -> Dict[str, torch.Tensor]:
            r"""
            Generate null input on device.

            Args
            ----
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

            # Get sub model inputs.
            output = {}
            output.update(self.isub.nullin())
            output.update(self.hsub.nullin())
            return output

        # Return the function.
        return null

    def __nullout__(
        self: RNN,
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

        It also assumes sequence length 1 for robustness.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        def null(
            *args: ArgT,
            **kargs: KArgT,
        ) -> Dict[str, torch.Tensor]:
            r"""
            Generate null output on device.

            Args
            ----
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

            # Get sub model outputs.
            output = self.hsub.nullout()
            return output

        # Return the function.
        return null

    def configure(
        self: RNN,
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
        self.isub: GradModel
        self.hsub: GradModel
        self.join: GradModel
        self.act: GradModel

        # Get models for raw input and hidden state.
        self.isub = xkargs["isub"]
        self.hsub = xkargs["hsub"]

        # Get model aggregation transform.
        self.transform_name = xkargs["transform"]
        self.join = AddJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                add_join_residuals=([], []),
                add_join=(
                    [self.ky_aggin_i, self.ky_aggin_h],
                    [self.ky_aggout],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())
        self.act = Activation(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                act_residuals=([], []),
                act=([self.ky_aggout], [self.ky_aggout]),
            ),
        ).set(
            self.device, xargs=(), xkargs=dict(activation=self.transform_name),
        )

    def __initialize__(
        self: RNN,
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
        self.isub.initialize(self.rng.get_state(), xargs=xargs, xkargs=xkargs)
        self.hsub.initialize(self.rng.get_state(), xargs=xargs, xkargs=xkargs)


class __RNN__(RNN):
    r"""
    PyTorch RNN.
    """
    def __forward__(
        self: __RNN__,
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

        In RNN, the function $f$ is further abstracted into:

        $$
        y = f \left(
            f_{\text{input}} \left(
                \theta_{\text{input}}, x_{\text{input}},
            \right) + f_{\text{hidden}} \left(
                \theta_{\text{hidden}}, x_{\text{hidden}},
            \right)
        \right)
        $$

        where $f_{\text{input}}$ and $f_{\text{hidden}}$ are sub models for raw
        input and hidden state, $f$ is the aggregation transform function.
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

            # Get essential sequence info.
            sample_length = cast(int, input["$batch_length"].item())
            batch_size = cast(int,input["$batch_size"].item())

            # Get essential recurrent transient buffer and expand batch
            # dimension by batch size.
            transient = {}
            tensor = self.hsub_nullout(self.device)[self.ky_aggin_h]
            shape = list(tensor.size())[1:]
            transient[self.ky_aggout] = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                # Inputs are fixed.
                transient[self.ky_aggout] = self.pytorch.forward(
                    input["{:s}.{:d}".format(self.ky_input_i, t)],
                    transient[self.ky_aggout],
                )

                # Get dynamic output.
                transient["{:s}.{:d}".format(self.ky_output, t)] = (
                    transient[self.ky_aggout]
                )

            # Fetch static and dynamic outputs.
            for key in self.ky_staouts:
                output[key] = transient[key]
            for t in range(sample_length):
                for key in self.ky_dynouts:
                    output["{:s}.{:d}".format(key, t)] = (
                        transient["{:s}.{:d}".format(key, t)]
                    )
            return output

        # Return the function.
        return f

    def configure(
        self: __RNN__,
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
        self.weight_ih: torch.nn.parameter.Parameter
        self.weight_hh: torch.nn.parameter.Parameter
        self.bias_ih: torch.nn.parameter.Parameter
        self.bias_hh: torch.nn.parameter.Parameter

        # Super.
        RNN.configure(self, xargs, xkargs)

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]
        self.no_bias = xkargs["no_bias"]

        # Allocate parameters.
        self.pytorch = torch.nn.RNNCell(
            input_size=self.num_inputs, hidden_size=self.num_outputs,
            bias=not self.no_bias, nonlinearity=self.transform_name,
        ).to(self.device)
        self.weight_ih = getattr(self.pytorch, "weight_ih")
        self.weight_hh = getattr(self.pytorch, "weight_hh")
        self.bias_ih = getattr(self.pytorch, "bias_ih")
        self.bias_hh = getattr(self.pytorch, "bias_hh")

        # Temporarily save sub models for initialization consistency.
        self.isub = xkargs["isub"]
        self.hsub = xkargs["hsub"]

        # Pre-fetch IO direction for consistency.
        (self.ky_input_i,), (_,) = self.isub.IOKEYS["linear"]

        # Pre-fetch null function for consistency.
        self.hsub_nullout = self.hsub.nullout

    def __initialize__(
        self: __RNN__,
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

        # Super.
        RNN.__initialize__(self, xargs=xargs, xkargs=xkargs)

        # Copy data to correct place.
        self.weight_ih.data.copy_(cast(Linear, self.isub).weight.data)
        self.weight_hh.data.copy_(cast(Linear, self.hsub).weight.data)
        if (self.no_bias):
            pass
        else:
            self.bias_ih.data.copy_(cast(Linear, self.isub).bias.data)
            self.bias_hh.data.copy_(cast(Linear, self.hsub).bias.data)

        # Remove from registration.
        del self.parameter.submodels["isub"]
        del self.parameter.submodels["hsub"]
        del self.parameter.submodels["join"]
        del self.parameter.submodels["act"]
        del self.isub
        del self.hsub
        del self.join
        del self.act