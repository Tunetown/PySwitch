class DisplayParserTests extends TestBase {

    async getDisplaysMinimal() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-display/get-displays-minimal");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        await this.#testDisplay(parser, {
            splashes: "None"
        });
    }

    async getDisplaysEmpty() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-display/get-displays-empty");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        await this.#testDisplay(parser, {
            name: "TunerDisplayCallback",
            client: "kemper",
            // assign: "Splashes",
            arguments: [
                {
                    name: "splash_default",
                    value: {
                        name: "DisplayElement",
                        arguments: [
                            {
                                name: "children",
                                value: []
                            }
                        ]
                    }
                }
            ]
        });
    }

    async getDisplaysArray() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-display/get-displays-other");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        await this.#testDisplay(parser, [
            {
                value: '"foo"'
            },
            {
                arguments: [
                    {
                        name: "some",
                        value: {
                            name: "SomeCall",
                            arguments: [
                                {
                                    name: "ddd",
                                    value: "3"
                                },
                                {
                                    name: "eee",
                                    value: {
                                        assign: "_ASSIGN",
                                        name: "hello",
                                        arguments: [
                                            {
                                                value: {
                                                    assign: "_ASSIGN2",
                                                    name: "Call2",
                                                    arguments: [
                                                        {
                                                            name: "jjj",
                                                            value: "98"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
            {
                name: "Call3",
                arguments: [
                    {
                        name: "aaa",
                        value: {
                            arguments: [
                                {
                                    name: "k",
                                    value: "hey"
                                },
                                {
                                    name: "b",
                                    value: {
                                        assign: "_BARE",
                                        value: "5"
                                    }
                                },
                                {
                                    name: "c",
                                    value: {
                                        assign: "_REDIRECT",
                                        value: {
                                            assign: "_BARE",
                                            value: "5"
                                        }
                                    }
                                },
                                {
                                    name: "d",
                                    value: {
                                        assign: "_REDIRECT2",
                                        value: {
                                            assign: "_BARE",
                                            value: {
                                                assign: "_ASSIGN",
                                                name: "hello",
                                                arguments: [
                                                    {
                                                        value: {
                                                            assign: "_ASSIGN2",
                                                            name: "Call2",
                                                            arguments: [
                                                                {
                                                                    name: "jjj",
                                                                    value: "98"
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]); //, true);
    }

    async getDisplaysDefault() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-display/get-displays-default");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        await this.#testDisplay(parser, {
            name: "TunerDisplayCallback",
            client: "kemper",
            // assign: "Splashes",
            arguments: [
                {
                    name: "strobe",
                    value: "True"
                },
                {
                    name: "splash_default",
                    value: {
                        name: "DisplayElement",
                        arguments: [
                            {
                                name: "bounds",
                                value: {
                                    name: "DisplayBounds",
                                    arguments: [
                                        {
                                            name: "x",
                                            value: "0"
                                        },
                                        {
                                            name: "y",
                                            value: "0"
                                        },
                                        {
                                            name: "w",
                                            value: {
                                                assign: "_DISPLAY_WIDTH",
                                                name: "const",
                                                arguments: [
                                                    {
                                                        value: "240"
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            name: "h",
                                            value: {
                                                assign: "_DISPLAY_HEIGHT",
                                                name: "const",
                                                arguments: [
                                                    {
                                                        value: "240"
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                name: "children",
                                value: [
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_HEADER_1",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "1"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_HEADER_2",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "1"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "y",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_FOOTER_1",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "1"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    assign: "_FOOBOUNDS",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_FOOTER_Y",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "200"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_FOOTER_2",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "1"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_FOOTER_Y",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "200"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        arguments: [
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    assign: "_RIGBOUNDS",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_DISPLAY_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "240"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_RIG_NAME_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "160"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "layout",
                                                value: {
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/PTSans-NarrowBold-40.pcf"'
                                                        },
                                                        {
                                                            name: "lineSpacing",
                                                            value: "0.8",
                                                        },
                                                        {
                                                            name: "maxTextWidth",
                                                            value: "220",
                                                        },
                                                        {
                                                            name: "text",
                                                            value: "KemperRigNameCallback.DEFAULT_TEXT",
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "callback",
                                                value: {
                                                    assign: "_CB",
                                                    name: "KemperRigNameCallback",
                                                    client: "kemper",
                                                    arguments: [
                                                        {
                                                            name: "show_name",
                                                            value: "True"
                                                        },
                                                        {
                                                            name: "show_rig_id",
                                                            value: "False"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        arguments: [
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_RIG_ID_Y",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "200"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_DISPLAY_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "240"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_RIG_ID_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "layout",
                                                value: {
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "callback",
                                                value: {
                                                    name: "KemperRigNameCallback",
                                                    client: "kemper",
                                                    arguments: [
                                                        {
                                                            name: "show_name",
                                                            value: "False"
                                                        },
                                                        {
                                                            name: "show_rig_id",
                                                            value: "True"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "BidirectionalProtocolState",
                                        arguments: [
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_DISPLAY_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "240"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_RIG_NAME_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "160"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        });
    }

    ////////////////////////////////////////////////////////////////////////////////////////////

    async codeForNode() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-display/get-displays-minimal");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;
        await parser.init();

        // Basic
        expect(parser.codeForNode("foo")).toEqual("foo");
        
        // Lists
        expect(parser.codeForNode([])).toEqual("[]");        
        expect(parser.codeForNode(["2","3","4"])).toEqual("[2, 3, 4]");
        expect(parser.codeForNode(["2","3",'"hjk"'])).toEqual('[2, 3, "hjk"]');
        expect(parser.codeForNode([
            "2", 
            { 
                name: "foos", 
                arguments: [
                    {
                        name: "h",
                        value: "67"
                    },
                    {
                        name: "g",
                        value: '"67"'
                    }
                ]
            },
            {
                assign: "_assi",
                name: "arbitraryCall"
            }
        ])).toEqual('[2, foos(h = 67, g = "67"), _assi]');

        // Dicts
        expect(parser.codeForNode({ arguments: [] })).toEqual("{}");
        expect(parser.codeForNode({
            arguments: [
                {
                    name: "jk",
                    value: "67"
                }
            ]
        })).toEqual('{"jk": 67}');
        expect(parser.codeForNode({
            arguments: [
                {
                    name: "jk",
                    value: '"67"'
                },
                {
                    name: "jg",
                    value: {
                        name: "dd",
                        arguments: [
                            {
                                name: "j",
                                value: "9"
                            },
                            {
                                name: "i",
                                value: ["2","3","4"]
                            }                            
                        ]
                    }
                },
                {
                    name: "g",
                    value: {
                        assign: "_assi"
                    }
                }
            ]
        })).toEqual('{"jk": "67", "jg": dd(j = 9, i = [2, 3, 4]), "g": _assi}');

        // Calls
        expect(parser.codeForNode({
            name: "kk"
        })).toEqual("kk()");
        expect(parser.codeForNode({
            name: "kk",
            arguments: [
                {
                    value: '3'
                }
            ]
        })).toEqual('kk(3)');
        expect(parser.codeForNode({
            name: "kk",
            arguments: [
                {
                    name: "l",
                    value: '"aa"'
                },
                {
                    name: "a",
                    value: {
                        name: "oo"
                    }
                },
                {
                    name: "g",
                    value: {
                        assign: "_assi"
                    }
                }
            ]
        })).toEqual('kk(l = "aa", a = oo(), g = _assi)');

        // Assigns on first level
        expect(parser.codeForNode({
            name: "kk",
            assign: "_assi",
            arguments: [
                {
                    name: "l",
                    value: '"aa"'
                },
                {
                    name: "a",
                    value: {
                        name: "oo"
                    }
                }
            ]
        })).toEqual('_assi');
    }

    ////////////////////////////////////////////////////////////////////////////////////////////

    async replaceDisplaysCode() {
        // Root code
        await this.#replaceSplashes(
            // Set data
            {
                value: "DisplayEtwas(someparam = 9)"
            },

            // Expected
            {
                name: "DisplayEtwas",
                arguments: [
                    {
                        name: "someparam",
                        value: "9"
                    }
                ]
            }
        );

        // List items
        await this.#replaceSplashes(
            // Set data
            [
                {
                    value: "DisplayEtwas(someparam = 9)"
                },
                "9"
            ],

            // Expected
            [
                {
                    name: "DisplayEtwas",
                    arguments: [
                        {
                            name: "someparam",
                            value: "9"
                        }
                    ]
                },
                "9"
            ]
        );

        // Call args
        await this.#replaceSplashes(
            // Set data
            {
                name: "jj",
                arguments: [
                    {
                        name: "foos",
                        value: "DisplayEtwas(someparam = 9)"
                    }
                ]
            },

            // Expected
            {
                name: "jj",
                arguments: [
                    {
                        name: "foos",
                        value: {
                            name: "DisplayEtwas",
                            arguments: [
                                {
                                    name: "someparam",
                                    value: "9"
                                }
                            ]
                        }
                    }
                ]
            }
        );

        // Dict args
        await this.#replaceSplashes(
            // Set data
            {
                arguments: [
                    {
                        name: "foos",
                        value: "DisplayEtwas(someparam = 9)"
                    }
                ]
            },

            // Expected
            {
                arguments: [
                    {
                        name: "foos",
                        value: {
                            name: "DisplayEtwas",
                            arguments: [
                                {
                                    name: "someparam",
                                    value: "9"
                                }
                            ]
                        }
                    }
                ]
            }
        );

        await this.#replaceSplashes(
            // Set data
            {
                arguments: [
                    {
                        name: "ddd",
                        value: 'DesrbHut(sdfvsdv = { "foo": [2,3,4,"hg", foos(SOMETYPE)] }, deb = True)'
                    }
                ]
            },

            // Expected
            {
                arguments: [
                    {
                        name: "ddd",
                        value: {
                            name: "DesrbHut",
                            arguments: [
                                {
                                    name: "sdfvsdv",
                                    value: {
                                        arguments: [
                                            {
                                                name: 'foo',
                                                value: [
                                                    "2",
                                                    "3",
                                                    "4",
                                                    '"hg"',
                                                    {
                                                        name: "foos",
                                                        arguments: [
                                                            {
                                                                value: "SOMETYPE" 
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                },
                                {
                                    name: "deb",
                                    value: "True"
                                }
                            ]
                        }
                    }
                ]
            }
        );
    }

    async replaceDisplaysDict() {
        await this.#replaceSplashes({
            arguments: [
                {
                    name: "foos",
                    value: "4"
                }
            ]
        });

        await this.#replaceSplashes({
            assign: "_FOO",
            arguments: [
                {
                    name: "foos",
                    value: "4"
                }
            ]
        });
    }

    async replaceDisplaysCall() {
        await this.#replaceSplashes({
            name: "SomeCall",
            arguments: [
                {
                    name: "foos",
                    value: "4"
                }
            ]
        });

        await this.#replaceSplashes({
            name: "SomeCall",
            assign: "_GGG",
            arguments: [
                {
                    name: "foos",
                    value: "4"
                }
            ]
        });
    }

    async replaceDisplaysArray() {
        await this.#replaceSplashes([
            '"simplestring"'
        ]);

        await this.#replaceSplashes([
            {
                name: "simplecall",
                arguments: []
            }
        ]);

        await this.#replaceSplashes([
            [
                '"otherlist"',
                "444",
                {
                    assign: "_ASS",
                    value: '"hk"'
                },
                {
                    arguments: [
                        {
                            name: "ff",
                            value: "2"
                        },
                        {
                            name: "fdf",
                            value: "kkk"
                        }
                    ]
                },
                {
                    name: "somecall",
                    arguments: [
                        {
                            name: "hz",
                            value: {
                                assign: "_KSKS",
                                name: "SomeType",
                                arguments: [
                                    {
                                        name: "foo",
                                        value: '"jkhp"'
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        ]);

        await this.#replaceSplashes([
            {
                arguments: [
                    {
                        name: "somed",
                        value: {
                            name: "SomeCadsll",
                            arguments: [
                                {
                                    name: "dddd",
                                    value: "34"
                                },
                                {
                                    name: "feee",
                                    value: {
                                        assign: "_ASASIGN",
                                        name: "helslo",
                                        arguments: [
                                            {
                                                value: {
                                                    assign: "_ASdSIGN2",
                                                    name: "Cafll2",
                                                    arguments: [
                                                        {
                                                            name: "jjdj",
                                                            value: "980"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            },
            '"foos"',
            {
                assign: "_JJJ",
                value: {
                    assign: "_LLLL",
                    name: "SomeDeepCall",
                    arguments: [
                        {
                            name: "sdv",
                            value: {
                                assign: "LLASS",
                                value: "7"
                            }
                        }
                    ]
                }
            },
            {
                name: "Caldl3",
                arguments: [
                    {
                        name: "aaaf",
                        value: {
                            arguments: [
                                {
                                    name: "kf",
                                    value: '"hedy"'
                                },
                                {
                                    name: "ba",
                                    value: {
                                        assign: "_BAdRE",
                                        value: "54"
                                    }
                                },
                                {
                                    name: "c",
                                    value: {
                                        assign: "_REDIRECT",
                                        value: {
                                            assign: "_BAdRE",
                                            value: "54"
                                        }
                                    }
                                },
                                {
                                    name: "d",
                                    value: {
                                        assign: "_REDIRE4CT2",
                                        value: {
                                            assign: "_BRE",
                                            value: {
                                                assign: "_ASSIGwN",
                                                name: "hedllo",
                                                arguments: [
                                                    {
                                                        value: {
                                                            assign: "_ASSfIGN2",
                                                            name: "Calsl2",
                                                            arguments: [
                                                                {
                                                                    name: "jjjd",
                                                                    value: "968"
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]);
    }

    async replaceDisplaysFantasy() {
        await this.#replaceSplashes({
            name: "TunerDisplayCallback",
            client: "kemper",
            // assign: "Splashes",
            arguments: [
                {
                    name: "strobe",
                    value: "False"
                },
                {
                    name: "splash_ddefault",
                    value: {
                        name: "DisplaydElement",
                        arguments: [
                            {
                                name: "bousdnds",
                                value: {
                                    name: "DisplfayBounds",
                                    arguments: [
                                        {
                                            name: "xd",
                                            value: "1"
                                        },
                                        {
                                            name: "y",
                                            value: "0"
                                        },
                                        {
                                            name: "w",
                                            value: {
                                                assign: "_DISPLSAY_WIDTH",
                                                name: "codnst",
                                                arguments: [
                                                    {
                                                        value: "2340"
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            name: "h",
                                            value: {
                                                assign: "_DISPLAY_HEIGHT",
                                                name: "consst",
                                                arguments: [
                                                    {
                                                        value: "2440"
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                name: "childdren",
                                value: [
                                    {
                                        name: "DisplfayLabel",
                                        assign: "DISPLAYds_HEADER_1",
                                        arguments: [
                                            {
                                                name: "layoudt",
                                                value: {
                                                    assign: "_ACTIONf_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "fognt",
                                                            value: '"/fonfts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backCfolor",
                                                            value: "DEFAgULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "strohke",
                                                            value: "13"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bofunds",
                                                value: {
                                                    name: "DisplawyBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "10"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: "4"
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOTd_WIDTH",
                                                                name: "confst",
                                                                arguments: [
                                                                    {
                                                                        value: "1420"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "480"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_HEADER_2",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LgABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "fonft",
                                                            value: '"/fodnts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULdT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "100"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "y",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_FOOTER_1",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "1"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    assign: "_FOOBOUNDS",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_FOOTER_Y",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "200"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        assign: "DISPLAY_FOOTER_2",
                                        arguments: [
                                            {
                                                name: "layout",
                                                value: {
                                                    assign: "_ACTION_LABEL_LAYOUT",    
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        },
                                                        {
                                                            name: "backColor",
                                                            value: "DEFAULT_LABEL_COLOR",
                                                        },
                                                        {
                                                            name: "stroke",
                                                            value: "1"
                                                        }
                                                    
                                                    ]
                                                }
                                            },
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_FOOTER_Y",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "200"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_SLOT_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "120"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLsdabel",
                                        arguments: [
                                            {
                                                name: "vdbounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    assign: "_RIGBOUNDS",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_SLOdT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "440"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_DISPLAY_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "240"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_RIG_NAME_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "160"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "layout",
                                                value: {
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/PTSans-NarrowBold-40.pcf"'
                                                        },
                                                        {
                                                            name: "lineSpacing",
                                                            value: "0.8",
                                                        },
                                                        {
                                                            name: "maxTextWidth",
                                                            value: "220",
                                                        },
                                                        {
                                                            name: "text",
                                                            value: "KemperRigNameCallback.DEFAULT_TEXT",
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "callback",
                                                value: {
                                                    assign: "_CB",
                                                    name: "KemperRigNameCallback",
                                                    client: "kemper",
                                                    arguments: [
                                                        {
                                                            name: "show_name",
                                                            value: "True"
                                                        },
                                                        {
                                                            name: "show_rig_id",
                                                            value: "False"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "DisplayLabel",
                                        arguments: [
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_RIG_ID_Y",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "200"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_DISPLAY_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "240"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_RIG_ID_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "layout",
                                                value: {
                                                    arguments: [
                                                        {
                                                            name: "font",
                                                            value: '"/fonts/H20.pcf"'
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "callback",
                                                value: {
                                                    name: "KemperRigNameCallback",
                                                    client: "kemper",
                                                    arguments: [
                                                        {
                                                            name: "show_name",
                                                            value: "False"
                                                        },
                                                        {
                                                            name: "show_rig_id",
                                                            value: "True"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    },
                                    {
                                        name: "BidirectionalProftocolState",
                                        arguments: [
                                            {
                                                name: "bounds",
                                                value: {
                                                    name: "DisplayBounds",
                                                    arguments: [
                                                        {
                                                            name: "x",
                                                            value: "0"
                                                        },
                                                        {
                                                            name: "y",
                                                            value: {
                                                                assign: "_SLOT_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "40"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "w",
                                                            value: {
                                                                assign: "_DISdPLAY_WIDTH",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "240"
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            name: "h",
                                                            value: {
                                                                assign: "_RIG_NAMdsE_HEIGHT",
                                                                name: "const",
                                                                arguments: [
                                                                    {
                                                                        value: "160"
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        })
    }

    //////////////////////////////////////////////////////////////////////////////////////////////////

    async replaceDisplaysReal() {
        await this.#replaceSplashesWithRun(
            {
                name: "TunerDisplayCallback",
                client: "kemper",
                // assign: "Splashes",
                arguments: [
                    {
                        name: "strobe",
                        value: "True"
                    },
                    {
                        name: "splash_default",
                        value: {
                            name: "DisplayElement",
                            arguments: [
                                {
                                    name: "bounds",
                                    value: {
                                        name: "DisplayBounds",
                                        arguments: [
                                            {
                                                name: "x",
                                                value: "0"
                                            },
                                            {
                                                name: "y",
                                                value: "0"
                                            },
                                            {
                                                name: "w",
                                                value: {
                                                    assign: "_DISPLAY_WIDTH",
                                                    name: "const",
                                                    arguments: [
                                                        {
                                                            value: "240"
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                name: "h",
                                                value: {
                                                    assign: "_DISPLAY_HEIGHT",
                                                    name: "const",
                                                    arguments: [
                                                        {
                                                            value: "240"
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    name: "children",
                                    value: [
                                        {
                                            name: "DisplayLabel",
                                            assign: "DISPLAY_HEADER_1",
                                            arguments: [
                                                {
                                                    name: "layout",
                                                    value: {
                                                        assign: "_ACTION_LABEL_LAYOUT",    
                                                        arguments: [
                                                            {
                                                                name: "font",
                                                                value: '"/fonts/H20.pcf"'
                                                            },
                                                            {
                                                                name: "backColor",
                                                                value: "DEFAULT_LABEL_COLOR",
                                                            },
                                                            {
                                                                name: "stroke",
                                                                value: "1"
                                                            }
                                                        
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "y",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_SLOT_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "120"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_SLOT_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            name: "DisplayLabel",
                                            assign: "DISPLAY_HEADER_2",
                                            arguments: [
                                                {
                                                    name: "layout",
                                                    value: {
                                                        assign: "_ACTION_LABEL_LAYOUT",    
                                                        arguments: [
                                                            {
                                                                name: "font",
                                                                value: '"/fonts/H20.pcf"'
                                                            },
                                                            {
                                                                name: "backColor",
                                                                value: "DEFAULT_LABEL_COLOR",
                                                            },
                                                            {
                                                                name: "stroke",
                                                                value: "1"
                                                            }
                                                        
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: {
                                                                    assign: "_SLOT_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "120"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "y",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_SLOT_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "120"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_SLOT_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        },
                    
                                        {
                                            name: "DisplayLabel",
                                            assign: "DISPLAY_FOOTER_1",
                                            arguments: [
                                                {
                                                    name: "layout",
                                                    value: {
                                                        assign: "_ACTION_LABEL_LAYOUT",    
                                                        arguments: [
                                                            {
                                                                name: "font",
                                                                value: '"/fonts/H20.pcf"'
                                                            },
                                                            {
                                                                name: "backColor",
                                                                value: "DEFAULT_LABEL_COLOR",
                                                            },
                                                            {
                                                                name: "stroke",
                                                                value: "1"
                                                            }
                                                        
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        assign: "_FOOBOUNDS",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "y",
                                                                value: {
                                                                    assign: "_FOOTER_Y",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "200"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_SLOT_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "120"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_SLOT_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            name: "DisplayLabel",
                                            assign: "DISPLAY_FOOTER_2",
                                            arguments: [
                                                {
                                                    name: "layout",
                                                    value: {
                                                        assign: "_ACTION_LABEL_LAYOUT",    
                                                        arguments: [
                                                            {
                                                                name: "font",
                                                                value: '"/fonts/H20.pcf"'
                                                            },
                                                            {
                                                                name: "backColor",
                                                                value: "DEFAULT_LABEL_COLOR",
                                                            },
                                                            {
                                                                name: "stroke",
                                                                value: "1"
                                                            }
                                                        
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: {
                                                                    assign: "_SLOT_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "120"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "y",
                                                                value: {
                                                                    assign: "_FOOTER_Y",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "200"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_SLOT_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "120"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_SLOT_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            name: "DisplayLabel",
                                            arguments: [
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        assign: "_RIGBOUNDS",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "y",
                                                                value: {
                                                                    assign: "_SLOT_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_DISPLAY_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "240"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_RIG_NAME_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "160"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "layout",
                                                    value: {
                                                        arguments: [
                                                            {
                                                                name: "font",
                                                                value: '"/fonts/PTSans-NarrowBold-40.pcf"'
                                                            },
                                                            {
                                                                name: "lineSpacing",
                                                                value: "0.8",
                                                            },
                                                            {
                                                                name: "maxTextWidth",
                                                                value: "220",
                                                            },
                                                            {
                                                                name: "text",
                                                                value: "KemperRigNameCallback.DEFAULT_TEXT",
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "callback",
                                                    value: {
                                                        assign: "_CB",
                                                        name: "KemperRigNameCallback",
                                                        client: "kemper",
                                                        arguments: [
                                                            {
                                                                name: "show_name",
                                                                value: "True"
                                                            },
                                                            {
                                                                name: "show_rig_id",
                                                                value: "False"
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            name: "DisplayLabel",
                                            arguments: [
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "y",
                                                                value: {
                                                                    assign: "_RIG_ID_Y",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "200"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_DISPLAY_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "240"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_RIG_ID_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "layout",
                                                    value: {
                                                        arguments: [
                                                            {
                                                                name: "font",
                                                                value: '"/fonts/H20.pcf"'
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    name: "callback",
                                                    value: {
                                                        name: "KemperRigNameCallback",
                                                        client: "kemper",
                                                        arguments: [
                                                            {
                                                                name: "show_name",
                                                                value: "False"
                                                            },
                                                            {
                                                                name: "show_rig_id",
                                                                value: "True"
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            name: "BidirectionalProtocolState",
                                            arguments: [
                                                {
                                                    name: "bounds",
                                                    value: {
                                                        name: "DisplayBounds",
                                                        arguments: [
                                                            {
                                                                name: "x",
                                                                value: "0"
                                                            },
                                                            {
                                                                name: "y",
                                                                value: {
                                                                    assign: "_SLOT_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "40"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "w",
                                                                value: {
                                                                    assign: "_DISPLAY_WIDTH",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "240"
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            {
                                                                name: "h",
                                                                value: {
                                                                    assign: "_RIG_NAME_HEIGHT",
                                                                    name: "const",
                                                                    arguments: [
                                                                        {
                                                                            value: "160"
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            null,
            "data/test-display/get-displays-real"
        )
    }
    
    ////////////////////////////////////////////////////////////////////////////////////////////

    async #testDisplay(parser, expSplashes, debug = false) {
        await this.init();
        await parser.init();

        const splashes = await parser.splashes();
        if (debug) console.log(splashes, expSplashes)
        
        function test(node, expNode) {
            if (expNode.name) {
                expect(node.name).toBe(expNode.name);

                if (expNode.client) {
                    expect(node.client).toBe(expNode.client);
                } else {
                    expect(node.client).toBe("local");
                }
            } else {
                expect(node.name).toBe(undefined);
            }
            
            for (let i = 0; i < (expNode.arguments || []).length; ++i) {
                const arg = node.arguments[i];
                const expArg = expNode.arguments[i];

                if (expArg.name) {
                    expect(arg.name).toBe(expArg.name);
                } else {
                    expect(arg.name).toBe(undefined);
                }
                if (expArg.value) {
                    test(arg.value, expArg.value);
                } else {
                    expect(arg.value).toBe(undefined);
                }
            }
        }

        test(splashes, expSplashes);
    }

    async #replaceSplashesWithRun(splashes, expSplashes = null, testdataPath = null, debug = false) {
        const parser = await this.#replaceSplashes(splashes, expSplashes, testdataPath, debug);
        await this.runner.run(parser.config);        
    }

    async #replaceSplashes(splashes, expSplashes = null, testdataPath = null, debug = false) {
        await this.init();
        const config = new WebConfiguration(new MockController(), testdataPath ? testdataPath : "data/test-display/get-displays-minimal");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        await parser.setSplashes(splashes);
        
        if (debug) {
            console.log(splashes);
            console.log((await config.get()).display_py);
        }

        await this.#testDisplay(parser, expSplashes ? expSplashes : splashes);
        return parser
    }
}