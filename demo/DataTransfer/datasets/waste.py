# Import future.
from __future__ import annotations

# Import typing.
from typing import Any as VarArg
from typing import Final as Const
from typing import Tuple as MultiReturn
from typing import Type, Protocol
from typing import TextIO, BinaryIO
from typing import Union, Tuple, List, Dict, Set, Callable

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
from pytorch.datasets.generate import GenerateDataset


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Dataset Objects >>
# A dataset generating meaningless data.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class WasteDataset(GenerateDataset):
    r"""
    Dataset generating waste data.
    """
    def configure(
        self: WasteDataset,
        config: Dict[str, VarArg],
        *args: VarArg,
        **kargs: VarArg,
    ) -> None:
        r"""
        Configure dataset.

        Args
        ----
        - self
        - config
            Configuration dict.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Save necessary attributes.
        self.rng = config["rng"]
        self.num_samples = config["num_samples"]
        self.num_inputs = config["num_inputs"]

    def generate(
        self: WasteDataset,
        *args: VarArg,
        **kargs: VarArg,
    ) -> None:
        r"""
        Generate dataset memory.

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

        # Generate a list of vectors to memory.
        for _ in range(self.num_samples):
            sample = getattr(torch, "zeros")(self.num_inputs, dtype=self.DTYPE)
            sample.random_(generator=self.rng)
            self.memory.append({"input": sample})

    def relative(
        self: WasteDataset,
        *args: VarArg,
        **kargs: VarArg,
    ) -> str:
        r"""
        Relative path to dataset.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - relative
            Relative path.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Waste data does not need caching.
        return "waste"

    def aggregate(
        self: WasteDataset,
        *args: VarArg,
        **kargs: VarArg,
    ) -> List[Dict[str, torch.Tensor]]:
        r"""
        Aggregate dataset memory into a single object.

        Args
        ----
        - self
        - *args
        - **kargs

        Returns
        -------
        - obj
            Single object.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Create a null object.
        obj = self.memory
        return obj

    def segregate(
        self: WasteDataset,
        obj: List[Dict[str, torch.Tensor]],
        *args: VarArg,
        **kargs: VarArg,
    ) -> None:
        r"""
        Segregate a single object into dataset memory.

        Args
        ----
        - self
        - obj
            Single object.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Create a null object.
        self.memory.extend(obj)