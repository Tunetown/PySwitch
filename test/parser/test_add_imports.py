import ast
import unittest

import libcst

from web.htdocs.python.parser.misc.AddImportsTransformer import AddImportsTransformer
from web.htdocs.python.parser.misc.RemoveUnusedImportTransformer import RemoveUnusedImportTransformer


class TestAddImportsTransformer(unittest.TestCase):
    imports = [{"name": "deque", "importPath": "collections"}]

    def generate(self, source, cleanup = True):
        module = libcst.parse_module(source).visit(AddImportsTransformer(self.imports))
        if not cleanup:
            return module.code
        wrapper = libcst.metadata.MetadataWrapper(module)
        return wrapper.module.visit(RemoveUnusedImportTransformer(wrapper)).code

    def test_function_body_is_not_used_as_the_module_import_location(self):
        source = "def callback(value):\n    return value\n\nresult = deque([1, 2])\n"
        generated = self.generate(source)
        module = ast.parse(generated)
        self.assertTrue(any(isinstance(node, ast.ImportFrom) for node in module.body))
        namespace = {}
        exec(generated, namespace)
        self.assertEqual(list(namespace["result"]), [1, 2])
        self.assertEqual(namespace["callback"](17), 17)
        self.assertIn("def callback(value):\n    return value\n", generated)

    def test_class_body_does_not_capture_a_required_module_import(self):
        generated = self.generate("class Callback:\n    enabled = True\n\nresult = deque([3])\n")
        namespace = {}
        exec(generated, namespace)
        self.assertEqual(list(namespace["result"]), [3])
        self.assertTrue(namespace["Callback"].enabled)

    def test_docstring_and_future_import_stay_before_generated_imports(self):
        generated = self.generate(
            '"""Configuration metadata."""\n'
            "from __future__ import annotations\n"
            "def callback(value: DeferredType):\n    return value\n\n"
            "result = deque([4])\n",
            cleanup = False
        )
        namespace = {}
        exec(generated, namespace)
        self.assertEqual(namespace["__doc__"], "Configuration metadata.")
        self.assertEqual(namespace["callback"].__annotations__, {"value": "DeferredType"})
        self.assertEqual(list(namespace["result"]), [4])

    def test_repeated_generation_keeps_one_import_and_preserves_comments(self):
        source = "# custom configuration\ndef callback():\n    return deque([5])\n"
        generated = self.generate(self.generate(source))
        self.assertEqual(generated.count("from collections import deque"), 1)
        self.assertIn("# custom configuration", generated)
        namespace = {}
        exec(generated, namespace)
        self.assertEqual(list(namespace["callback"]()), [5])

    def test_empty_module_can_receive_imports(self):
        generated = libcst.parse_module("").visit(AddImportsTransformer(self.imports)).code
        self.assertEqual(generated.rstrip("\n"), "from collections import deque")

    def test_empty_import_list_preserves_the_module(self):
        source = "# custom configuration\ndef callback():\n    return 17\n"
        generated = libcst.parse_module(source).visit(AddImportsTransformer([])).code
        self.assertEqual(generated, source)
