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
        processed = {key: sample[key] for key in self.KEYS}
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
        static_keys: List[str],
        dynamic_keys: List[str],
        *args: ArgT,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - static_keys
            A list of static keys to keep.
        - dynamic_keys
            A list of dynamic keys to be temporally stacked.
        - *args
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.STATIC_KEYS: Const = static_keys
        self.DYNAMIC_KEYS: Const = dynamic_keys

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
        processed: Dict[str, torch.Tensor]

        # Get static things first.
        processed = {}
        sample = raw[0]
        for key in self.STATIC_KEYS:
            processed[key] = sample[key]

        # Allocate a buffer and fill it.
        batch_size = 0
        for t, sample in enumerate(raw):
            for key in self.DYNAMIC_KEYS:
                processed["{:s}.{:d}".format(key, t)] = sample[key]
                if (batch_size == 0):
                    batch_size = len(sample[key])
                elif (batch_size == len(sample[key])):
                    pass
                else:
                    error(
                        "Sequential batching has different batch size for" \
                        " \"{:s}\".",
                        key,
                    )
                    raise RuntimeError
        processed["$batch_length"] = torch.LongTensor([len(raw)])
        processed["$batch_size"] = torch.LongTensor([batch_size])
        return processed


class GraphStackform(Stackform):
    r"""
    Graph data transform stacking.
    """
    def __init__(
        self: GraphStackform,
        static_keys: List[str],
        graphic_keys: List[str],
        *args: ArgT,
        vertex: str, adjacency: str, t: bool,
        **kargs: KArgT,
    ) -> None:
        r"""
        Initialize.

        Args
        ----
        - self
        - static_keys
            A list of keys to keep.
        - graphic_keys
            A list of keys to be graphically stacked.
        - *args
        - vertex
            Key of one vertex features.
            It is used to detect number of nodes.
        - adjacency
            Key of adjacency list.
        - t
            If True, tranpose the raw adjacency list.
            The adjacency list is required to be $2 \times n$, while most of
            the time, the raw input is $n \times 2$.
            Thus, the transpose is required.
        - **kargs

        Returns
        -------

        """
        # \
        # ANNOTATE VARIABLES
        # \
        # Save necessary attributes.
        self.STATIC_KEYS: Const = static_keys
        self.GRAPHIC_KEYS: Const = graphic_keys
        self.VEX: Const = vertex
        self.ADJ: Const = adjacency
        self.T: Const = t

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
        buf = {key: [] for key in self.GRAPHIC_KEYS}
        buf[self.ADJ] = []
        node_cnt = 0
        edge_cnt = 0
        node_break_points = [node_cnt]
        edge_break_points = [edge_cnt]
        for sample in raw:
            for key in self.GRAPHIC_KEYS:
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
        processed = {}
        sample = raw[0]
        for key in self.STATIC_KEYS:
            processed[key] = sample[key]
        for key in self.GRAPHIC_KEYS:
            processed[key] = getattr(torch, "cat")(buf[key], dim=0)
        processed["$node_breaks"] = node_breaks
        processed["$edge_breaks"] = edge_breaks

        # Ensure adjacency list is transposed.
        if (self.T):
            processed[self.ADJ] = processed[self.ADJ].t()
        else:
            pass
        return processed