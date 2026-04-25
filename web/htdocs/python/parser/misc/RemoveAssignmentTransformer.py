import libcst
from .VisitorsWithStack import TransformerWithStack


class RemoveAssignmentTransformer(TransformerWithStack):
    """Remove a top-level assignment by name."""

    def __init__(self, name):
        super().__init__()
        self._name = name
        self.removed = False

    def leave_SimpleStatementLine(self, original_node, updated_node):
        # Module body level (stack = [Module, SimpleStatementLine])
        if len(self.stack) != 1:
            return updated_node

        if len(updated_node.body) == 1 and isinstance(updated_node.body[0], libcst.Assign):
            for target in updated_node.body[0].targets:
                if isinstance(target.target, libcst.Name) and target.target.value == self._name:
                    self.removed = True
                    return libcst.RemovalSentinel.REMOVE

        return updated_node
