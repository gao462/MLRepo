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
import abc

# Add development library to path.
if (os.path.basename(os.getcwd()) == "MLRepo"):
    sys.path.append(os.path.join("."))
else:
    print("Code must strictly work in \"MLRepo\".")
    exit()

# Import logging.
from pytorch.logging import debug, info1, info2, focus, warning, error

# Import dependencies.
from pytorch.datasets.dataset import Dataset


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Dataset Virtual Objects >>
# The virtual dataset protoype for any dataset types.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class GenerateDataset(Dataset):
    r"""
    Virtual class for dataset.
    """
    def save(
        self: GenerateDataset,
        path: str,
        *args: VarArg,
        md5: Union[str, None],
        **kargs: VarArg,
    ) -> None:
        """
        Save dataset memory.

        Args
        ----
        - self
        - path
            Path to save memory.
        - *args
        - md5
            Requiring MD5.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Generate data.
        debug("Generating for \"{:s}\".", path)
        self.generate()

        # Super.
        Dataset.save(self, path, md5=md5)

    @abc.abstractmethod
    def generate(
        self: GenerateDataset,
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
        # VIRTUAL
        # \
        ...