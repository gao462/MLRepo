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
import itertools

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


class GraphDataset(GenerateDataset):
    r"""
    Dataset generating random Erdos-Renyi graph with node features and with or
    with edge features.
    """
    def configure(
        self: GraphDataset,
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
        self.min_nodes = xkargs["min_nodes"]
        self.max_nodes = xkargs["max_nodes"]
        self.num_node_inputs = xkargs["num_node_inputs"]
        self.num_edge_inputs = xkargs["num_edge_inputs"]
        self.num_node_outputs = xkargs["num_node_outputs"]
        self.er_p = xkargs["er_p"]

    def generate(
        self: GraphDataset,
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
        for num_nodes in range(self.min_nodes, self.max_nodes):
            node_input, adj_input, edge_input, node_target = self.erdos_renyi(
                self.rng, num_nodes,
                num_node_inputs=self.num_node_inputs,
                num_edge_inputs=self.num_edge_inputs,
                num_node_outputs=self.num_node_outputs,
                er_p=self.er_p,
            )
            self.memory.append({
                "node_input": node_input,
                "adj_input": adj_input, "edge_input": edge_input,
                "node_target": node_target,
            })

    def erdos_renyi(
        self: GraphDataset,
        rng: torch._C.Generator, num_nodes: int,
        *args: ArgT,
        num_node_inputs: int, num_edge_inputs: int, num_node_outputs: int,
        er_p: float,
        **kargs: KArgT,
    ) -> MultiReturn[
        torch.Tensor,
        torch.LongTensor, torch.Tensor,
        torch.Tensor,
    ]:
        r"""
        Erdos-Renyi random graph.

        Args
        ----
        - self
        - rng
            Random number generator.
        - num_nodes
            Number of nodes.
        - *args
        - num_node_inputs
            Number of node inputs.
        - num_edge_inputs
            Number of edge inputs.
        - num_node_outputs
            Number of node outputs.
        - **kargs

        Returns
        -------
        - node_input
            Node feature input.
        - adj_input
            Adjacency matrix input.
        - edge_input
            Edge feature input.
        - node_target
            Node target.

        """
        # \
        # ANNOTATE VARIABLES
        # \
        adj_input: torch.LongTensor
        edge_input: torch.Tensor

        # Generate all low-high edges.
        node_indices = list(range(num_nodes))
        edge_indices = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                edge_indices.append((i, j))
        adj_input = torch.LongTensor(edge_indices)

        # Randomly selct edges from them.
        distribution = getattr(torch, "zeros")(len(edge_indices))
        distribution.uniform_(0, 1, generator=rng)
        select = (distribution > er_p).nonzero(as_tuple=True)[0].tolist()
        adj_input = cast(torch.LongTensor, adj_input[select])

        # Erdos-Renyi is symmetric.
        adj_input = getattr(torch, "cat")(
            [adj_input, adj_input[:, [1, 0]]], dim=0,
        )

        # Assign node input features.
        node_input = getattr(torch, "zeros")(
            num_nodes, num_node_inputs, dtype=self.DTYPE,
        )
        node_input.uniform_(-1, 1, generator=rng)

        # Assign edge input features.
        edge_input = getattr(torch, "zeros")(
            len(adj_input), max(1, num_edge_inputs), dtype=self.DTYPE,
        )
        edge_input.uniform_(-1, 1, generator=rng)

        # Assign node targetfeatures.
        node_target = getattr(torch, "zeros")(
            num_nodes, num_node_outputs, dtype=self.DTYPE,
        )
        node_target.uniform_(-1, 1, generator=rng)
        return node_input, adj_input, edge_input, node_target

    def relative(
        self: GraphDataset,
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
        return "graph"

    def aggregate(
        self: GraphDataset,
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
        self: GraphDataset,
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