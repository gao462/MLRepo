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
from pytorch.reforms.transform import Transform


# =============================================================================
# *****************************************************************************
# -----------------------------------------------------------------------------
# << Transform Stacking Objects >>
# Transforms that stacking a batch of tensors with the same keyword into a
# single tensor with the same keyword.
# It commonly stack a list of N dicts of K-dim tensors into a list of 1 dict
# of (K+1)-dim tensors.
# The first dimension is extended as batch dimension.
#
# It is possible to have different cases, for example, graph stacking just
# merge batch graphs into a new large graph which does not extend batch
# dimension.
# -----------------------------------------------------------------------------
# *****************************************************************************
# =============================================================================


class Stackform(object):
    r"""
    Virtual class for data transform stacking.
    """
    @abc.abstractmethod
    def __init__(
        self: Stackform,
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
        # \
        # VIRTUAL
        # \
        ...

    @abc.abstractmethod
    def __call__(
        self: Stackform,
        raw: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - self
        - raw
            Raw data before processing.
        - *args
        - **kargs

        Returns
        -------
        - processed
            Processed data.

        """
        # \
        # VIRTUAL
        # \
        ...


class NotStackform(Stackform):
    r"""
    Data transform stacking by unravel the only sample.
    """
    def __init__(
        self: NotStackform,
        keys: List[str],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - keys
            A list of keys to be stacked.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.KEYS: Const = keys

    def __call__(
        self: NotStackform,
        raw: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - self
        - raw
            Raw data before processing.
        - *args
        - **kargs

        Returns
        -------
        - processed
            Processed data.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        buf: Dict[str, List[torch.Tensor]]

        # This only works for batch size 1.
        if (len(raw) == 1):
            pass
        else:
            error("Not-batching can only unravel batch size 1.")
            raise RuntimeError

        # Get output directly.
        sample = raw[0]
        processed = {
            key: sample[key]
            for key in self.KEYS
        }
        return processed


class NaiveStackform(Stackform):
    r"""
    Naive data transform stacking.
    """
    def __init__(
        self: NaiveStackform,
        keys: List[str],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - keys
            A list of keys to be stacked.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.KEYS: Const = keys

    def __call__(
        self: NaiveStackform,
        raw: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - self
        - raw
            Raw data before processing.
        - *args
        - **kargs

        Returns
        -------
        - processed
            Processed data.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        buf: Dict[str, List[torch.Tensor]]

        # Allocate a buffer and fill it.
        buf = {key: [] for key in self.KEYS}
        for sample in raw:
            for key in self.KEYS:
                buf[key].append(sample[key])

        # Stack directly.
        processed = {
            key: getattr(torch, "stack")(val)
            for key, val in buf.items()
        }
        return processed


class SeqStackform(Stackform):
    r"""
    Sequence data transform stacking.
    """
    def __init__(
        self: SeqStackform,
        keys: List[str],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - keys
            A list of keys to be stacked.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.KEYS: Const = keys

    def __call__(
        self: SeqStackform,
        raw: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - self
        - raw
            Raw data before processing.
        - *args
        - **kargs

        Returns
        -------
        - processed
            Processed data.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        buf: Dict[str, List[torch.Tensor]]

        # Allocate a buffer and fill it.
        buf = {key: [] for key in self.KEYS}
        for sample in raw:
            for key in self.KEYS:
                buf[key].append(sample[key])

        # Stack directly.
        processed = {
            key: getattr(torch, "stack")(val, dim=1)
            for key, val in buf.items()
        }
        return processed


class GraphStackform(Stackform):
    r"""
    Graph data transform stacking.
    """
    def __init__(
        self: GraphStackform,
        keys: List[str],
        *args: ArgT,
        vertex: str, adjacency: str,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - keys
            A list of keys to be stacked.
        - *args
        - vertex
            Key of one vertex features.
            It is used to detect number of nodes.
        - adjacency
            Key of adjacency list.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.KEYS: Const = keys
        self.VEX: Const = vertex
        self.ADJ: Const = adjacency

    def __call__(
        self: GraphStackform,
        raw: List[Dict[str, torch.Tensor]],
        *args: ArgT,
        **kargs: KArgT,
    ) -> Dict[str, torch.Tensor]:
        r"""
        Call as function.

        Args
        ----
        - self
        - raw
            Raw data before processing.
        - *args
        - **kargs

        Returns
        -------
        - processed
            Processed data.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        buf: Dict[str, List[torch.Tensor]]

        # Allocate a buffer and fill it.
        buf = {key: [] for key in self.KEYS}
        buf[self.ADJ] = []
        node_cnt = 0
        edge_cnt = 0
        node_break_points = [node_cnt]
        edge_break_points = [edge_cnt]
        for sample in raw:
            for key in self.KEYS:
                buf[key].append(sample[key])
            buf[self.ADJ].append(sample[self.ADJ] + node_cnt)
            num_nodes = len(sample[self.VEX])
            num_edges = len(sample[self.ADJ])
            node_cnt += num_nodes
            edge_cnt += num_edges
            node_break_points.append(node_cnt)
            edge_break_points.append(edge_cnt)
        node_breaks = torch.LongTensor(node_break_points)
        edge_breaks = torch.LongTensor(edge_break_points)

        # Stack directly.
        processed = {
            key: getattr(torch, "cat")(val, dim=0)
            for key, val in buf.items()
        }
        processed["$node.breaks"] = node_breaks
        processed["$edge.breaks"] = edge_breaks

        # Ensure adjacency list is transposed.
        processed[self.ADJ] = processed[self.ADJ].t()
        return processed