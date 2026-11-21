import libcst

class CodeGenerator:

    # names: Optional callback names(name, client) returning the name to be used in the code for a call
    #        (for example an import alias of a client function)
    def __init__(self, parser = None, file_id = None, insert_before_assign = None, format = False, names = None):
        self.parser = parser
        self.names = names
        self.file_id = file_id
        self.insert_before_assign = insert_before_assign
        self.format = format
        self.initial_level = 0

    # Generate libcst nodes from the passed specification data.
    def generate(self, data):   
        return self._generate(data, self.initial_level)

    ####################################################################################################################

    # Implementation for generate()
    def _generate(self, data, level):
        if isinstance(data, list):
            return self._generate_list_node(data, level)
        
        elif isinstance(data, dict):
            if "name" in data:
                return self._generate_call_node(data, level)
            
            if "arguments" in data:
                return self._generate_dict_node(data, level)
            
            if "assign" in data and data["assign"]:
                return self._resolve_assign(
                    node = self._generate(data["value"], self.initial_level) if "value" in data and data["value"] else None, 
                    data = data
                )                
            
            if "value" in data:
                return self._generate(data["value"], level)

        return libcst.parse_expression(data)
        
    ####################################################################################################################

    # Generate libcst node from th passed list representation
    def _generate_list_node(self, data, level):
        def format_list():
            for item in data:
                if not isinstance(item, str):
                    return True
                
            return False

        # If there are only atomic items, do not format
        format = format_list()

        return libcst.List(
            elements = [
                libcst.Element(
                    value = self._generate(item, level + 1),
                    comma = self._generate_whitespaced_node(libcst.Comma, libcst.MaybeSentinel.DEFAULT, level + 1) if format else libcst.MaybeSentinel.DEFAULT
                )
                for item in data
            ],
            rbracket = self._generate_whitespaced_node(libcst.RightSquareBracket, libcst.RightSquareBracket(), level) if format else libcst.RightSquareBracket(),
            lbracket = self._generate_whitespaced_node(libcst.LeftSquareBracket, libcst.LeftSquareBracket(), level + 1) if format else libcst.LeftSquareBracket()
        )
    
    # Generate libcst node from the passed dict representation
    def _generate_dict_node(self, data, level):
        if "arguments" not in data:
            raise Exception("No arguments in dict: " + repr(data))

        level = self._resolve_assign_level(data, level)

        dic = libcst.Dict(
            elements = [
                libcst.DictElement(
                    key = libcst.parse_expression('"' + item["name"] + '"'),
                    value = self._element_value(item, level + 1),
                    comma = self._generate_whitespaced_node(libcst.Comma, libcst.MaybeSentinel.DEFAULT, level + 1)
                )
                for item in data["arguments"]
            ],
            rbrace = self._generate_whitespaced_node(libcst.RightCurlyBrace, libcst.RightCurlyBrace(), level),
            lbrace = self._generate_whitespaced_node(libcst.LeftCurlyBrace, libcst.LeftCurlyBrace(), level + 1)
        )
    
        return self._resolve_assign(dic, data)

    # Generate libcst node from the passed call representation
    def _generate_call_node(self, data, level):
        args = data["arguments"] if "arguments" in data else []

        last_arg = args[len(args)-1] if len(args) > 0 else None
        level = self._resolve_assign_level(data, level)

        call = libcst.Call(
            func = libcst.parse_expression(self._call_name(data)),
            args = [
                libcst.Arg(
                    keyword = libcst.parse_expression(arg["name"]) if ("name" in arg and arg["name"]) else None,
                    value = self._element_value(arg, level + 1),
                    whitespace_after_arg = self._generate_parenthesized_whitespace(libcst.SimpleWhitespace(""), (level + 1) if arg != last_arg else level)
                )
                for arg in args
            ],
            whitespace_before_args = self._generate_parenthesized_whitespace(libcst.SimpleWhitespace(""), level + 1) if len(args) > 0 else libcst.SimpleWhitespace("")
        )

        return self._resolve_assign(call, data)
        
    # Returns the name to be used in the code for a call
    def _call_name(self, data):
        if self.names and "client" in data and data["client"]:
            return self.names(data["name"], data["client"])
        
        return data["name"]

    # Resolve assigns. Not recursive: Assigns to assigns are realized with separate nodes.
    def _resolve_assign(self, node, data):
        if "assign" in data and data["assign"]:
            if self.parser and self.file_id:
                if not node:
                    raise Exception("You can only omit the value field when no parser is connected")
                
                self.parser.set_assignment(
                    data["assign"],
                    node,
                    self.file_id, 
                    insert_before_assign = self.insert_before_assign
                )

            return libcst.Name(
                value = data["assign"]
            )

        return node

    # If the data is an assignment, start at the initial level again
    def _resolve_assign_level(self, data, level):
        if "assign" in data and data["assign"]:
            return self.initial_level
        
        return level

    # Returns the value of an element
    def _element_value(self, element, level):
        if "value" in element and element["value"] != None:
            return self._generate(element["value"], level)
            
        raise Exception("Invalid node: " + repr(element))
    
    #########################################################################################################

    # Returns a node of type with whitespaces
    def _generate_whitespaced_node(self, type, default, level):
        if not self.format:
            return default
        
        if type == libcst.Comma:
            return libcst.Comma(
                whitespace_after = self._generate_parenthesized_whitespace(default, level)
            )
        
        if type == libcst.RightSquareBracket:
            return libcst.RightSquareBracket(
                whitespace_before = self._generate_parenthesized_whitespace(default, level)
            )

        if type == libcst.LeftSquareBracket:
            return libcst.LeftSquareBracket(
                whitespace_after = self._generate_parenthesized_whitespace(default, level)
            )
        
        if type == libcst.RightCurlyBrace:
            return libcst.RightCurlyBrace(
                whitespace_before = self._generate_parenthesized_whitespace(default, level)
            )

        if type == libcst.LeftCurlyBrace:
            return libcst.LeftCurlyBrace(
                whitespace_after = self._generate_parenthesized_whitespace(default, level)
            )
        
        raise Exception("Type unknown: " + repr(type))
        
    # Gerate a parenthesized whitespace
    def _generate_parenthesized_whitespace(self, default, level):
        if not self.format:
            return default
        
        return libcst.ParenthesizedWhitespace(
            first_line = libcst.TrailingWhitespace(
                newline = libcst.Newline()
            ),
            indent=True,
            last_line = libcst.SimpleWhitespace(
                value = self._get_indent(level)
            ),
        )

    # Get indentation string of spaces
    def _get_indent(self, level):
        return "".join(["    " for i in range(level)])


