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
from pytorch.datasets.generate import GenerateDataset


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Dataset Objects >>
# A dataset generating random data.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class EmbeddingDataset(GenerateDataset):
    r"""
    Dataset generating random integers and embeddings.
    """
    def configure(
        self: EmbeddingDataset,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Configure dataset.

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

        # Save necessary attributes.
        self.num_samples = xkargs["num_samples"]
        self.num_embeddings = xkargs["num_embeddings"]
        self.num_features = xkargs["num_features"]

    def generate(
        self: EmbeddingDataset,
        *args: ArgT,
        **kargs: KArgT,
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
            input = getattr(torch, "zeros")(
                1, dtype=getattr(torch, "long"),
            )
            input.random_(0, self.num_embeddings, generator=self.rng)
            target = getattr(torch, "zeros")(
                self.num_features, dtype=self.DTYPE,
            )
            target.uniform_(-1, 1, generator=self.rng)
            self.memory.append({"input": input, "target": target})

    def relative(
        self: EmbeddingDataset,
        *args: ArgT,
        **kargs: KArgT,
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
        return "embedding"

    def aggregate(
        self: EmbeddingDataset,
        *args: ArgT,
        **kargs: KArgT,
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
        self: EmbeddingDataset,
        obj: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
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
        self.memory = obj