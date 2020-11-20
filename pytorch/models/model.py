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
#
# It uses pure function design with PyTorch for potential transplant to JAX,
# and better compatibility with JIT compiling.
#
# It is virtual a class, but for simulation creation of reproducibilty test,
# some methods are defined as instanciable class methods, for example, loss
# function will be defined for sub model usage.
# Those abstract methods are manually defined to raise errors.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GradModel(abc.ABC):
    r"""
    Virtual class for gradient supporting model.
    """
    # \
    # ANNOTATE VARIABLES
    # \
    main: str

    def __init__(
        self: GradModel,
        root: str,
        *args: ArgT,
        sub: bool, dtype: str,
        iokeys: Dict[str, Tuple[List[str], List[str]]],
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
        - sub
            If True, it is going to be used as sub model, and some logging is
            prohibited.
        - dtype
            Data precision.
        - iokeys
            Computation IO keys in batch.
            It is useful when submodels output something should be passed
            directly rather than processed by the model.
            It is defined in form "section: [(in_key1, out_key1), ...]".
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.SUB: Const = sub
        self.ROOT: Const = root
        self.DTYPE_NAME: Const = dtype
        self.DTYPE: Const = getattr(torch, dtype)
        self.IOKEYS: Const = iokeys

        # Ensure IO keywords.
        main_items = self.main.lower().split("_")
        for key in self.IOKEYS:
            key_items = key.split("_")
            for i in range(len(main_items)):
                if (key_items[i] == main_items[i]):
                    pass
                else:
                    error(
                        "{:s} IO flow requires section name in the form of" \
                        " \"{:s}(_{{name}})*\", but get \"{:s}\".",
                        self.main, self.main.lower(), key,
                    )
                    raise RuntimeError

        # Parse computation IO keys into single items.
        self.__parse__()

    @abc.abstractmethod
    def __parse__(
        self: GradModel,
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
        # VIRTUAL
        # /
        ...

    @abc.abstractmethod
    def __forward__(
        self: GradModel,
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
        # \
        # VIRTUAL
        # \
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
            # VIRTUAL
            # /
            ...

        # Return the function.
        return f

    @abc.abstractmethod
    def __nullin__(
        self: GradModel,
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
        # VIRTUAL
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
            # VIRTUAL
            # /
            ...

        # Return the function.
        return null

    @abc.abstractmethod
    def __nullout__(
        self: GradModel,
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
        # VIRTUAL
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
            # VIRTUAL
            # /
            ...

        # Return the function.
        return null

    def __train__(
        self: GradModel,
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

        Some models may be used as sub models of other models, thus their loss
        functions will be undefined, thus this generation is not abstract, and
        will return a NotImplementedError virtual function by default.

        It must of defined a function $f$ by form:
        $$
        l = f(\theta, y, \hat{y})
        $$
        where $\theta$ is parameter, $y$ is output, and $\hat{y}$ is target.

        It also accepts parameters for parametric loss functions, for example,
        softmax replacements.
        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        def f(
            parameter: Parameter,
            output: Dict[str, torch.Tensor],
            target: Dict[str, torch.Tensor],
            *args: ArgT,
            **kargs: KArgT,
        ) -> torch.Tensor:
            r"""
            Get training loss.

            Args
            ----
            - parameter
                Parameter.
            - output
                Output.
            - target
                Target.
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
            raise NotImplementedError

        # Return the function.
        return f

    def __evaluate__(
        self: GradModel,
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

        It also accepts parameters for parametric loss functions, for example,
        softmax replacements.
        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        def f(
            parameter: Parameter,
            output: Dict[str, torch.Tensor],
            target: Dict[str, torch.Tensor],
            *args: ArgT,
            **kargs: KArgT,
        ) -> torch.Tensor:
            r"""
            Get evaluating loss.

            Args
            ----
            - parameter
                Parameter.
            - output
                Output.
            - target
                Target.
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
            raise NotImplementedError

        # Return the function.
        return f

    @abc.abstractmethod
    def __initialize__(
        self: GradModel,
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
        # VIRTUAL
        # /
        ...

    def set(
        self: GradModel,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> GradModel:
        r"""
        Settle down and register model parameters and sub models.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - model
            Return model itself.
            It is useful when creation and setup are done in the same time.

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

        # Output workflow to logging.
        self.workflow = self.workflow_diffuse()
        _, self.fullname, _ = str(type(self)).split("\'")
        if (self.SUB):
            debug(
                "Workflow of SUB \"\033[35m{:s}\033[0m\" is hidden.",
                self.fullname,
            )
        else:
            debug(
                "Workflow of MAIN \"\033[35;1m{:s}\033[0m\":",
                self.fullname,
            )
            self.workflow_logging()

        # Scan over model attributes by now.
        self.parameter = Parameter()
        for key, val in vars(self).items():
            if (isinstance(val, torch.nn.parameter.Parameter)):
                self.parameter.registar_parameter(key, val)
            elif (isinstance(val, GradModel)):
                if (val.SUB):
                    self.parameter.registar_submodel(key, val.parameter)
                else:
                    error(
                        "Register a non-sub model \"{:s}\"as a sub model.",
                        val.__class__.__name__,
                    )
                    raise RuntimeError
            else:
                pass

        # Construct purified function.
        self.forward = self.__forward__()
        self.nullin = self.__nullin__()
        self.nullout = self.__nullout__()
        self.train = self.__train__()
        self.evaluate = self.__evaluate__()
        return self

    def workflow_diffuse(
        self: GradModel,
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
        for key, val in vars(self).items():
            if (isinstance(val, GradModel)):
                for sub, grouped in val.workflow.items():
                    if (sub == ""):
                        flows[key] = grouped
                    else:
                        flows[key + "." + sub] = grouped
            else:
                pass

        # Output each defined flow.
        flows[""] = []
        for i, (section, (inkeys, outkeys)) in enumerate(self.IOKEYS.items()):
            # Allocate section buffer.
            flows[""].append([])

            # Print a flow section to the buffer.
            for j in range(max(len(inkeys), len(outkeys))):
                # Pad for insufficient keys.
                inkey = inkeys[j] if (j < len(inkeys)) else ""
                outkey = outkeys[j] if (j < len(outkeys)) else ""

                # Output the key flow.
                if (j == 0):
                    flows[""][-1].append((section, inkey, outkey))
                else:
                    flows[""][-1].append(("", inkey, outkey))
        return flows

    def workflow_logging(
        self: GradModel,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Output workflow defined by IO keys to logging.

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
        subflows: Dict[str, List[List[Tuple[str, str, str]]]]

        # Get the output length first.
        max_sub = len("Submodel")
        max_sec = len("Section")
        max_in = len("Input")
        max_out = len("Output")
        for subname, submodel in self.workflow.items():
            max_sub = max(max_sub, len(subname))
            for grouped in submodel:
                for section, inkey, outkey in grouped:
                    max_sec = max(max_sec, len(section))
                    max_in = max(max_in, len(inkey))
                    max_out = max(max_out, len(outkey))

        # Output title.
        debug(
            "\"={:s}={:s}==={:s}====={:s}=\".",
            "=" * max_sub, "=" * max_sec, "=" * max_in, "=" * max_out,
        )
        debug(
            "\" {:s} {:s} | {:s} ==> {:s} \".",
            "Submodel".rjust(max_sub), "Section".rjust(max_sec),
            "Input".rjust(max_in), "Output".ljust(max_out),
        )
        debug(
            "\"={:s}={:s}=+={:s}====={:s}=\".",
            "=" * max_sub, "=" * max_sec, "=" * max_in, "=" * max_out,
        )

        # Output sub models.
        for i, (subname, submodel) in enumerate(self.workflow.items()):
            # Hightlight the main model.
            if (subname == ""):
                highlight = ";1"
            else:
                highlight = ""

            # Output each defined flow.
            for j, grouped in enumerate(submodel):
                # Output subname only at the beginning.
                if (j == 0):
                    pass
                else:
                    subname = ""

                # Output focusing section head.
                section, inkey, outkey = grouped[0]
                debug(
                    "\" {:s} {:s} | \033[34{highlight:s}m{:s}\033[0m ==>" \
                    " \033[32{highlight:s}m{:s}\033[0m \".",
                    subname.rjust(max_sub), section.rjust(max_sec),
                    inkey.rjust(max_in), outkey.ljust(max_out),
                    highlight=highlight,
                )

                # Output remaining focusing section.
                for section, inkey, outkey in grouped[1:]:
                    debug(
                        "\" {:s} {:s} | \033[34{highlight:s}m{:s}\033[0m" \
                        "     \033[32{highlight:s}m{:s}\033[0m \".",
                        "".rjust(max_sub), section.rjust(max_sec),
                        inkey.rjust(max_in), outkey.ljust(max_out),
                        highlight=highlight,
                    )

                # Output inner bar break.
                if (j == len(submodel) - 1):
                    pass
                else:
                    debug(
                        "\" {:s}-{:s}-+-{:s}-----{:s}-\".",
                        " " * max_sub, "-" * max_sec, "-" * max_in,
                        "-" * max_out,
                    )

            # Output bar break.
            if (i == len(self.workflow) - 1):
                debug(
                    "\"={:s}={:s}==={:s}====={:s}=\".",
                    "=" * max_sub, "=" * max_sec, "=" * max_in, "=" * max_out,
                )
            else:
                debug(
                    "\"-{:s}-{:s}-+-{:s}-----{:s}-\".",
                    "-" * max_sub, "-" * max_sec, "-" * max_in, "-" * max_out,
                )

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

    def initialize(
        self: GradModel,
        rng: torch._C.Generator,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> GradModel:
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
        - model
            Return model itself.
            It is useful when creation, setup and initialization are done in
            the same time.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Dive into real initialization.
        self.__initialize__(rng, xargs=xargs, xkargs=xkargs)

        # Output initialized parameters
        if (self.SUB):
            pass
        else:
            info1(
                "Initialize {:d} parameters for MAIN" \
                " \"\033[35;1m{:s}\033[0m\".",
                self.parameter.num(), self.fullname,
            )
        return self

    def training(
        self: GradModel,
        batch: Dict[str, torch.Tensor],
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

        # Get output and training loss.
        self.batch = batch
        self.output = self.forward(self.parameter, self.batch)
        self.loss = self.train(self.parameter, self.output, self.batch)

        # Utilize autograd.
        getattr(self.loss, "backward")()
        return self.loss

    def evaluating(
        self: GradModel,
        batch: Dict[str, torch.Tensor],
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

        # Get output and training loss.
        self.batch = batch
        self.output = self.forward(self.parameter, self.batch)
        self.loss = self.evaluate(self.parameter, self.output, self.batch)
        return self.loss


class Parameter(object):
    r"""
    Parameter object.
    """
    def __init__(
        self: Parameter,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

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
        self.parameters: Dict[str, torch.nn.parameter.Parameter]
        self.submodels: Dict[str, Parameter]

        # Allocate tracers.
        self.parameters = {}
        self.submodels = {}

    def __getitem__(
        self: Parameter,
        name: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.nn.parameter.Parameter:
        r"""
        Get a named parameter.

        Args
        ----
        - self
        - name
            Parameter name.
            If it is a parameter in a sub model, the name should be of form
            "submodel.name".
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Get parameter tensor directly or recursively.
        if (name in self.parameters):
            return self.parameters[name]
        else:
            submodel, name = name.split(".", 1)
            return self.submodels[submodel][name]

    def sub(
        self: Parameter,
        name: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> Parameter:
        r"""
        Get a named sub model.

        Args
        ----
        - self
        - name
            Submodel name.
            If it is a submodel in a sub model, the name should be of form
            "submodel.name".
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Get sub model directly or recursively.
        if (name in self.submodels):
            return self.submodels[name]
        else:
            submodel, name = name.split(".", 1)
            return self.submodels[submodel].sub(name)

    def registar_parameter(
        self: Parameter,
        name: str,
        parameter: torch.nn.parameter.Parameter,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Register a parameter.

        Args
        ----
        - self
        - name
            Parameter name.
        - parameter
            Parameter tensor.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Save to dict.
        self.parameters[name] = parameter

    def registar_submodel(
        self: Parameter,
        name: str,
        submodel: Parameter,
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Register a submodel.

        Args
        ----
        - self
        - name
            submodel name.
        - submode
            Submodel.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Save to dict.
        self.submodels[name] = submodel

    def tolist(
        self: Parameter,
        *args: ArgT,
        **kargs: KArgT,
    ) -> List[torch.nn.parameter.Parameter]:
        r"""
        Transform into a list of parameters.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - memory
            A list of parameters.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        memory: List[torch.nn.parameter.Parameter]

        # Extend recursively.
        memory = []
        for submodel in self.submodels.values():
            memory.extend(submodel.tolist())

        # Append parameters.
        for parameter in self.parameters.values():
            memory.append(parameter)
        return memory

    def num(
        self: Parameter,
        *args: ArgT,
        **kargs: KArgT,
    ) -> int:
        r"""
        Get number of parameters.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - num_params
            Number of parameters.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        memory: List[torch.nn.parameter.Parameter]

        # Extend recursively.
        num_params = 0
        for submodel in self.submodels.values():
            num_params += submodel.num()

        # Append parameters.
        for parameter in self.parameters.values():
            num_params += parameter.numel()
        return num_params


class ForwardFunction(Protocol):
    r"""
    Forward function type.
    """
    def __call__(
        self: ForwardFunction,
        parameter: Parameter,
        input: Dict[str, torch.Tensor],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - parameter
            Parameter.
        - input
            input.
        - *args
        - **kargs

        Returns
        -------
        - output
            Output.

        """
        # \
        # VIRTUAL
        # \
        ...


class NullFunction(Protocol):
    r"""
    Null IO generation function type.
    """
    def __call__(
        self: NullFunction,
        device: str,
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - self
        - device
            Device
        - *args
        - **kargs

        Returns
        -------
        - output
            Output.

        """
        # \
        # VIRTUAL
        # \
        ...


class LossFunction(Protocol):
    r"""
    Loss function type.
    """
    def __call__(
        self: LossFunction,
        parameter: Parameter,
        output: Dict[str, torch.Tensor],
        target: Dict[str, torch.Tensor],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Call as function.

        Args
        ----
        - self
        - output
            Output.
        - target
            Target.
        - *args
        - **kargs

        Returns
        -------
        - loss
            Loss.

        """
        # \
        # VIRTUAL
        # \
        ...