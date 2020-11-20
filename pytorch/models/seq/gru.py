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
# << GRU Gradient Model >>
# The GRU gradient model.
# The model forward function $f$ must be described as:
#
# $$
# r = f_{\text{reset}} \left( \theta_{\text{reset}}, x, h \right)
# u = f_{\text{update}} \left( \theta_{\text{update}}, x, h \right)
# c = f_{\text{cell}} \left( \theta_{\text{cell}}, x, r \odot h, \right)
# y = f_{\text{output}} \left(
#    \theta_{\text{output}}, u \odot h, (1 - u) \odot c,
# \right)
# $$
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GRU(GradModel):
    r"""
    RNN.
    """
    # Define main flow name.
    main = "gru"

    def __forward__(
        self: GRU,
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

        In GRU, the function $f$ is further abstracted into:

        $$
        r = f_{\text{reset}} \left( \theta_{\text{reset}}, x, h \right)
        u = f_{\text{update}} \left( \theta_{\text{update}}, x, h \right)
        c = f_{\text{cell}} \left( \theta_{\text{cell}}, x, r \odot h, \right)
        y = f_{\text{output}} \left(
           \theta_{\text{output}}, u \odot h, (1 - u) \odot c,
        \right)
        $$
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Fetch all things to local level.
        (reset_ikey, reset_hkey), (reset_outkey,) = (
            self.IOKEYS["gru_reset_agg"]
        )
        (update_ikey, update_hkey), (update_outkey,) = (
            self.IOKEYS["gru_update_agg"]
        )
        (cell_ikey, cell_rkey, cell_hkey), (cell_outkey,) = (
            self.IOKEYS["gru_cell_agg"]
        )
        (agg_gtkey, agg_inkey, agg_clkey), (agg_outkey,) = (
            self.IOKEYS["gru_aggregate"]
        )
        (inkey,), (outkey,) = self.IOKEYS["gru"]
        hnullout = self.cell_hsub.nullout
        reset_iforward = self.reset_isub.forward
        reset_hforward = self.reset_hsub.forward
        update_iforward = self.update_isub.forward
        update_hforward = self.update_hsub.forward
        cell_iforward = self.cell_isub.forward
        cell_hforward = self.cell_hsub.forward
        gate_transform = getattr(torch, "sigmoid")
        cell_transform = getattr(torch, "tanh")

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
            tensor = hnullout(device)[cell_hkey]
            shape = list(tensor.size())[1:]
            transient[agg_outkey] = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                # Fill in raw input of current step.
                for key, val in input.items():
                    transient[key] = val[t]

                # Get reset gate.
                reset = {}
                ibuf = reset_iforward(
                    parameter.sub("reset_isub"), transient,
                )
                hbuf = reset_hforward(
                    parameter.sub("reset_hsub"), transient,
                )
                reset[reset_outkey] = gate_transform(
                    ibuf[reset_ikey] + hbuf[reset_hkey],
                )

                # Get update gate.
                update = {}
                ibuf = update_iforward(
                    parameter.sub("update_isub"), transient,
                )
                hbuf = update_hforward(
                    parameter.sub("update_hsub"), transient,
                )
                update[update_outkey] = gate_transform(
                    ibuf[update_ikey] + hbuf[update_hkey],
                )

                # Get cell state with projected hidden state.
                cell = {}
                ibuf = cell_iforward(
                    parameter.sub("cell_isub"), transient,
                )
                hbuf = cell_hforward(
                    parameter.sub("cell_hsub"), transient,
                )
                cell[cell_outkey] = cell_transform(
                    ibuf[cell_ikey] + reset[cell_rkey] * hbuf[cell_hkey],
                )

                # Get final weighted summation.
                transient[agg_outkey] = (
                    update[agg_gtkey] * transient[agg_inkey] +
                    (1 - update[agg_gtkey]) * cell[agg_clkey]
                )
            output = {}
            output[outkey] = transient[inkey]
            return output

        # Return the function.
        return f

    def __nullin__(
        self: GRU,
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
        inullin = self.cell_isub.nullin
        hnullin = self.cell_hsub.nullin

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
        self: GRU,
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
        (inkey,), (outkey,) = self.IOKEYS["gru"]
        hnullout = self.cell_hsub.nullout

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
        self: GRU,
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
        self.gate_transform: Callable[[torch.Tensor], torch.Tensor]
        self.cell_transform: Callable[[torch.Tensor], torch.Tensor]
        self.reset_isub: GradModel
        self.reset_hsub: GradModel
        self.update_isub: GradModel
        self.update_hsub: GradModel
        self.cell_isub: GradModel
        self.cell_hsub: GradModel

        # Get models for raw input and hidden state.
        self.reset_isub = xkargs["reset_isub"]
        self.reset_hsub = xkargs["reset_hsub"]
        self.update_isub = xkargs["update_isub"]
        self.update_hsub = xkargs["update_hsub"]
        self.cell_isub = xkargs["cell_isub"]
        self.cell_hsub = xkargs["cell_hsub"]

    def __initialize__(
        self: GRU,
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
        self.reset_isub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.reset_hsub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.update_isub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.update_hsub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.cell_isub.initialize(
            rng,
            xargs=xkargs["cell"]["xargs"], xkargs=xkargs["cell"]["xkargs"],
        )
        self.cell_hsub.initialize(
            rng,
            xargs=xkargs["cell"]["xargs"], xkargs=xkargs["cell"]["xkargs"],
        )


class __GRU__(GRU):
    r"""
    PyTorch GRU.
    """
    def __forward__(
        self: __GRU__,
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

        In GRU, the function $f$ is further abstracted into:

        $$
        r = f_{\text{reset}} \left( \theta_{\text{reset}}, x, h \right)
        u = f_{\text{update}} \left( \theta_{\text{update}}, x, h \right)
        c = f_{\text{cell}} \left( \theta_{\text{cell}}, x, r \odot h, \right)
        y = f_{\text{output}} \left(
           \theta_{\text{output}}, u \odot h, (1 - u) \odot c,
        \right)
        $$
        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Fetch all things to local level.
        (cell_ikey, cell_rkey, cell_hkey), (cell_outkey,) = (
            self.IOKEYS["gru_cell_agg"]
        )
        (agg_gtkey, agg_inkey, agg_clkey), (agg_outkey,) = (
            self.IOKEYS["gru_aggregate"]
        )
        (inkey,), (outkey,) = self.IOKEYS["gru"]
        hnullout = self.cell_hsub.nullout
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
            tensor = hnullout(device)[cell_hkey]
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
        self: __GRU__,
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

        # Allocate parameters.
        self.pytorch = torch.nn.GRUCell(
            input_size=self.num_inputs, hidden_size=self.num_outputs,
            bias=not self.no_bias,
        )
        self.weight_ih = getattr(self.pytorch, "weight_ih")
        self.weight_hh = getattr(self.pytorch, "weight_hh")
        self.bias_ih = getattr(self.pytorch, "bias_ih")
        self.bias_hh = getattr(self.pytorch, "bias_hh")

        # Temporarily save sub models for initialization consistency.
        self.reset_isub = xkargs["reset_isub"]
        self.reset_hsub = xkargs["reset_hsub"]
        self.update_isub = xkargs["update_isub"]
        self.update_hsub = xkargs["update_hsub"]
        self.cell_isub = xkargs["cell_isub"]
        self.cell_hsub = xkargs["cell_hsub"]

        # Pre-fetch IO direction only for linear form.
        (self.i_inkey,), (_,) = self.cell_isub.IOKEYS["linear"]
        (self.h_inkey,), (_,) = self.cell_hsub.IOKEYS["linear"]

    def __initialize__(
        self: __GRU__,
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

        # Simulate linear units.
        self.reset_isub = cast(Linear, self.reset_isub)
        self.reset_hsub = cast(Linear, self.reset_hsub)
        self.update_isub = cast(Linear, self.update_isub)
        self.update_hsub = cast(Linear, self.update_hsub)
        self.cell_isub = cast(Linear, self.cell_isub)
        self.cell_hsub = cast(Linear, self.cell_hsub)
        self.reset_isub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.reset_hsub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.update_isub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.update_hsub.initialize(
            rng,
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.cell_isub.initialize(
            rng,
            xargs=xkargs["cell"]["xargs"], xkargs=xkargs["cell"]["xkargs"],
        )
        self.cell_hsub.initialize(
            rng,
            xargs=xkargs["cell"]["xargs"], xkargs=xkargs["cell"]["xkargs"],
        )

        # Merge matrices to fit PyTorch.
        weight_ih = getattr(torch, "cat")([
            self.reset_isub.weight.data,
            self.update_isub.weight.data,
            self.cell_isub.weight.data,
        ], dim=0)
        weight_hh = getattr(torch, "cat")([
            self.reset_hsub.weight.data,
            self.update_hsub.weight.data,
            self.cell_hsub.weight.data,
        ], dim=0)
        bias_ih = getattr(torch, "cat")([
            self.reset_isub.bias.data,
            self.update_isub.bias.data,
            self.cell_isub.bias.data,
        ], dim=0)
        bias_hh = getattr(torch, "cat")([
            self.reset_hsub.bias.data,
            self.update_hsub.bias.data,
            self.cell_hsub.bias.data,
        ], dim=0)

        # Copy data to correct place.
        self.weight_ih.data.copy_(weight_ih)
        self.weight_hh.data.copy_(weight_hh)
        if (self.no_bias):
            pass
        else:
            self.bias_ih.data.copy_(bias_ih)
            self.bias_hh.data.copy_(bias_hh)

        # Remove from registration.
        del self.parameter.submodels["reset_isub"]
        del self.parameter.submodels["reset_hsub"]
        del self.parameter.submodels["update_isub"]
        del self.parameter.submodels["update_hsub"]
        del self.parameter.submodels["cell_isub"]
        del self.parameter.submodels["cell_hsub"]