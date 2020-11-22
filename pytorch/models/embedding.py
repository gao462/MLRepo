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
# << Embedding Gradient Model >>
# The embedding gradient model.
# The model forward function $f$ accepts an index $i$ and returns learnable
# embedding $\theta_{i}$ for it.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Embedding(GradModel):
    r"""
    Embedding.
    """
    # Define main flow name.
    main = "embedding"

    def __parse__(
        self: Embedding,
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
        self: Embedding,
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

            # Get embeddings by direct indexing.
            indices = input[self.ky_input]
            indices = indices.view(len(indices))
            output[self.ky_output] = parameter["embedding"][indices]
            return output

        # Return the function.
        return f

    def __nullin__(
        self: Embedding,
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
                    1, dtype=getattr(torch, "long"), device=self.device,
                ),
            }

        # Return the function.
        return null

    def __nullout__(
        self: Embedding,
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
                    1, self.num_features, dtype=self.DTYPE, device=self.device,
                ),
            }

        # Return the function.
        return null

    def configure(
        self: Embedding,
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
        self.embedding: torch.nn.parameter.Parameter

        # Save necessary attributes.
        self.num_embeddings = xkargs["num_embeddings"]
        self.num_features = xkargs["num_features"]

        # Allocate parameters.
        self.embedding = torch.nn.parameter.Parameter(getattr(torch, "zeros")(
            self.num_embeddings, self.num_features,
            dtype=self.DTYPE, device=self.device,
        ))

    def __initialize__(
        self: Embedding,
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

        Use normal as PyTorch default.
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Initialize embedding.
        self.embedding.data.normal_(0, 1, generator=self.rng)


class __Embedding__(Embedding):
    r"""
    PyTorch embedding.
    """
    def __forward__(
        self: __Embedding__,
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
            indices = input[self.ky_input]
            indices = indices.view(len(indices))
            output[self.ky_output] = self.pytorch.forward(indices)
            return output

        # Return the function.
        return f

    def configure(
        self: __Embedding__,
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
        Embedding.configure(self, xargs, xkargs)

        # Allocate parameters.
        self.pytorch = torch.nn.Embedding(
            num_embeddings=self.num_embeddings,
            embedding_dim=self.num_features,
            padding_idx=None, max_norm=None, norm_type=2,
            scale_grad_by_freq=False, sparse=False,
        ).to(self.device)
        self.embedding = getattr(self.pytorch, "weight")