import json
import libcst
import uuid
from .Arguments import Arguments

class Action:
    def __init__(self, input, element_node):
        self.__id = str(uuid.uuid4())

        self.node = element_node
        self.input = input 

        self._evaluate_node()
        self.client = self._determine_client()

        # Buffers
        self.__arguments = None

    def _evaluate_node(self):
        # Is it a function call? Most actions are.
        if isinstance(self.node.value, libcst.Call):
            self.name = self.node.value.func.value
            
        # No call: Search if there is an assignment with the name
        elif isinstance(self.node.value, libcst.Name):
            self.name = self.node.value.value

    # Unique ID
    def id(self):
        return self.__id

    # Returns a json encoded list of arguments of the node, represented by dicts.
    def arguments(self):
        if self.__arguments:
            return json.dumps(self.__arguments)
        
        visitor = Arguments()
        self.node.value.visit(visitor)
        self.__arguments = visitor.result

        return json.dumps(self.__arguments)

    # Returns the value of an argument as string, or None if not found
    def argument(self, name):
        if not self.__arguments:
            self.arguments()

        for arg in self.__arguments:
            if arg["name"] == name:
                return arg["value"]
            
        return None

    # Removes the action from the tree.
    def remove(self):
        self.__arguments = None
        self.input.remove_action(self.node)

    # If the action is connected to a pager, this returns the page ID, or None if not.
    def page(self):
        ec = self.argument("enable_callback")
        if not ec:
            return None
        
        pager = self.input.parser.pager()
        if not pager:
            return None
        
        if ec != pager.name + ".enable_callback":
            return None
        
        return self.argument("id")

    # Determine the client
    def _determine_client(self):
        import_statement = self.input.parser.determine_import_statement(self)
        if not import_statement:
            # No import statement: Perhaps this is defined in inputs.py directly, so we have no client
            return "local"

        for client in self.input.parser.clients:
            if client in import_statement:
                 return client

        return "local"