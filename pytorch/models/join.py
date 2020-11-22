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
# << Joining Gradient Model >>
# The joining gradient model.
# The model forward function $f$ is a compostion of basic algebrea that join
# several inputs together into a single output.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Join(GradModel):
    r"""
    Join.
    """
    # Define main flow name.
    main = "join"

    def __parse__(
        self: Join,
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
        self.ky_input_residuals: List[str]
        self.ky_output_residuals: List[str]
        self.ky_inputs: List[str]
        self.ky_output: str

        # Fetch main input and output.
        self.ky_input_residuals, self.ky_output_residuals = (
            self.IOKEYS["{:s}_residuals".format(self.main)]
        )
        self.ky_inputs, (self.ky_output,) = self.IOKEYS[self.main]

        # Safety check.
        for ky_inres, ky_outres in zip(
            self.ky_input_residuals, self.ky_output_residuals,
        ):
            if (ky_outres == self.ky_output):
                error(
                    "Join residual output key \"{:s}\" is occupied by" \
                    " an activated key.",
                    self.ky_output,
                )
                raise RuntimeError
            elif (ky_inres == ky_outres):
                pass
            else:
                error(
                    "Join residual keys do not match from input" \
                    " \"{:s}\" to output \"{:s}\".",
                    ky_inres, ky_outres,
                )
                raise RuntimeError

    def __nullin__(
        self: Join,
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

            # Join works on any tensor inputs.
            raise NotImplementedError

        # Return the function.
        return null

    def __nullout__(
        self: Join,
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

            # Join works on any tensor inputs.
            raise NotImplementedError

        # Return the function.
        return null

    def configure(
        self: Join,
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

        # Join requires nothing.
        pass

    def __initialize__(
        self: Join,
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

        # Join is not parametric.
        pass


class AddJoin(Join):
    r"""
    Addition (element-wise) join.
    """
    # Define main flow name.
    main = "add_join"

    def __forward__(
        self: AddJoin,
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

            # Join directly.
            tensor = input[self.ky_inputs[0]]
            for key in self.ky_inputs[1:]:
                tensor += input[key]
            output[self.ky_output] = tensor

            # Add residual-from-input outputs.
            for ky_inres, ky_outres in zip(
                self.ky_input_residuals, self.ky_output_residuals,
            ):
                output[ky_outres] = input[ky_inres]
            return output

        # Return the function.
        return f


class MulJoin(Join):
    r"""
    Multiplication (element-wise) join.
    """
    # Define main flow name.
    main = "mul_join"

    def __forward__(
        self: MulJoin,
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

            # Join directly.
            tensor = input[self.ky_inputs[0]]
            for key in self.ky_inputs[1:]:
                tensor *= input[key]
            output[self.ky_output] = tensor

            # Add residual-from-input outputs.
            for ky_inres, ky_outres in zip(
                self.ky_input_residuals, self.ky_output_residuals,
            ):
                output[ky_outres] = input[ky_inres]
            return output

        # Return the function.
        return f