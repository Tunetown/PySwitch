import libcst

class AddImportsTransformer(libcst.CSTTransformer):
    
    def __init__(self, import_paths):
        self.import_paths = import_paths

    def leave_Module(self, original_node, updated_node):
        new_statements = [
            libcst.parse_statement("from " + definition["importPath"] + " import " + (definition["importName"] if "importName" in definition else definition["name"]) + "\n")
            for definition in self.import_paths
        ]

        # Imports belong to the module, never the first function/class body
        # encountered during traversal. Keep its docstring and future imports first.
        insert_at = 1 if updated_node.get_docstring() is not None else 0
        while insert_at < len(updated_node.body):
            statement = updated_node.body[insert_at]
            if not isinstance(statement, libcst.SimpleStatementLine) or not any(
                isinstance(item, libcst.ImportFrom)
                and isinstance(item.module, libcst.Name)
                and item.module.value == "__future__"
                for item in statement.body
            ):
                break
            insert_at += 1

        return updated_node.with_changes(body = [
            *updated_node.body[:insert_at],
            *new_statements,
            *updated_node.body[insert_at:]
        ])
