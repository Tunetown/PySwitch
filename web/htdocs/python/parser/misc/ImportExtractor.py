import libcst

# Searches the import statement which binds the passed name (also via an alias: "import X as name").
# After visiting, the following attributes are set (all None if not found):
#   result:          Code of the import statement
#   result_name:     Imported (real) name ("X" for "from m import X as name")
#   result_module:   Module path for "from ... import" statements ("m"), None for plain imports
class ImportExtractor(libcst.CSTVisitor):

    def __init__(self, name):
        self.import_name = name
        self.result = None
        self.result_name = None
        self.result_module = None

    def _visit_import_alike(self, node):
        if self.result:
            return False

        if isinstance(node.names, libcst.ImportStar):
            return False

        for name in node.names:
            asname = name.asname
            if asname is not None:
                name_value = asname.name.value
            else:
                name_value = name.name.value

            if name_value == self.import_name:
                code = libcst.parse_module("")

                self.result = code.code_for_node(node)
                self.result_name = code.code_for_node(name.name)
                self.result_module = code.code_for_node(node.module) if isinstance(node, libcst.ImportFrom) and node.module else None

        return False

    def visit_Import(self, node):
        return self._visit_import_alike(node)

    def visit_ImportFrom(self, node):
        return self._visit_import_alike(node)
