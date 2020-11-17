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
from pytorch.batches.paralf import FunctionalProcess
from pytorch.logging import POSITION


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Sampling Operations >>
# The sampling operations.
# They are parallelable.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Sampling(FunctionalProcess[
    Tuple[int, int], Tuple[int, Dict[str, torch.Tensor]],
]):
    r"""
    Sampling from dataset.
    """
    def init(
        self: Sampling,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Specific initialization.

        Args
        ----
        - self
        - xargs
            Extra arguments to specific initialization.
        - xkargs
            Extra keyword arguments to specific initialization.
        - *args
        - **kargs

        Returns
        -------

        """
        # /
        # ANNOTATE VARIABLES
        # /
        ...

        # Get disk dataset and its transform.
        self.disk = xargs[0]
        self.transform = xargs[1]

    def ending(
        self: Sampling,
        input: Tuple[int, int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> bool:
        r"""
        Check ending signal.

        Args
        ----
        - self
        - input
            Input.
        - *args
        - **kargs

        Returns
        -------

        """

        # Decode input.
        src, dst = input
        return src < 0 or dst < 0

    def run(
        self: Sampling,
        input: Tuple[int, int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Tuple[int, Dict[str, torch.Tensor]]:
        r"""
        Real operations.

        Args
        ----
        - self
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
        ...

        # Decode input.
        src, dst = input

        # Get from disk.
        debug(
            "{:s}\"\033[33mDisk [{:d} ==> {:d}]\033[0m\".",
            self.name, src, dst,
        )

        # Load from disk.
        raw = self.disk[src]

        # Some additional transforms on the loaded sample.
        try:
            obj = self.transform(raw)
            return (dst, cast(Dict[str, torch.Tensor], obj))
        except:
            error(
                "{:s}Fail to transform \"{:s}\".",
                self.name,
                POSITION.format("Disk [{:d}]".format(src)),
            )
            raise RuntimeError

    def fin(
        self: Sampling,
        input: Tuple[int, int],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Tuple[int, Dict[str, torch.Tensor]]:
        r"""
        Final operations.

        Args
        ----
        - self
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
        ...

        # Decode input.
        src, dst = input
        debug("{:s}\"\033[33mDisk [{:d}]\033[0m\" (Fin).", self.name, src)

        # Return a null element.
        return (-1, {})