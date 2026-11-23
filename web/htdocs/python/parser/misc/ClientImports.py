import libcst

from .ImportExtractor import ImportExtractor
from .AddImportsTransformer import AddImportsTransformer

# Client aware imports for the client functions (actions and mappings, as listed in the definitions files).
# Functions may have the same name in several clients (classes may not), so they are imported by (client, name).
# If functions with the same name from several clients are used in one file, they are imported with an alias
# <CLIENT>_<NAME> (for example "from pyswitch.clients.fractal.actions.tap_tempo import TAP_TEMPO as FRACTAL_TAP_TEMPO").
# A client whose function is already imported without alias keeps the plain name.
#
# Code strings (values passed as code, for example mappings selected in the UI) write functions which exist in
# several clients with the qualified name <CLIENT>_<NAME> (same as the alias), so the client is not lost. In the
# code, qualified names are replaced by the planned name (plain or alias).
class ClientImports:

    # Returns if a definition (entry of actions.json or mappings.json) is handled here. Definitions with
    # a dot in the name (class members like "FractalMappings.PRESET") import their class, which is unique.
    @staticmethod
    def handles(definition):
        return "." not in definition["name"]

    # definitions: List of { "name", "importPath", "client" }
    def __init__(self, definitions, clients):
        self.clients = clients
        self.__by_name = {}

        for d in definitions:
            if not ClientImports.handles(d):
                continue

            if d["name"] not in self.__by_name:
                self.__by_name[d["name"]] = {}

            if d["client"] not in self.__by_name[d["name"]]:
                self.__by_name[d["name"]][d["client"]] = d["importPath"]

    # Returns if the name is a client function (of any client)
    def is_client_function(self, name):
        return name in self.__by_name

    # Returns the alias name used for a client function when several clients' functions have the same name
    @staticmethod
    def alias(name, client):
        return client.upper() + "_" + name

    # Returns if functions with the name exist in several clients
    def is_ambiguous(self, name):
        return name in self.__by_name and len(self.__by_name[name]) > 1

    # Returns the name of a client function in code strings: qualified (<CLIENT>_<NAME>) if functions 
    # with the name exist in several clients, else the plain name.
    def code_string_name(self, name, client):
        if client and self.is_ambiguous(name) and client in self.__by_name[name]:
            return self.alias(name, client)
        
        return name

    # Resolves a qualified name (see code_string_name()) to (name, client), or returns None
    def resolve_qualified(self, qualified):
        for client in self.clients:
            prefix = client.upper() + "_"
            if not qualified.startswith(prefix):
                continue

            name = qualified[len(prefix):]
            if self.is_ambiguous(name) and client in self.__by_name[name]:
                return (name, client)
            
        return None

    # Returns a list of (name, client) for all qualified names (see code_string_name()) in a code string
    def qualified_calls(self, code):
        if not any((client.upper() + "_") in code for client in self.clients):
            return []
        
        try:
            node = libcst.parse_expression(code)
        except Exception:
            return []
        
        visitor = _QualifiedNamesVisitor(self)
        node.visit(visitor)
        return visitor.result

    # Returns the client for a module path (pyswitch.clients.<client>[.xxx]), or None
    def client_of_module(self, module):
        if not module:
            return None

        for client in self.clients:
            prefix = "pyswitch.clients." + client
            if module == prefix or module.startswith(prefix + "."):
                return client

        return None

    ######################################################################################################

    # Returns a dict (name, client) => name to be used in the code, for all client functions in calls
    # (list of (name, client) tuples).
    def plan(self, calls, cst):
        used = {}       # Name => list of clients

        for (name, client) in calls:
            if name not in self.__by_name or client not in self.__by_name[name]:
                continue

            if name not in used:
                used[name] = []

            if client not in used[name]:
                used[name].append(client)

        ret = {}
        for name, clients in used.items():
            if len(clients) == 1:
                ret[(name, clients[0])] = name
                continue

            # Several clients: The one which is already imported without alias keeps the plain name
            plain_client = self.__plain_import_client(name, cst)

            for client in clients:
                ret[(name, client)] = name if client == plain_client else self.alias(name, client)

        return ret

    # Applies the imports for a plan (see plan()) to the CST and returns the new CST:
    # - Imports binding a planned name to something else are removed,
    # - missing imports for the planned names are added,
    # - client functions used in the code which are not imported at all (for example from code strings set by the UI)
    #   are imported, preferring the clients of the plan, then local ones.
    def apply(self, cst, plan):
        required = {}       # Binding name => (module, name)
        clients = []        # Clients used by the plan (in order)

        for (name, client), binding in plan.items():
            required[binding] = (self.__by_name[name][client], name)

            if client not in clients:
                clients.append(client)

        # Qualified names (from code strings) are replaced by the planned names
        renames = {}
        for (name, client), binding in plan.items():
            if self.is_ambiguous(name) and self.alias(name, client) != binding:
                renames[self.alias(name, client)] = binding

        if renames:
            cst = cst.visit(_RenameNamesTransformer(renames))

        # Remove conflicting imports
        remover = _RemoveConflictingImportsTransformer(required)
        cst = cst.visit(remover)

        definitions = [
            self.__import_definition(binding, module, name)
            for binding, (module, name) in required.items()
            if binding not in remover.satisfied
        ]

        # Client functions used but not imported
        usage = _NameUsageVisitor()
        cst.visit(usage)

        for name in usage.used:
            if name in required or name in usage.bound or name in usage.defined:
                continue

            if name not in self.__by_name:
                continue

            client = self.__preferred_client(name, clients)
            definitions.append(self.__import_definition(name, self.__by_name[name][client], name))

        if not definitions:
            return cst

        return cst.visit(AddImportsTransformer(definitions))

    ######################################################################################################

    # Returns the client of the import binding the plain name (without alias), or None
    def __plain_import_client(self, name, cst):
        visitor = ImportExtractor(name)
        cst.visit(visitor)

        if not visitor.result or visitor.result_name != name:
            return None

        return self.client_of_module(visitor.result_module)

    # Client to import an unresolved function name from: clients of the plan first, then local ones, then the first one
    def __preferred_client(self, name, clients):
        available = self.__by_name[name]

        for client in clients + ["local"]:
            if client in available:
                return client

        return list(available.keys())[0]

    # Import definition as used by AddImportsTransformer
    def __import_definition(self, binding, module, name):
        return {
            "name": binding,
            "importPath": module,
            "importName": name if binding == name else (name + " as " + binding)
        }


######################################################################################################


# Removes import bindings of the required names which import something else. Sets satisfied to the
# binding names which are already imported correctly.
class _RemoveConflictingImportsTransformer(libcst.CSTTransformer):
    def __init__(self, required):
        self.required = required
        self.satisfied = set()

    def leave_ImportFrom(self, original_node, updated_node):
        if isinstance(updated_node.names, libcst.ImportStar) or not updated_node.module:
            return updated_node

        code = libcst.parse_module("")
        module = code.code_for_node(updated_node.module)

        names_to_keep = []
        changed = False

        for alias in updated_node.names:
            name = code.code_for_node(alias.name)
            binding = alias.asname.name.value if alias.asname else name

            if binding in self.required:
                if self.required[binding] == (module, name) and binding not in self.satisfied:
                    self.satisfied.add(binding)
                else:
                    changed = True
                    continue

            names_to_keep.append(alias)

        if not changed:
            return updated_node

        if not names_to_keep:
            return libcst.RemoveFromParent()

        return updated_node.with_changes(
            names = [n.with_changes(comma = libcst.MaybeSentinel.DEFAULT) for n in names_to_keep]
        )


# Collects the names used in the code (outside of imports), the names bound by imports and the names
# defined on module level
class _NameUsageVisitor(libcst.CSTVisitor):
    def __init__(self):
        self.used = []
        self.bound = set()
        self.defined = set()
        self.__depth = 0

    def visit_Import(self, node):
        self.__bind(node)
        return False

    def visit_ImportFrom(self, node):
        self.__bind(node)
        return False

    def visit_Name(self, node):
        if node.value not in self.used:
            self.used.append(node.value)

    def visit_FunctionDef(self, node):
        self.defined.add(node.name.value)

    def visit_ClassDef(self, node):
        self.defined.add(node.name.value)

    def visit_AssignTarget(self, node):
        if isinstance(node.target, libcst.Name):
            self.defined.add(node.target.value)

    def __bind(self, node):
        if isinstance(node.names, libcst.ImportStar):
            return

        for alias in node.names:
            if alias.asname:
                self.bound.add(alias.asname.name.value)
            else:
                self.bound.add(libcst.parse_module("").code_for_node(alias.name))


# Collects (name, client) of the qualified names (see ClientImports.code_string_name()) in a code string
class _QualifiedNamesVisitor(libcst.CSTVisitor):
    def __init__(self, client_imports):
        self.client_imports = client_imports
        self.result = []

    def visit_Name(self, node):
        resolved = self.client_imports.resolve_qualified(node.value)
        if resolved and resolved not in self.result:
            self.result.append(resolved)


# Renames names in the code (outside of imports, attribute names and keywords): renames is a dict old => new name
class _RenameNamesTransformer(libcst.CSTTransformer):
    def __init__(self, renames):
        self.renames = renames

    def visit_Import(self, node):
        return False

    def visit_ImportFrom(self, node):
        return False

    def leave_Name(self, original_node, updated_node):
        if updated_node.value in self.renames:
            return updated_node.with_changes(value = self.renames[updated_node.value])
        
        return updated_node
    
    def leave_Attribute(self, original_node, updated_node):
        return updated_node.with_changes(attr = original_node.attr)
    
    def leave_Arg(self, original_node, updated_node):
        return updated_node.with_changes(keyword = original_node.keyword)
