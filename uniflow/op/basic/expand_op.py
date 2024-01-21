import copy
from typing import Any, Mapping, Sequence

from uniflow.node import Node
from uniflow.op.op import Op


class ExpandOp(Op):
    """Expand operation class to split nodes into two."""

    def _split(self, value_dict: Mapping[str, Any]) -> Mapping[str, Any]:
        """Split value dict into two parts.

        Args:
            value_dict (Mapping[str, Any]): Input value dict.

        Returns:
            Tuple[Mapping[str, Any], Mapping[str, Any]]: Two output value dicts.
        """
        # print(value_dict)
        n = len(value_dict)
        items = list(value_dict.items())
        return dict(items[:n//2]), dict(items[n//2:])

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Call expand operation.

        Args:
            nodes (Sequence[Node]): Input nodes.

        Returns:
            Sequence[Node]: Output nodes, each input node is expanded into two nodes.
        """
        output_nodes = []
        for node in nodes:
            value_dict_1, value_dict_2 = self._split(node.value_dict)
            expand_1 = Node(name=self.unique_name() + "_1", value_dict=value_dict_1, prev_nodes=[node])
            expand_2 = Node(name=self.unique_name() + "_2", value_dict=value_dict_2, prev_nodes=[node])
            output_nodes.extend([expand_1, expand_2])
        return output_nodes