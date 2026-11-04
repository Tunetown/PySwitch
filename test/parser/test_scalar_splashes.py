import ast
from contextlib import chdir
import json
from pathlib import Path
import unittest

from web.htdocs.python.parser.PySwitchParser import PySwitchParser


class TreeArgument:
    def __init__(self, value):
        self.value = value

    def to_py(self):
        return self.value


class TestScalarSplashes(unittest.TestCase):
    webroot = Path(__file__).resolve().parents[2] / "web" / "htdocs"

    def parser(self, display = "# no display\nSplashes = None\n"):
        parser = PySwitchParser("pyswitch.hardware.devices.pa_midicaptain_nano_4", "[]")
        parser.from_source("Inputs = []\n", display)
        return parser

    def source(self, parser):
        with chdir(self.webroot):
            return parser.to_source()["display_py"]

    def test_native_none_expression_keeps_no_display_semantics(self):
        parser = self.parser()
        parser.set_splashes("None")
        source = self.source(parser)
        self.assertEqual(json.loads(parser.splashes()), "None")
        self.assertIn("# no display", source)
        self.assertNotIn("DisplayElement", source)
        namespace = {}
        exec(source, namespace)
        self.assertIsNone(namespace["Splashes"])

    def test_action_writeback_can_reuse_the_scalar_splashes_tree(self):
        parser = self.parser()
        parser.set_inputs(TreeArgument([]))
        parser.set_splashes(json.loads(parser.splashes()))
        self.assertEqual(self.source(parser), "# no display\nSplashes = None\n")

    def test_scalar_reference_containing_assign_is_not_treated_as_a_dictionary(self):
        parser = self.parser("reassigned_layout = None\nSplashes = None\n")
        parser.set_splashes("reassigned_layout")
        module = ast.parse(self.source(parser))
        assignment = next(node for node in module.body if isinstance(node, ast.Assign) and node.targets[0].id == "Splashes")
        self.assertEqual(assignment.value.id, "reassigned_layout")

    def test_proxy_tree_still_generates_a_display_element(self):
        parser = self.parser()
        tree = {"name": "DisplayElement", "arguments": [{"name": "children", "value": []}], "assign": "Splashes"}
        parser.set_splashes(TreeArgument(tree))
        source = self.source(parser)
        module = ast.parse(source)
        assignment = next(node for node in module.body if isinstance(node, ast.Assign))
        self.assertEqual(assignment.value.func.id, "DisplayElement")
        self.assertIn("from pyswitch.ui.ui import DisplayElement", source)

    def test_proxy_scalar_uses_the_same_expression_path(self):
        parser = self.parser()
        parser.set_splashes(TreeArgument("None"))
        self.assertEqual(json.loads(parser.splashes()), "None")
