"""Flow class."""
from typing import Any, Dict, Sequence

from uniflow.constants import TRANSFORM
from uniflow.flow.flow import Flow
from uniflow.node import Node
from uniflow.op.basic.expand_op import ExpandOp
from uniflow.op.basic.reduce_op import ReduceOp
from uniflow.op.prompt import PromptTemplate


class ExpandReduceFlow(Flow):
    """Copy flow class.

    This is a demo flow does nothing but copy the input nodes.
    """

    TAG = TRANSFORM

    def __init__(
        self,
        prompt_template: PromptTemplate,
        model_config: Dict[str, Any],
    ) -> None:  # pylint: disable=useless-parent-delegation
        """Initialize ExpandReduceFlow class."""
        self._expand_op = ExpandOp(name="extend_op")
        self._reduce_op = ReduceOp(name="reduce_op")
        super().__init__()

    def run(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Run ExpandReduceFlow.

        Args:
            nodes (Sequence[Node]): Nodes to run.

        Returns:
            Sequence[Node]: Nodes after running.
        """
        # First, expand each node into two nodes
        expanded_nodes = []
        expanded_nodes.extend(self._expand_op(nodes))

        # Then, combine each pair of expanded nodes back into one node
        reduced_nodes = []
        for i in range(0, len(expanded_nodes), 2):
            reduced_nodes.append(self._reduce_op(expanded_nodes[i:i+2])[0])

        return reduced_nodes
