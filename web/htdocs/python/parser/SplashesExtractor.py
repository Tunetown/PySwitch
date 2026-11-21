from .misc.CodeExtractor import CodeExtractor

class SplashesExtractor(CodeExtractor):
    
    def __init__(self, parser, cst):
        super().__init__(cst)
        self.parser = parser

    # Can be redefined to define unnamed parameters for specific types. If this
    # returns [], only keyword arguments are allowed or an Exception will be raised.
    def get_arg_names(self, type_name):
        if type_name == "DisplayBounds":
            return ["x", "y", "w", "h"]
        
    # Can be redefined to add/manipulate data for Call output nodes
    def postprocess_call(self, call_data):
        # Import aliases (client functions with the same name of several clients) are resolved to the real name
        (call_data["name"], call_data["client"]) = self.parser.resolve_name(call_data["name"], cst = self.cst)