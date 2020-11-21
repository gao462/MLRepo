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
import pytorch.filesys as filesys


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Dataset Virtual Objects >>
# The virtual dataset protoype for any dataset types.
# For best utilization of PyTorch offical optimization, it is inherited from
# PyTorch abstract dataset class. It makes no difference in implementation from
# inheriting from object.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Dataset(object):
    r"""
    Virtual class for dataset.
    """
    def __init__(
        self: Dataset,
        root: str,
        *args: ArgT,
        dtype: str, pin: Dict[str, Union[str, None]],
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
        *args: ArgT,
        **kargs: KArgT,
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
        *args: ArgT,
        **kargs: KArgT,
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

        # Get item from memory.
        return self.memory[i]

    def set(
        self: Dataset,
        rngmem: torch.Tensor,
        *args: ArgT,
        xargs: Tuple[Naive, ...], xkargs: Dict[str, Naive],
        **kargs: KArgT,
    ) -> Dataset:
        r"""
        Settle down dataset by given configuration.

        Args
        ----
        - self
        - rngmem
            Random number generator memory to update.
        - *args
        - xargs
            Extra arguments to specific configuration.
        - xkargs
            Extra keyword arguments to specific configuration.
        - **kargs

        Returns
        -------
        - dataset
            Return dataset itself.
            It is useful when creation and setup are done in the same time.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        ...

        # Save necessary attribtues.
        self.rng = getattr(torch, "Generator")()
        self.rng.set_state(rngmem)

        # Configure dataset with extra arguments.
        self.configure(xargs, xkargs)

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
        return self

    @abc.abstractmethod
    def configure(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def relative(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...

    def save(
        self: Dataset,
        path: str,
        *args: ArgT,
        md5: Union[str, None],
        **kargs: KArgT,
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
        getattr(torch, "save")(tensors, path)

        # Check MD5 if it is required.
        if (md5 is None):
            pass
        elif (len(md5) == 0):
            warning(
                "\"{:s}\" updates \"MD5\" to \"\033[35;1m{:s}\033[0m\".",
                os.path.join(
                    os.path.dirname(path),
                    "\033[35;1m{:s}\033[0m".format(os.path.basename(path)),
                ),
                filesys.md5(path),
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
        *args: ArgT,
        **kargs: KArgT,
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
        tensors = getattr(torch, "load")(path)

        # Segregate data.
        debug("Segregating for \"{:s}\".", path)
        self.segregate(tensors)

    @abc.abstractmethod
    def aggregate(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def segregate(
        self: Dataset,
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
        # VIRTUAL
        # \
        ...