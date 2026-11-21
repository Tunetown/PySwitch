from .misc.CodeExtractor import CodeExtractor

class InputsExtractor(CodeExtractor):
    
    def __init__(self, parser, cst):
        super().__init__(cst)
        self.parser = parser
        
    # Can be redefined to add/manipulate data for Call output nodes
    def postprocess_call(self, call_data):
        # Import aliases (client functions with the same name of several clients) are resolved to the real name
        (call_data["name"], call_data["client"]) = self.parser.resolve_name(call_data["name"], cst = self.cst)