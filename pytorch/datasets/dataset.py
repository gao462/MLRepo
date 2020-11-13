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
import pytorch.filesys as filesys


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Dataset Virtual Objects >>
# The virtual dataset protoype for any dataset types.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Dataset(abc.ABC):
    r"""
    Virtual class for dataset.
    """
    def __init__(
        self: Dataset,
        root: str,
        *args: VarArg,
        dtype: str, pin: Dict[str, Union[str, None]],
        **kargs: VarArg,
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
        - pin
            A dict mapping relative-to-root file path to their MD5.
            When a pinned file is being accessed, it will check MD5 first. If
            the MD5 is satisfied, it is directly loaded. Otherwise, generation
            or processing is required.
            If MD5 is None, it is assumed to be the first time of generation or
            processing, and a warning will be reported to update MD5 value.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.ROOT: Const = root
        self.PIN: Const = pin
        self.DTYPE: Const = getattr(torch, dtype)

        # \
        # ANNOTATE VARIABLES
        # \
        self.memory: List[Dict[str, torch.Tensor]]

        # Allocate dataset memory.
        self.memory = []

    def __len__(
        self: Dataset,
        *args: VarArg,
        **kargs: VarArg,
    ) -> int:
        r"""
        Get length.

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

        # Get memory length.
        return len(self.memory)

    def __getitem__(
        self: Dataset,
        i: int,
        *args: VarArg,
        **kargs: VarArg,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Get length.

        Args
        ----
        - self
        - i
            Index.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Get memory length.
        return self.memory[i]

    def set(
        self: Dataset,
        *args: VarArg,
        config: Dict[str, VarArg],
        **kargs: VarArg,
    ) -> None:
        r"""
        Settle down dataset by given configuration.

        Args
        ----
        - self
        - *args
        - config
            Configuration dict.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Configure dataset with given arguments.
        self.configure(config)

        # Get relative file path.
        relative = self.relative()
        absolute = os.path.join(self.ROOT, relative)

        # Settle down dataset.
        if (relative in self.PIN):
            # Check pin, save and load.
            md5 = self.PIN[relative]
            if (md5 is None):
                self.save(absolute, md5=md5)
                warning("\"{:s}\" is on-require dataset.", absolute)
            elif (len(md5) > 0 and md5 == filesys.md5(absolute)):
                pass
            else:
                self.save(absolute, md5=md5)
            self.load(absolute)
        else:
            error("\"{:s}\" is not cached in dataset.", relative)
            raise RuntimeError

    @abc.abstractmethod
    def configure(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def relative(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...

    def save(
        self: Dataset,
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

        # Ensure saving directory.
        filesys.ensure_dir(os.path.dirname(path))

        # Skip null base name
        if (len(os.path.basename(path)) == 0):
            warning("Null base \"{:s}\" saving is skipped.", path)
            return
        else:
            pass

        # Aggregate tensor data.
        debug("Aggregating for \"{:s}\".", path)
        tensors = self.aggregate()

        # Save data to given path.
        torch.save(tensors, path)

        # Check MD5 if it is required.
        if (md5 is None):
            pass
        elif (len(md5) == 0):
            warning(
                "\"{:s}\" updates \"MD5\" to \"\033[35;1m{:s}\033[0m\".",
                path, filesys.md5(path),
            )
        elif (filesys.md5(path) == md5):
            pass
        else:
            error(
                "\"{:s}\" does not fit requiring \"MD5\" \"{:s}\".",
                path, md5,
            )
            raise RuntimeError

    def load(
        self: Dataset,
        path: str,
        *args: VarArg,
        **kargs: VarArg,
    ) -> None:
        r"""
        Load dataset memory.

        Args
        ----
        - self
        - path
            Path to load memory.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Skip null base name
        if (len(os.path.basename(path)) == 0):
            warning("Null base \"{:s}\" loading is skipped.", path)
            return
        else:
            pass

        # Load data from given path.
        tensors = torch.load(path)

        # Segregate data.
        debug("Segregating for \"{:s}\".", path)
        self.segregate(tensors)

    @abc.abstractmethod
    def aggregate(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def segregate(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...