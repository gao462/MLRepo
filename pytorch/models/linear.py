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
            self.num_outputs, self.num_inputs, dtype=self.DTYPE,
        ))
        if (self.no_bias):
            pass
        else:
            self.bias = torch.nn.parameter.Parameter(getattr(torch, "zeros")(
                self.num_outputs, dtype=self.DTYPE,
            ))

    def initialize(
        self: Linear,
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
        self.weight.data.uniform_(-bound, bound, generator=rng)

        # Initialize bias if necessary.
        if (self.no_bias):
            pass
        else:
            bound = 1 / math.sqrt(self.num_inputs)
            self.bias.data.uniform_(-bound, bound, generator=rng)

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

    def set_forward(
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

        # Get IO direction.
        (inkey,), (outkey,) = self.IOKEYS["linear"]

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
            tensor = getattr(torch, "matmul")(
                input[inkey], parameter["weight"].t(),
            )
            if (self.no_bias):
                output[outkey] = tensor
            else:
                output[outkey] = tensor + parameter["bias"]
            return output

        # Return the function.
        return f

    def null_input(
        self: Linear,
        batch_size: Union[int, None],
        device: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Generate null input.

        Args
        ----
        - self
        - batch_size
            Batch size.
            If it is None, return not-in-batch version.
        - device
            Device.

        Returns
        -------
        - input
            Null input.

        After setup, the null input to a model is fixed.
        This is helpful to understand the expectation of input.
        This is also useful when the default model output is required, for
        example, this is the sub model of RNN H-to-H model at the first time
        step.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Get IO direction.
        (inkey,), (outkey,) = self.IOKEYS["linear"]

        # return all-zero.
        return {
            inkey: getattr(torch, "zeros")(
                batch_size, self.num_inputs, dtype=self.DTYPE, device=device,
            ),
        }

    def null_output(
        self: Linear,
        batch_size: Union[int, None],
        device: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Generate null output.

        Args
        ----
        - self
        - batch_size
            Batch size.
            If it is None, return not-in-batch version.
        - device
            Device.
        - *kargs
        - **kargs

        Returns
        -------
        - input
            Null input.

        After setup, the null output to a model is fixed.
        This is helpful to understand the expectation of output.
        This is also useful when the default model output is required, for
        example, this is the sub model of RNN H-to-H model at the first time
        step.
        Null output does not have batch dimension.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Get IO direction.
        (inkey,), (outkey,) = self.IOKEYS["linear"]

        # return all-zero.
        return {
            outkey: getattr(torch, "zeros")(
                batch_size, self.num_outputs, dtype=self.DTYPE, device=device,
            ),
        }


class __Linear__(Linear):
    r"""
    PyTorch Linear.
    """
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
        self.num_inputs: int
        self.num_outputs: int
        self.no_bias: bool

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]
        self.no_bias = xkargs["no_bias"]

        # Allocate parameters.
        self.pytorch = torch.nn.Linear(
            in_features=self.num_inputs, out_features=self.num_outputs,
            bias=not self.no_bias,
        )
        self.weight = getattr(self.pytorch, "weight")
        self.bias = getattr(self.pytorch, "bias")

    def set_forward(
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
            (inkey,), (outkey,) = self.IOKEYS["linear"]
            output[outkey] = self.pytorch.forward(input[inkey])
            return output

        # Return the function.
        return f