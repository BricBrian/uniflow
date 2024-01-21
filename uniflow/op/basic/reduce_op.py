import copy
import itertools
from typing import Any, Mapping, Sequence, Callable

from uniflow.node import Node
from uniflow.op.op import Op


class ReduceOp(Op):
    """Reduce operation class to merge two nodes into one."""

    def _merge(self, value_dict_1: Mapping[str, Any], value_dict_2: Mapping[str, Any]) -> Mapping[str, Any]:
        """Default merge function to combine two value_dicts.

        Args:
            value_dict_1 (Mapping[str, Any]): First value dict.
            value_dict_2 (Mapping[str, Any]): Second value dict.

        Returns:
            Mapping[str, Any]: Merged value dict.
        """
        merged_dict = {}
        keys1 = list(value_dict_1.keys())
        keys2 = list(value_dict_2.keys())

        max_len = max(len(keys1), len(keys2))
        for i in range(max_len):
            key1 = keys1[i] if i < len(keys1) else None
            key2 = keys2[i] if i < len(keys2) else None

            value1 = value_dict_1.get(key1, 'N/A') if key1 is not None else 'N/A'
            value2 = value_dict_2.get(key2, 'N/A') if key2 is not None else 'N/A'
            if key1 is None:
                merged_key = f"{key2}"
                merged_value = f"{value2}"
                merged_dict[merged_key] = merged_value
            else:
                merged_key = f"{key1} {key2}"
                merged_value = f"{value1} {value2}"
                merged_dict[merged_key] = merged_value
        return merged_dict

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Call reduce operation.

        Args:
            nodes (Sequence[Node]): Input nodes, expected to be expand_1 and expand_2.

        Returns:
            Sequence[Node]: Output node, reduce_1.
        """
        if len(nodes) != 2:
            raise ValueError("ReduceOp expects exactly two input nodes.")

        value_dict_1 = nodes[0].value_dict
        value_dict_2 = nodes[1].value_dict

        merged_value_dict = self._merge(value_dict_1, value_dict_2)
        reduce_1 = Node(name=self.unique_name(), value_dict=merged_value_dict, prev_nodes=nodes)
        
        return [reduce_1]
