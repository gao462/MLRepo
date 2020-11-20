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
import time

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from pytorch.batches.batch import Batch
from pytorch.models.model import Parameter


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Benchmark >>
# Benchmark to check forward or backward computations on a full synthetic batch
# so that a model is reproduced within required error tolerance from the target
# model.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class BackwardBenchmark(object):
    r"""
    Benchmark for backward computations.
    """
    def __init__(
        self: BackwardBenchmark,
        bat: Batch, repcls: type, tarcls: type,
        checkon: List[Tuple[
            Tuple[str, List[Tuple[int, int]]],
            Tuple[str, List[Tuple[int, int]]],
        ]],
        *args: ArgT,
        iokeys: Dict[str, Tuple[List[str], List[str]]],
        set_xargs: Tuple[Naive, ...], set_xkargs: Dict[str, Naive],
        ini_xargs: Tuple[Naive, ...], ini_xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize

        Args
        ----
        - self
        - bat
            Batching.
        - repcls
            Reproduced class.
        - tarcls
            Targeting class.
        - checkon
            Check backward result on given parameter name and tensor slice.
        - *args
        - iokeys
            Model IO flow.
        - set_xargs
            Extra arguments for model setup.
        - set_xkargs
            Extra keyword arguments for model setup.
        - ini_xargs
            Extra arguments for model parameter initialization.
        - ini_xkargs
            Extra keyword arguments for model parameter initialization.
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Tolerance is defined by benchmark.
        tol = 1e-6

        # Get randomness
        seed = 47
        rng = getattr(torch, "Generator")()
        rng.manual_seed(47)
        rngmem = rng.get_state()

        # Get reproduced model.
        rng.set_state(rngmem)
        repmod = repcls(
            "../FastModel/Reproduce",
            sub=False, dtype="float32",
            iokeys=iokeys,
        ).set(
            xargs=set_xargs, xkargs=set_xkargs,
        ).initialize(
            rng, xargs=ini_xargs, xkargs=ini_xkargs,
        )
        info1(
            "Reproduced model \"\033[35;1m{:s}\033[0m\" is ready.",
            repmod.fullname,
        )

        # Get target model.
        rng.set_state(rngmem)
        tarmod = tarcls(
            "../FastModel/Reproduce",
            sub=False, dtype="float32",
            iokeys=iokeys,
        ).set(
            xargs=set_xargs, xkargs=set_xkargs,
        ).initialize(
            rng, xargs=ini_xargs, xkargs=ini_xkargs,
        )
        info1(
            "Targeting model \"\033[35;1m{:s}\033[0m\" is ready.",
            tarmod.fullname,
        )

        # Get a full batch.
        info1("Batching is running.")
        bat.refresh(xargs=(), xkargs={})
        signal, batch = bat.next()
        if (signal):
            pass
        else:
            error("Reproducibility should be tested on full batch.")
            raise RuntimeError
        info2("Batching is terminated.")

        # Forward and backward
        info1("Reproduced models are running.")
        repmod.training(batch)
        info2("Reproduced models are terminated.")
        info1("Targeting models are running.")
        tarmod.training(batch)
        info2("Targeting models are terminated.")

        # Check gradients and report.
        for (repname, repslices), (tarname, tarslices) in checkon:
            repgrad = self.fetch(repmod.parameter, repname, repslices)
            targrad = self.fetch(tarmod.parameter, tarname, tarslices)
            error = (repgrad - targrad).abs().max().item()
            if (error < tol):
                focus(
                    "Reproduced gradient \"{:s}[{:s}]\"" \
                    " \"\033[32;1mFITS\033[0m\" targeting gradient" \
                    " \"{:s}[{:s}]\" ({:.6f}).",
                    repname,
                    ", ".join([
                        "{:d}:{:d}".format(start, end)
                        for start, end in repslices
                    ]),
                    tarname,
                    ", ".join([
                        "{:d}:{:d}".format(start, end)
                        for start, end in tarslices
                    ]),
                    error,
                )
            else:
                warning(
                    "Reproduced gradient \"{:s}[{:s}]\"" \
                    " \"\033[31;1mDOES NOT FIT\033[0m\" targeting gradient" \
                    " \"{:s}[{:s}]\" ({:.6f}).",
                    repname,
                    ", ".join([
                        "{:d}:{:d}".format(start, end)
                        for start, end in repslices
                    ]),
                    tarname,
                    ", ".join([
                        "{:d}:{:d}".format(start, end)
                        for start, end in tarslices
                    ]),
                    error,
                )

    def fetch(
        self: BackwardBenchmark,
        parameter: Parameter,
        name: str, slices: List[Tuple[int, int]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> torch.Tensor:
        r"""
        Fetch a gradient.

        Args
        ----
        - self
        - parameter
            Parameter.
        - name
            Name.
        - slices
            Indexing slices.
        - *args
        - **kargs

        Returns
        -------
        - grad
            Gradient tensor.

        """
        # /
        # ANNOTATE VARIABLES
        # /
        grad: torch.Tensor

        # Fetch the gradient.
        grad = parameter[name].grad
        for start, end in slices:
            grad = grad[start:end]
        return grad