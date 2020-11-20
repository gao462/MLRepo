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
# << Collection of Gradient Model >>
# The collection of gradient models working as a gradient model.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GradModelSeq(GradModel):
    r"""
    A sequence of gradient models.
    """
    # Define main flow name.
    main = "seq"

    def __parse__(
        self: GradModelSeq,
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

        # Collection is just a wrapped without IO flow.
        pass

    def __forward__(
        self: GradModelSeq,
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
            transient = input
            for i, model in enumerate(self.models):
                transient = model.forward(
                    parameter.sub("{:d}".format(i)), transient,
                )
            output = transient
            return output

        # Return the function.
        return f

    def __nullin__(
        self: GradModelSeq,
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

            # return all-zero.
            return self.models[0].nullin(device)

        # Return the function.
        return null

    def __nullout__(
        self: GradModelSeq,
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

            # return all-zero.
            return self.models[-1].nullout(device)

        # Return the function.
        return null

    def configure(
        self: GradModelSeq,
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
        self.models: List[GradModel]

        # Save necessary attributes.
        self.models = []
        for model in xargs:
            self.models.append(model)

    def workflow_diffuse(
        self: GradModelSeq,
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, List[List[Tuple[str, str, str]]]]:
        r"""
        Diffuse workflow defined by sub models and IO keys.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - flows.
            Work flows of each sub model.
            The model itself is defined as sub model "".
            Work flow is a list of lists of section, input key and output key
            items.
            Same section name is aggregated in the same list.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        flows: Dict[str, List[List[Tuple[str, str, str]]]]

        # Get sub model flows.
        flows = {}
        for i, val in enumerate(self.models):
            key = "{:d}".format(i)
            for sub, grouped in val.workflow.items():
                if (sub == ""):
                    flows[key] = grouped
                else:
                    flows[key + "." + sub] = grouped
        return flows

    def __initialize__(
        self: GradModelSeq,
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
        for i, ini in enumerate(xargs):
            self.models[i].initialize(
                rng, xargs=ini["xargs"], xkargs=ini["xkargs"],
            )

    def __len__(
        self: GradModelSeq,
        *args: ArgT,
        **kargs: KArgT,
    ) -> int:
        r"""
        Get length.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Get memory length.
        return len(self.models)

    def __getitem__(
        self: GradModelSeq,
        i: int,
        *args: ArgT,
        **kargs: KArgT,
    ) -> GradModel:
        r"""
        Get length.

        Args
        ----
        - self
        - i
            Index.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Get item from saved models.
        return self.models[i]

    def register(
        self: GradModelSeq,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Register parameters and sub models.

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

        # Super.
        GradModel.register(self)

        # Manually register the model list.
        for i, model in enumerate(self.models):
            self.parameter.registar_submodel(
                "{:d}".format(i), model.parameter,
            )