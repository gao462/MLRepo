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

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Gradient Model Virtual Objects >>
# The virtual gradient supporting model prototype.
# All learning models can be described as learning (can learn nothing) from an
# input and an expected output (can be the same as input) are covered by this
# prototype.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GradModel(abc.ABC):
    r"""
    Virtual class for gradient supporting model.
    """
    def __init__(
        self: GradModel,
        root: str,
        *args: ArgT,
        dtype: str,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - root
            Root directory for all datasets.
        - *args
        - dtype
            Data precision.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.ROOT: Const = root
        self.DTYPE: Const = getattr(torch, dtype)

    def set(
        self: GradModel,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Settle down and register model parameters and sub models.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        It will automatically scan model attributes after configuration.
        Then, it will register scanned `torch.nn.module.Parameter` objects as
        parameters, and scanned `Model` objects as sub models.
        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Configure model with given extra arguments.
        self.configure(xargs, xkargs)

        # Scan over model attributes by now.
        self.parameters = {}
        self.submodels = {}
        for key, val in vars(self).items():
            if (isinstance(val, torch.nn.parameter.Parameter)):
                self.parameters[key] = val
            elif (isinstance(val, GradModel)):
                self.submodels[key] = val
            else:
                pass

    @abc.abstractmethod
    def configure(
        self: GradModel,
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
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def initialize(
        self: GradModel,
        rng: torch._C.Generator,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize model parameters and sub models.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def decode(
        self: GradModel,
        batch: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> MultiReturn[
        List[Dict[str, torch.Tensor]], List[Dict[str, torch.Tensor]]
    ]:
        r"""
        Decode batch.

        Args
        ----
        - self
        - batch
            Batch.
        - *args
        - **kargs

        Returns
        -------
        - input
            Batch with input parts only.
        - target
            Batch with target parts only.

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def forward(
        self: GradModel,
        input: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> List[Dict[str, torch.Tensor]]:
        r"""
        Forward a batch input part.

        Args
        ----
        - self
        - input
            Batch with input parts only.
        - *args
        - **kargs

        Returns
        -------
        - output
            Batch with output parts only.

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def train_loss_func(
        self: GradModel,
        output: List[Dict[str, torch.Tensor]],
        target: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Training loss function.

        Args
        ----
        - self
        - output
            Batch with output parts only.
        - target
            Batch with target parts only.
        - *args
        - **kargs

        Returns
        -------
        - loss
            Training loss.

        """
        # /
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def eval_loss_func(
        self: GradModel,
        output: List[Dict[str, torch.Tensor]],
        target: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Evaluating loss function.

        Args
        ----
        - self
        - output
            Batch with output parts only.
        - target
            Batch with target parts only.
        - *args
        - **kargs

        Returns
        -------
        - loss
            Evaluating loss.

        """
        # /
        # VIRTUAL
        # /
        ...

    def training(
        self: GradModel,
        batch: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Forward a batch input part and compare its output part with expected
        target part in training stage.

        Args
        ----
        - self
        - batch
            Batch.
        - *args
        - **kargs

        Returns
        -------
        - loss
            Latest loss in training and evaluating stages.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Split input and target.
        self.input, self.target = self.decode(batch)

        # Get output and training loss.
        self.output = self.forward(self.input)
        self.loss = self.train_loss_func(self.output, self.target)

        # Utilize autograd.
        getattr(self.loss, "backward")()
        return self.loss

    def evaluating(
        self: GradModel,
        batch: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Forward a batch input part and compare its output part with expected
        target part in evaluating stage.

        Args
        ----
        - self
        - batch
            Batch.
        - *args
        - **kargs

        Returns
        -------
        - loss
            Latest loss in training and evaluating stages.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Split input and target.
        self.input, self.target = self.decode(batch)

        # Get output and training loss.
        self.output = self.forward(self.input)
        self.loss = self.eval_loss_func(self.output, self.target)
        return self.loss