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

        # Fetch all things to local level.
        (agg_ikey, agg_hkey), (agg_outkey,) = self.IOKEYS["rnn_aggregate"]
        (inkey,), (outkey,) = self.IOKEYS["rnn"]
        hnullout = self.hsub.nullout
        iforward = self.isub.forward
        hforward = self.hsub.forward
        transform = self.transform

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

            # Get essential sequence info.
            tensor = next(iter(input.values()))
            sample_length = tensor.size(0)
            batch_size = tensor.size(1)
            device = tensor.device

            # Get essential recurrent transient buffer and expand batch
            # dimension by batch size.
            transient = {}
            tensor = hnullout(device)[agg_hkey]
            shape = list(tensor.size())[1:]
            transient[agg_outkey] = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                for key, val in input.items():
                    transient[key] = val[t]
                ibuf = iforward(parameter.sub("isub"), transient)
                hbuf = hforward(parameter.sub("hsub"), transient)
                transient[agg_outkey] = transform(
                    ibuf[agg_ikey] + hbuf[agg_hkey],
                )
            output = {}
            output[outkey] = transient[inkey]
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

        # Fetch all things to local level.
        inullin = self.isub.nullin
        hnullin = self.hsub.nullin

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

            # Get sub model inputs.
            inull = inullin(device)
            hnull = hnullin(device)

            # Merge sub model inputs and extend with sequence dimension at the
            # beginning.
            output = {}
            for key, val in inull.items():
                output[key] = val.unsqueeze(0)
            for key, val in hnull.items():
                output[key] = val.unsqueeze(0)
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

        # Fetch all things to local level.
        (inkey,), (outkey,) = self.IOKEYS["rnn"]
        hnullout = self.hsub.nullout

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

            # Get sub model outputs.
            hnull = hnullout(device)

            # Output is just hidden model output with extra sequence dimension.
            output = {}
            output[outkey] = hnull[inkey].unsqueeze(0)
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
        self.transform: Callable[[torch.Tensor], torch.Tensor]
        self.isub: GradModel
        self.hsub: GradModel

        # Get model aggregation transform.
        self.transform_name = xkargs["transform"]
        self.transform = getattr(torch, self.transform_name)

        # Get models for raw input and hidden state.
        self.isub = xkargs["isub"]
        self.hsub = xkargs["hsub"]

    def __initialize__(
        self: RNN,
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
        self.isub.initialize(rng, xargs=xargs, xkargs=xkargs)
        self.hsub.initialize(rng, xargs=xargs, xkargs=xkargs)


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

        # Fetch all things to local level.
        (_, agg_hkey), (_,) = self.IOKEYS["rnn_aggregate"]
        _, (outkey,) = self.IOKEYS["rnn"]
        hnullout = self.hsub.nullout
        i_inkey = self.i_inkey
        pytorch = self.pytorch

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

            # Get essential sequence info.
            tensor = next(iter(input.values()))
            sample_length = tensor.size(0)
            batch_size = tensor.size(1)
            device = tensor.device

            # Get essential recurrent transient buffer and expand batch
            # dimension by batch size.
            tensor = hnullout(device)[agg_hkey]
            shape = list(tensor.size())[1:]
            transient = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                raw = input[i_inkey][t]
                transient = pytorch.forward(raw, transient)
            output = {}
            output[outkey] = transient
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

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]
        self.no_bias = xkargs["no_bias"]
        self.transform_name = xkargs["transform"]

        # Allocate parameters.
        self.pytorch = torch.nn.RNNCell(
            input_size=self.num_inputs, hidden_size=self.num_outputs,
            bias=not self.no_bias, nonlinearity=self.transform_name,
        )
        self.weight_ih = getattr(self.pytorch, "weight_ih")
        self.weight_hh = getattr(self.pytorch, "weight_hh")
        self.bias_ih = getattr(self.pytorch, "bias_ih")
        self.bias_hh = getattr(self.pytorch, "bias_hh")

        # Temporarily save sub models for initialization consistency.
        self.isub = xkargs["isub"]
        self.hsub = xkargs["hsub"]

        # Pre-fetch IO direction only for linear form.
        (self.i_inkey,), (_,) = self.isub.IOKEYS["linear"]
        (self.h_inkey,), (_,) = self.hsub.IOKEYS["linear"]

    def __initialize__(
        self: __RNN__,
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

        # Simulate linear units.
        self.isub = cast(Linear, self.isub)
        self.hsub = cast(Linear, self.hsub)
        self.isub.initialize(rng, xargs=xargs, xkargs=xkargs)
        self.hsub.initialize(rng, xargs=xargs, xkargs=xkargs)

        # Copy data to correct place.
        self.weight_ih.data.copy_(self.isub.weight.data)
        self.weight_hh.data.copy_(self.hsub.weight.data)
        if (self.no_bias):
            pass
        else:
            self.bias_ih.data.copy_(self.isub.bias.data)
            self.bias_hh.data.copy_(self.hsub.bias.data)

        # Remove from registration.
        del self.parameter.submodels["isub"]
        del self.parameter.submodels["hsub"]