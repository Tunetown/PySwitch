import libcst
import json 

from .InputsExtractor import InputsExtractor
from .SplashesExtractor import SplashesExtractor

from .misc.CodeGenerator import CodeGenerator
from .misc.RemoveUnusedImportTransformer import RemoveUnusedImportTransformer
from .misc.AddImportsTransformer import AddImportsTransformer
from .misc.AssignmentNameExtractor import AssignmentNameExtractor
from .misc.AssignmentExtractor import AssignmentExtractor
from .misc.ImportExtractor import ImportExtractor
from .misc.ReplaceAssignmentTransformer import ReplaceAssignmentTransformer
from .misc.AddAssignmentTransformer import AddAssignmentTransformer
from .misc.RemoveAssignmentTransformer import RemoveAssignmentTransformer
from .misc.ClassNameExtractor import ClassNameExtractor

class PySwitchParser:

    def __init__(self, hw_import_path, available_clients_json):
        self.hw_import_path = hw_import_path       
        self.__csts = None
        
        self.clients = json.loads(available_clients_json)

        # Buffers
        self.__available_actions = None
        self.__available_mappings = None
        self.__available_display_imports = None
        
    # Set the parser data from source code
    def from_source(self, inputs_py, display_py):
        self.__csts = {
            "inputs_py": libcst.parse_module(inputs_py),
            "display_py": libcst.parse_module(display_py)
        }

    # Returns a dict holding the sources for the current configuration
    def to_source(self):
        if not self.__csts:
            raise Exception("No data loaded")
        
        self._add_all_possible_imports()
        self._remove_unused_imports()

        return {
            "inputs_py": self.__csts["inputs_py"].code,
            "display_py": self.__csts["display_py"].code
        }
    
    # Delivers code for a node of tree data. Cannot add assignments!
    def code_for_data_node(self, data, format = False):
        if isinstance(data, str):
            return data
        
        node = CodeGenerator(format = format).generate(data.to_py())
        return libcst.parse_module("").code_for_node(node)
    
    # Returns a JSON encoded tree of the Inputs assign in inputs.py
    def inputs(self):
        if not self.__csts:
            raise Exception("No data loaded")
                
        inputs = InputsExtractor(self, self.__csts["inputs_py"]).get("Inputs")
        return json.dumps(inputs)
    
    # Replace the inputs in inputs.py
    def set_inputs(self, inputs):
        if not self.__csts:
            raise Exception("No data loaded")
        
        # Remove first assign as this can lead to endless recursion and is not relevant anyway
        inputs_py = inputs.to_py()
        if "assign" in inputs_py: 
            inputs_py["assign"] = None

        inputs_node = CodeGenerator(
            parser = self, 
            file_id = "inputs_py", 
            insert_before_assign = "Inputs",
            format = True
        ).generate(inputs_py)
        
        self.set_assignment("Inputs", inputs_node, "inputs_py")

    # Searches for an Assign with the given name and returns its node, or None if not found
    def get_assignment(self, name, file_id):
        assignments = AssignmentExtractor().get(self.__csts[file_id])
        
        for a in assignments:
            if a["name"] == name:
                return a["node"]
            
        return None

    #######################################################################################

    # Returns a JSON encoded list of assignments in display.py TODO remove
    def displays(self):
        if not self.__csts:
            raise Exception("No data loaded")
        
        return json.dumps(AssignmentNameExtractor().get(self.__csts["display_py"]))
    
    # Returns a JSON encoded tree of the Splashes assign in display.py
    def splashes(self):
        if not self.__csts:
            raise Exception("No data loaded")
                
        splashes = SplashesExtractor(self, self.__csts["display_py"]).get("Splashes")
        return json.dumps(splashes)

    # Replace the splashes in display.py
    def set_splashes(self, splashes):
        if not self.__csts:
            raise Exception("No data loaded")

        # Remove first assign as this can lead to endless recursion and is not relevant anyway
        splashes_py = splashes.to_py()
        if "assign" in splashes_py:
            splashes_py["assign"] = None

        # Collect all assign names referenced in the new tree BEFORE code generation,
        # so we can remove stale DisplayLabel constants that are no longer referenced.
        referenced_assigns = self._collect_assign_names(splashes_py)

        splashes_node = CodeGenerator(
            parser = self,
            file_id = "display_py",
            insert_before_assign = "Splashes",
            format = True
        ).generate(splashes_py)

        self.set_assignment("Splashes", splashes_node, "display_py")

        # Remove orphaned DisplayLabel assignments that are no longer used in Splashes
        # and not referenced in inputs.py (the JS frontend already prevents removal
        # of referenced labels, but we double-check here for safety).
        current_names = AssignmentNameExtractor().get(self.__csts["display_py"])
        for name in current_names:
            if name.startswith("_") or name == "Splashes":
                continue
            if name not in referenced_assigns:
                self.remove_assignment(name, "display_py")

    ########################################################################################
        
    # Adds or replaces the given assignment by name.
    def set_assignment(self, name, call_node, file_id, insert_before_assign = None):
        replacer = ReplaceAssignmentTransformer(name, call_node)
        self.__csts[file_id] = self.__csts[file_id].visit(replacer)
        if replacer.replaced:
            return

        adder = AddAssignmentTransformer(
            name,
            call_node,
            insert_before_assign = insert_before_assign,
            cst = self.__csts[file_id] if not insert_before_assign else None
        )

        self.__csts[file_id] = self.__csts[file_id].visit(adder)

    # Remove the given assignment by name.
    def remove_assignment(self, name, file_id):
        remover = RemoveAssignmentTransformer(name)
        self.__csts[file_id] = self.__csts[file_id].visit(remover)

    # Recursively collect all "assign" names from a parsed tree dict.
    def _collect_assign_names(self, data, names = None):
        if names is None:
            names = set()
        if isinstance(data, dict):
            if "assign" in data and data["assign"]:
                names.add(data["assign"])
            for value in data.values():
                self._collect_assign_names(value, names)
        elif isinstance(data, list):
            for item in data:
                self._collect_assign_names(item, names)
        return names

    ########################################################################################

    # Remove unused imports on all files. Does no config update!
    def _remove_unused_imports(self):
        self._remove_unused_import_for_file("inputs_py")
        self._remove_unused_import_for_file("display_py")

    def _remove_unused_import_for_file(self, file_id):
        wrapper = libcst.metadata.MetadataWrapper(self.__csts[file_id])
        visitor = RemoveUnusedImportTransformer(wrapper)
        self.__csts[file_id] = wrapper.module.visit(visitor)

    ########################################################################################

    # Adds all possible imports (actions etc.) Does no config update!
    def _add_all_possible_imports(self):
        self._add_all_possible_imports_inputs()
        self._add_all_possible_imports_display()

    def _add_all_possible_imports_inputs(self):
        if not self.__available_actions:
            self.__available_actions = self._generate_action_imports()

        if not self.__available_mappings:
            self.__available_mappings = self._generate_mapping_imports()    
        
        display_assignments = [
            { 
                "name": assign, 
                "importPath": "display" 
            } 
            for assign in AssignmentNameExtractor().get(self.__csts["display_py"])
        ]

        # Add all imports
        visitor = AddImportsTransformer(self.__available_actions + self.__available_mappings + display_assignments)
        self.__csts["inputs_py"] = self.__csts["inputs_py"].visit(visitor)

    def _add_all_possible_imports_display(self):
        if not self.__available_display_imports:
            self.__available_display_imports = self._generate_display_imports()

        # Add all imports
        visitor = AddImportsTransformer(self.__available_display_imports)
        self.__csts["display_py"] = self.__csts["display_py"].visit(visitor)
            
    # Generates all client specific display assigns (everything from the client's __init__.py file and some standards)
    def _generate_display_imports(self):
        ret = []

        # Load callback definitions from file
        with open('definitions/callbacks.json') as f: available_callbacks_json = f.read()
        
        clients = json.loads(available_callbacks_json)
        
        for client in clients:
            ret += client["callbacks"]

        # Get __init__ classes of clients
        for client in self.clients:
            ret += ClassNameExtractor(
                file = "pyswitch/clients/" + client + "/__init__.py", 
                import_path = "pyswitch.clients." + client
            ).get()
        
        return ret + [
            {
                "name": "const",
                "importPath": "micropython"
            },

            {
                "name": "Colors",
                "importPath": "pyswitch.colors"
            },
            {
                "name": "DEFAULT_LABEL_COLOR",
                "importPath": "pyswitch.colors"
            },

            {
                "name": "DisplayElement",
                "importPath": "pyswitch.ui.ui"
            },
            {
                "name": "DisplayBounds",
                "importPath": "pyswitch.ui.ui"
            },
            {
                "name": "DisplayLabel",
                "importPath": "pyswitch.ui.elements"
            },
            {
                "name": "BidirectionalProtocolState",
                "importPath": "pyswitch.ui.elements"
            },
            {
                "name": "PYSWITCH_VERSION",
                "importPath": "pyswitch.misc"
            }
        ]
    
    # Generates all imports for actions
    def _generate_action_imports(self):
        # Load actions definitions from file
        with open('definitions/actions.json') as f: available_actions_json = f.read()
        
        clients = json.loads(available_actions_json)
        actions = []

        for client in clients:
            actions += client["actions"]

        # Add additional potentially needed imports besides the actions.
        return actions + [
            # Additional imports: Colors
            {
                "name": "Colors",
                "importPath": "pyswitch.colors"
            },
            {
                "name": "DEFAULT_SWITCH_COLOR",
                "importPath": "pyswitch.colors"
            },

            # RIG_SELECT display modes (TODO move to client code)
            {
                "name": "RIG_SELECT_DISPLAY_CURRENT_RIG",
                "importPath": "pyswitch.clients.kemper.actions.rig_select"
            },
            {
                "name": "RIG_SELECT_DISPLAY_TARGET_RIG",
                "importPath": "pyswitch.clients.kemper.actions.rig_select"
            },

            # Fixed FX slot IDs (TODO move to client code)
            {
                "name": "FIXED_SLOT_ID_TRANSPOSE",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_GATE",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_COMP",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_BOOST",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_WAH",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_CHORUS",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_AIR",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },
            {
                "name": "FIXED_SLOT_ID_DBL_TRACKER",
                "importPath": "pyswitch.clients.kemper.actions.fixed_fx"
            },

            # Effect slot definitions (TODO move to client code)
            {
                "name": "KemperEffectSlot",
                "importPath": "pyswitch.clients.kemper"
            },

            # Callbacks
            {
                "name": "BinaryParameterCallback",
                "importPath": "pyswitch.controller.callbacks"
            },

            # PushButtonAction
            {
                "name": "PushButtonAction",
                "importPath": "pyswitch.controller.actions"
            },

            # HID Keycodes
            {
                "name": "Keycode",
                "importPath": "adafruit_hid.keycode"
            },
            {
                "name": "PYSWITCH_VERSION",
                "importPath": "pyswitch.misc"
            }
        ]
    
    # Generates all imports for mappings
    def _generate_mapping_imports(self):
        # Load actions definitions from file
        with open('definitions/mappings.json') as f: available_mappings_json = f.read()
        
        clients = json.loads(available_mappings_json)
        mappings = []

        for client in clients:
            mappings = mappings + client["mappings"]

        return mappings
    
    ##############################################################################################

    # Determine the client for an Action instance
    def _determine_import_statement(self, name, cst):
        visitor = ImportExtractor(name)
        cst.visit(visitor)
        return visitor.result

    # Determine the client for a type name. You must pass either cst or file_id.
    def determine_client(self, name, file_id = None, cst = None):
        import_statement = self._determine_import_statement(name, self.__csts[file_id] if file_id else cst)
        
        if not import_statement:
            # No import statement: Perhaps this is defined in inputs.py directly, so we have no client
            return "local"

        for client in self.clients:
            if client in import_statement:
                 return client

        return "local"