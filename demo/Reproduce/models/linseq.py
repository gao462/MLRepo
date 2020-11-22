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
from pytorch.models.model import GradModel, Parameter
from pytorch.models.model import ForwardFunction, LossFunction, NullFunction
from pytorch.models.linear import Linear
from pytorch.models.activation import Activation
from pytorch.models.collect import GradModelSeq
from demo.Reproduce.models.naive import NaiveDistLoss


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Linear Gradient Model Sequence Naive Distribution >>
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class RepLinearSeq(GradModel):
    r"""
    Reproduced Linear sequence.
    """
    # Define main flow name.
    main = "linear_seq"

    def __parse__(
        self: RepLinearSeq,
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
        ...

        # No flow runs.
        pass

    def __forward__(
        self: RepLinearSeq,
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

            # Apply sequential flow directly.
            output = self.seq.forward(parameter.sub("seq"), input)
            return output

        # Return the function.
        return f

    def __nullin__(
        self: RepLinearSeq,
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
            return self.seq.nullin()

        # Return the function.
        return null

    def __nullout__(
        self: RepLinearSeq,
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
            return self.seq.nullout()

        # Return the function.
        return null

    def configure(
        self: RepLinearSeq,
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

        # Create a dual linear.
        linear1 = Linear(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                linear=(["input"], ["input.1"]),
            ),
        ).set(
            self.device,
            xargs=(),
            xkargs=dict(
                num_inputs=self.num_inputs, num_outputs=self.num_outputs,
                no_bias=False,
            ),
        )
        activation1 = Activation(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                act_residuals=([], []),
                act=(["input.1"], ["input.1"]),
            ),
        ).set(
            self.device,
            xargs=(),
            xkargs=dict(activation="tanh"),
        )
        linear2 = Linear(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                linear=(["input.1"], ["output"]),
            ),
        ).set(
            self.device,
            xargs=(),
            xkargs=dict(
                num_inputs=self.num_outputs, num_outputs=self.num_outputs,
                no_bias=False,
            ),
        )

        # Allocate sequence collection.
        self.seq = cast(GradModelSeq, GradModelSeq(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys={},
        ).set(
            self.device,
            xargs=(linear1, activation1, linear2),
            xkargs=dict(),
        ))

    def __initialize__(
        self: RepLinearSeq,
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

        # Initialize sequence.
        self.seq.initialize(self.rng.get_state(), xargs=xargs, xkargs=xkargs)

    def __train__(
        self: RepLinearSeq,
        *args: ArgT,
        **kargs: KArgT,
    ) -> LossFunction:
        r"""
        Set training loss function.

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
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # return the function.
        return NaiveDistLoss((["output"], ["target"]))

    def __evaluate__(
        self: RepLinearSeq,
        *args: ArgT,
        **kargs: KArgT,
    ) -> LossFunction:
        r"""
        Set evaluating loss function.

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
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Return the function.
        return NaiveDistLoss((["output"], ["target"]))


class TarLinearSeq(RepLinearSeq):
    r"""
    Targeting linear sequence.
    """
    def __forward__(
        self: TarLinearSeq,
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

            # Apply sequential flow directly.
            output = {}
            output["output"] = getattr(self.pytorch, "forward")(input["input"])
            return output

        # Return the function.
        return f

    def configure(
        self: TarLinearSeq,
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

        # Super.
        RepLinearSeq.configure(self, xargs, xkargs)

        # Allocate sequence collection.
        self.pytorch = torch.nn.Sequential(
            torch.nn.Linear(
                in_features=self.num_inputs, out_features=self.num_outputs,
                bias=True,
            ),
            getattr(torch.nn, "Tanh")(),
            torch.nn.Linear(
                in_features=self.num_outputs, out_features=self.num_outputs,
                bias=True,
            ),
        ).to(self.device)
        self.weight1 = self.pytorch[0].weight
        self.weight2 = self.pytorch[2].weight
        self.bias1 = self.pytorch[0].bias
        self.bias2 = self.pytorch[2].bias

    def __initialize__(
        self: TarLinearSeq,
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
        RepLinearSeq.__initialize__(self, xargs=xargs, xkargs=xkargs)

        # Copy data.
        self.weight1.data.copy_(cast(Linear, self.seq[0]).weight.data)
        self.weight2.data.copy_(cast(Linear, self.seq[2]).weight.data)
        self.bias1.data.copy_(cast(Linear, self.seq[0]).bias.data)
        self.bias2.data.copy_(cast(Linear, self.seq[2]).bias.data)

        # Remove from registration
        del self.parameter.submodels["seq"]
        del self.seq