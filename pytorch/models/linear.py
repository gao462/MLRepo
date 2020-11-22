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
# << Linear Gradient Model >>
# The linear gradient model.
# The model forward function $f$ must be constructed with linear matrix
# operations, such as matrix multiplication, element-wise addition.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Linear(GradModel):
    r"""
    Linear.
    """
    # Define main flow name.
    main = "linear"

    def __parse__(
        self: Linear,
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
        self.ky_input: str
        self.ky_output: str

        # Fetch main input and output.
        (self.ky_input,), (self.ky_output,) = self.IOKEYS[self.main]

    def __forward__(
        self: Linear,
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

            # Apply matrix multiplication and bias.
            tensor = getattr(torch, "matmul")(
                input[self.ky_input], parameter["weight"].t(),
            )
            if (self.no_bias):
                output[self.ky_output] = tensor
            else:
                output[self.ky_output] = tensor + parameter["bias"]
            return output

        # Return the function.
        return f

    def __nullin__(
        self: Linear,
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

            # return all-zero.
            return {
                self.ky_input: getattr(torch, "zeros")(
                    1, self.num_inputs, dtype=self.DTYPE, device=self.device,
                ),
            }

        # Return the function.
        return null

    def __nullout__(
        self: Linear,
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

            # return all-zero.
            return {
                self.ky_output: getattr(torch, "zeros")(
                    1, self.num_outputs, dtype=self.DTYPE, device=self.device,
                ),
            }

        # Return the function.
        return null

    def configure(
        self: Linear,
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
        self.weight: torch.nn.parameter.Parameter
        self.bias: torch.nn.parameter.Parameter
        self.num_inputs: int
        self.num_outputs: int
        self.no_bias: bool

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]
        self.no_bias = xkargs["no_bias"]

        # Allocate parameters.
        self.weight = torch.nn.parameter.Parameter(getattr(torch, "zeros")(
            self.num_outputs, self.num_inputs,
            dtype=self.DTYPE, device=self.device,
        ))
        if (self.no_bias):
            pass
        else:
            self.bias = torch.nn.parameter.Parameter(getattr(torch, "zeros")(
                self.num_outputs, dtype=self.DTYPE, device=self.device,
            ))

    def __initialize__(
        self: Linear,
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

        Use Kaiming Uniform as PyTorch default.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Initialize weight.
        gain = Linear.activation_gain(
            name=xkargs["activation"], negative_slope=xkargs["negative_slope"],
        )
        std = gain / math.sqrt(self.num_inputs)
        bound = math.sqrt(3) * std
        self.weight.data.uniform_(-bound, bound, generator=self.rng)

        # Initialize bias if necessary.
        if (self.no_bias):
            pass
        else:
            bound = 1 / math.sqrt(self.num_inputs)
            self.bias.data.uniform_(-bound, bound, generator=self.rng)

    @staticmethod
    def activation_gain(
        *args: ArgT,
        name: str, negative_slope: float,
        **kargs: KArgT,
    ) -> float:
        r"""
        Activation gain for initialization.

        Args
        ----
        - *args
        - name
            Activation name.
            "null" for no activation or convolution.
            "sigmoid" for Sigmoid activation.
            "tanh" for Tanh activation.
            "relu" for Relu activation.
            "leaky_relu" for Leaky ReLU activation.
        - negative_slope
            Negative slope for Leaky ReLU activation.
            Use 0 if activation is not Leaky ReLU.
        - **kargs

        Returns
        -------
        - gain
            Gain.

        It is directly duplicated from PyTorch default.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Get gain.
        if (name == "sigmoid"):
            return 1.0
        elif (name == "tanh"):
            return 5.0 / 3.0
        elif (name == "relu"):
            return math.sqrt(2.0)
        elif (name == "leaky_relu"):
            return math.sqrt(2.0 / (1.0 + negative_slope ** 2))
        else:
            error("Activcation \"{:s}\" has no gain definition.", name)
            raise RuntimeError


class __Linear__(Linear):
    r"""
    PyTorch Linear.
    """
    def __forward__(
        self: __Linear__,
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

            # Apply matrix multiplication and bias.
            output = {}
            output[self.ky_output] = self.pytorch.forward(input[self.ky_input])
            return output

        # Return the function.
        return f

    def configure(
        self: __Linear__,
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
        self.weight: torch.nn.parameter.Parameter
        self.bias: torch.nn.parameter.Parameter

        # Super.
        Linear.configure(self, xargs, xkargs)

        # Allocate parameters.
        self.pytorch = torch.nn.Linear(
            in_features=self.num_inputs, out_features=self.num_outputs,
            bias=not self.no_bias,
        ).to(self.device)
        self.weight = getattr(self.pytorch, "weight")
        self.bias = getattr(self.pytorch, "bias")