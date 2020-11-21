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
# << Message Gradient Model >>
# The message gradient model.
# The model forward function $f$ accepts a list of destiniation feature
# $X^{(\text{dst})}$, a list of edge feature $E$ and a list of source feature
# $X^{(\text{src})}$.
# They will match on the list length.
#
# The function $f$ just get a message output for each pair of destination
# feature, edge feature and source feature.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class ConcatMessage(GradModel):
    r"""
    Concatentation message.
    """
    # Define main flow name.
    main = "concat_msg"

    def __parse__(
        self: ConcatMessage,
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
        self.ky_input_dst: str
        self.ky_input_e: str
        self.ky_input_src: str
        self.ky_output: str
        self.ky_inputs: List[str]

        # Fetch main input and output.
        (
            (self.ky_input_dst, self.ky_input_e, self.ky_input_src),
            (self.ky_output,),
        ) = self.IOKEYS[self.main]
        self.ky_inputs = []

    def __forward__(
        self: ConcatMessage,
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
            buf: List[torch.Tensor]
            output: Dict[str, torch.Tensor]

            # Take keeping tensors into buffer and concatenate.
            buf = []
            for key in self.ky_inputs:
                buf.append(input[key])
            output = {self.ky_output: getattr(torch, "cat")(buf, dim=1)}
            return output

        # Return the function.
        return f

    def __nullin__(
        self: ConcatMessage,
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

            # Neighbor aggregation has no null definition.
            raise NotImplementedError

        # Return the function.
        return null

    def __nullout__(
        self: ConcatMessage,
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

            # Neighbor aggregation has no null definition.
            raise NotImplementedError

        # Return the function.
        return null

    def configure(
        self: ConcatMessage,
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

        # Take keeping keys.
        if (xkargs["keep"]["node_input_dst"]):
            self.ky_inputs.append(self.ky_input_dst)
        else:
            pass
        if (xkargs["keep"]["edge_input"]):
            self.ky_inputs.append(self.ky_input_e)
        else:
            pass
        if (xkargs["keep"]["node_input_src"]):
            self.ky_inputs.append(self.ky_input_src)
        else:
            pass

        # Ensure at least one message.
        if (len(self.ky_inputs) == 0):
            error("Message requires at least one input key.")
            raise RuntimeError
        else:
            pass

    def __initialize__(
        self: ConcatMessage,
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
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Concatenation is a naive function requiring nothing.
        pass