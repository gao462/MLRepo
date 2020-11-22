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
from pytorch.models.activation import Activation
from pytorch.models.join import AddJoin, MulJoin


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

    def __parse__(
        self: GRU,
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
        self.ky_stains: List[str]
        self.ky_staouts: List[str]
        self.ky_dynins: List[str]
        self.ky_dynouts: List[str]
        self.ky_reset_i: str
        self.ky_reset_h: str
        self.ky_reset_out: str
        self.ky_update_i: str
        self.ky_update_h: str
        self.ky_update_out: str
        self.ky_cell_i: str
        self.ky_cell_h: str
        self.ky_cell_out: str
        self.ky_aggout: str
        self.ky_output: str

        # Fetch main input and output.
        self.ky_stains, self.ky_staouts = (
            self.IOKEYS["{:s}_static".format(self.main)]
        )
        self.ky_dynins, self.ky_dynouts = (
            self.IOKEYS["{:s}_dynamic".format(self.main)]
        )
        (self.ky_reset_i, self.ky_reset_h), (self.ky_reset_out,) = (
            self.IOKEYS["{:s}_reset_agg".format(self.main)]
        )
        (self.ky_update_i, self.ky_update_h), (self.ky_update_out,) = (
            self.IOKEYS["{:s}_update_agg".format(self.main)]
        )
        (self.ky_cell_i, self.ky_cell_h), (self.ky_cell_out,) = (
            self.IOKEYS["{:s}_cell_agg".format(self.main)]
        )
        (self.ky_aggout, self.ky_cell_out), (self.ky_aggout,) = (
            self.IOKEYS["{:s}_aggregate".format(self.main)]
        )
        (self.ky_aggout,), (self.ky_output,) = self.IOKEYS[self.main]

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

            # Keep always-pass inputs.
            output = {}
            for key, tensor in input.items():
                if (key[0] == "$"):
                    output[key] = tensor
                else:
                    pass

            # Get essential sequence info.
            sample_length = cast(int, input["$batch_length"].item())
            batch_size = cast(int,input["$batch_size"].item())

            # Get essential recurrent transient buffer and expand batch
            # dimension by batch size.
            transient = {}
            tensor = self.cell_hsub.nullout(self.device)[self.ky_cell_h]
            shape = list(tensor.size())[1:]
            transient[self.ky_aggout] = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                # Put current static and dynamic inputs into transient buffer.
                for key in self.ky_stains:
                    transient[key] = input[key]
                for key in self.ky_dynins:
                    transient[key] = input["{:s}.{:d}".format(key, t)]

                # Join raw input and hidden state input for reset gate.
                buf = {}
                buf.update(self.reset_isub.forward(
                    parameter.sub("reset_isub"), transient,
                ))
                buf.update(self.reset_hsub.forward(
                    parameter.sub("reset_hsub"), transient,
                ))
                buf.update(self.reset_join.forward(
                    parameter.sub("reset_join"), buf,
                ))
                reset_tensor = self.reset_act.forward(
                    parameter.sub("reset_act"), buf,
                )[self.ky_reset_out]

                # Join raw input and hidden state input for update gate.
                buf = {}
                buf.update(self.update_isub.forward(
                    parameter.sub("update_isub"), transient,
                ))
                buf.update(self.update_hsub.forward(
                    parameter.sub("update_hsub"), transient,
                ))
                buf.update(self.update_join.forward(
                    parameter.sub("update_join"), buf,
                ))
                update_tensor = self.update_act.forward(
                    parameter.sub("update_act"), buf,
                )[self.ky_update_out]

                # Join raw input and hidden state input for cell state.
                buf = {}
                buf[self.ky_reset_out] = reset_tensor
                buf.update(self.cell_isub.forward(
                    parameter.sub("cell_isub"), transient,
                ))
                buf.update(self.cell_hsub.forward(
                    parameter.sub("cell_hsub"), transient,
                ))
                buf.update(self.cell_join1.forward(
                    parameter.sub("cell_join1"), buf,
                ))
                buf.update(self.cell_join2.forward(
                    parameter.sub("cell_join2"), buf,
                ))
                cell_tensor = self.cell_act.forward(
                    parameter.sub("cell_act"), buf,
                )[self.ky_cell_out]

                # Join previous step and hidden state.
                buf = {}
                buf[self.ky_aggout] = transient[self.ky_aggout]
                buf[self.ky_update_out] = update_tensor
                buf["{:s}.complement".format(self.ky_update_out)] = (
                    1 - update_tensor
                )
                buf[self.ky_cell_out] = cell_tensor
                buf.update(self.join1.forward(
                    parameter.sub("join1"), buf,
                ))
                buf.update(self.join2.forward(
                    parameter.sub("join2"), buf,
                ))
                agg_tensor = self.join3.forward(
                    parameter.sub("join3"), buf,
                )[self.ky_aggout]

                # Get dynamic output.
                transient["{:s}.{:d}".format(self.ky_output, t)] = (
                    transient[self.ky_aggout]
                )

            # Fetch static and dynamic outputs.
            for key in self.ky_staouts:
                output[key] = transient[key]
            for t in range(sample_length):
                for key in self.ky_dynouts:
                    output["{:s}.{:d}".format(key, t)] = (
                        transient["{:s}.{:d}".format(key, t)]
                    )
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
            output: Dict[str, torch.Tensor]

            # Get sub model inputs.
            output = {}
            output.update(self.cell_isub.nullin())
            output.update(self.cell_hsub.nullin())
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

            # Get sub model outputs.
            output = self.cell_hsub.nullout()
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
        self.reset_isub: GradModel
        self.reset_hsub: GradModel
        self.update_isub: GradModel
        self.update_hsub: GradModel
        self.cell_isub: GradModel
        self.cell_hsub: GradModel
        self.reset_join: GradModel
        self.update_join: GradModel
        self.cell_join1: GradModel
        self.cell_join2: GradModel
        self.join1: GradModel
        self.join2: GradModel
        self.join3: GradModel

        # Get models for raw input and hidden state.
        self.reset_isub = xkargs["reset_isub"]
        self.reset_hsub = xkargs["reset_hsub"]
        self.update_isub = xkargs["update_isub"]
        self.update_hsub = xkargs["update_hsub"]
        self.cell_isub = xkargs["cell_isub"]
        self.cell_hsub = xkargs["cell_hsub"]

        # Get model reset join.
        self.reset_join = AddJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                add_join_residuals=([], []),
                add_join=(
                    [self.ky_reset_i, self.ky_reset_h],
                    [self.ky_reset_out],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())

        # Get model update join.
        self.update_join = AddJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                add_join_residuals=([], []),
                add_join=(
                    [self.ky_update_i, self.ky_update_h],
                    [self.ky_update_out],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())

        # Get model cell join.
        self.cell_join1 = MulJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                mul_join_residuals=([], []),
                mul_join=(
                    [self.ky_reset_out, self.ky_cell_h],
                    ["{:s}.reset".format(self.ky_cell_h)],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())
        self.cell_join2 = AddJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                add_join_residuals=([], []),
                add_join=(
                    [self.ky_cell_i, "{:s}.reset".format(self.ky_cell_h)],
                    [self.ky_cell_out],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())

        # Get model join.
        self.join1 = MulJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                mul_join_residuals=([], []),
                mul_join=(
                    [self.ky_update_out, self.ky_aggout],
                    ["{:s}.update".format(self.ky_aggout)],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())
        self.join2 = MulJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                mul_join_residuals=([], []),
                mul_join=(
                    [
                        "{:s}.complement".format(self.ky_update_out),
                        self.ky_cell_out,
                    ],
                    ["{:s}.update".format(self.ky_cell_out)],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())
        self.join3 = AddJoin(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                add_join_residuals=([], []),
                add_join=(
                    [
                        "{:s}.update".format(self.ky_aggout),
                        "{:s}.update".format(self.ky_cell_out),
                    ],
                    [self.ky_aggout],
                ),
            ),
        ).set(self.device, xargs=(), xkargs=dict())

        # Get model reset activation.
        self.reset_act = Activation(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                act_residuals=([], []),
                act=([self.ky_reset_out], [self.ky_reset_out]),
            ),
        ).set(
            self.device, xargs=(), xkargs=dict(activation="sigmoid"),
        )

        # Get model update activation.
        self.update_act = Activation(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                act_residuals=([], []),
                act=([self.ky_update_out], [self.ky_update_out]),
            ),
        ).set(
            self.device, xargs=(), xkargs=dict(activation="sigmoid"),
        )

        # Get model reset activation.
        self.cell_act = Activation(
            self.ROOT,
            sub=True, dtype=self.DTYPE_NAME, iokeys=dict(
                act_residuals=([], []),
                act=([self.ky_cell_out], [self.ky_cell_out]),
            ),
        ).set(
            self.device, xargs=(), xkargs=dict(activation="tanh"),
        )

    def __initialize__(
        self: GRU,
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

        # Initialize recursively.
        self.reset_isub.initialize(
            self.rng.get_state(),
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.reset_hsub.initialize(
            self.rng.get_state(),
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.update_isub.initialize(
            self.rng.get_state(),
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.update_hsub.initialize(
            self.rng.get_state(),
            xargs=xkargs["gate"]["xargs"], xkargs=xkargs["gate"]["xkargs"],
        )
        self.cell_isub.initialize(
            self.rng.get_state(),
            xargs=xkargs["cell"]["xargs"], xkargs=xkargs["cell"]["xkargs"],
        )
        self.cell_hsub.initialize(
            self.rng.get_state(),
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

            # Get essential sequence info.
            sample_length = cast(int, input["$batch_length"].item())
            batch_size = cast(int,input["$batch_size"].item())

            # Get essential recurrent transient buffer and expand batch
            # dimension by batch size.
            transient = {}
            tensor = self.cell_hsub_nullout(self.device)[self.ky_cell_h]
            shape = list(tensor.size())[1:]
            transient[self.ky_aggout] = tensor.expand(batch_size, *shape)

            # Compute directly.
            for t in range(sample_length):
                # Inputs are fixed.
                transient[self.ky_aggout] = self.pytorch.forward(
                    input["{:s}.{:d}".format(self.ky_input_i, t)],
                    transient[self.ky_aggout],
                )

                # Get dynamic output.
                transient["{:s}.{:d}".format(self.ky_output, t)] = (
                    transient[self.ky_aggout]
                )

            # Fetch static and dynamic outputs.
            for key in self.ky_staouts:
                output[key] = transient[key]
            for t in range(sample_length):
                for key in self.ky_dynouts:
                    output["{:s}.{:d}".format(key, t)] = (
                        transient["{:s}.{:d}".format(key, t)]
                    )
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

        # Super.
        GRU.configure(self, xargs, xkargs)

        # Save necessary attributes.
        self.num_inputs = xkargs["num_inputs"]
        self.num_outputs = xkargs["num_outputs"]
        self.no_bias = xkargs["no_bias"]

        # Allocate parameters.
        self.pytorch = torch.nn.GRUCell(
            input_size=self.num_inputs, hidden_size=self.num_outputs,
            bias=not self.no_bias,
        ).to(self.device)
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

        # Pre-fetch IO direction for consistency.
        (self.ky_input_i,), (_,) = self.cell_isub.IOKEYS["linear"]

        # Pre-fetch null function for consistency.
        self.cell_hsub_nullout = self.cell_hsub.nullout

    def __initialize__(
        self: __GRU__,
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
        GRU.__initialize__(self, xargs=xargs, xkargs=xkargs)

        # Merge matrices to fit PyTorch.
        weight_ih = getattr(torch, "cat")([
            cast(Linear, self.reset_isub).weight.data,
            cast(Linear, self.update_isub).weight.data,
            cast(Linear, self.cell_isub).weight.data,
        ], dim=0)
        weight_hh = getattr(torch, "cat")([
            cast(Linear, self.reset_hsub).weight.data,
            cast(Linear, self.update_hsub).weight.data,
            cast(Linear, self.cell_hsub).weight.data,
        ], dim=0)
        bias_ih = getattr(torch, "cat")([
            cast(Linear, self.reset_isub).bias.data,
            cast(Linear, self.update_isub).bias.data,
            cast(Linear, self.cell_isub).bias.data,
        ], dim=0)
        bias_hh = getattr(torch, "cat")([
            cast(Linear, self.reset_hsub).bias.data,
            cast(Linear, self.update_hsub).bias.data,
            cast(Linear, self.cell_hsub).bias.data,
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
        del self.parameter.submodels["reset_join"]
        del self.parameter.submodels["update_join"]
        del self.parameter.submodels["cell_join1"]
        del self.parameter.submodels["cell_join2"]
        del self.parameter.submodels["join1"]
        del self.parameter.submodels["join2"]
        del self.parameter.submodels["join3"]
        del self.reset_isub
        del self.reset_hsub
        del self.update_isub
        del self.update_hsub
        del self.cell_isub
        del self.cell_hsub
        del self.reset_join
        del self.update_join
        del self.cell_join1
        del self.cell_join2
        del self.join1
        del self.join2
        del self.join3