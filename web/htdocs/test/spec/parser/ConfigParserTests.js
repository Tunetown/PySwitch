class ConfigParserTests extends TestBase {

    async minimal() {
        await this.init();
        const config = new MockConfiguration("", "");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        expect(await parser.input("1")).toBe(null);
        expect(await parser.input("2")).toBe(null);
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    async getInputSettings() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-presets/get-input-settings");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;
        
        await this.#testAction(parser, {
            modelName: "1",
            client: "kemper",
            actions: [{
                name: "RIG_UP",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_1"
                    },
                    {
                        name: "text",
                        value: '"Rig up"'
                    }
                ]
            }],
            holdTimeMillis: 555,
            holdRepeat: true
        });
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    async getInputActionsDefault() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-presets/get-inputs-default");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        await this.#testAction(parser, {
            modelName: "1",
            client: "kemper",
            actions: [{
                name: "RIG_UP",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_1"
                    },
                    {
                        name: "text",
                        value: '"Rig up"'
                    }
                ]
            }]
        });

        await this.#testAction(parser, {
            modelName: "2",
            client: "kemper",
            actions: [
                { 
                    name: "BANK_UP",
                    arguments: [
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_2"
                        }
                    ] 
                },
                { 
                    name: "RIG_DOWN",
                    arguments: [] 
                },
                { 
                    name: "RIG_UP",
                    arguments: [
                        {
                            name: "some",
                            value: "val"
                        },
                        {
                            name: "numb",
                            value: '78'
                        },
                        {
                            name: "large",
                            value: '{"d": {"e": {"f": 8}}}'
                        },
                        {
                            name: "arr",
                            value: '[{"f": 8, "j": [3, 5, 6]}, None, "g"]'
                        }
                    ] 
                }
            ] 
        });

        await this.#testAction(parser, {
            modelName: "A",
            client: "kemper",
            actions: [{ 
                name: "RIG_DOWN",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_FOOTER_1"
                    },
                    {
                        name: "text",
                        value: '"Rig dn"'
                    }
                ]
            }] 
        });

        await this.#testAction(parser, {
            modelName: "B",
            client: "kemper",
            actions: [{ 
                name: "BANK_DOWN",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_FOOTER_2"
                    }
                ] 
            }] 
        });
    }

    async getInputActionsHold() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-presets/get-inputs-hold");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;
        
        await this.#testAction(parser, {
            modelName: "1",
            client: "kemper",
            actions: [{ 
                name: "RIG_UP",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_1"
                    },
                    {
                        name: "text",
                        value: '"Rig up"'
                    },
                    {
                        name: "calculated_arg",
                        value: "value != None"
                    }
                ] 
            }] 
        });

        await this.#testAction(parser, {
            modelName: "2",
            client: "kemper",
            actionsHold: [{ 
                name: "TUNER_MODE",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_2"
                    }
                ]
            }], 
            actions: [
                { 
                    name: "BANK_UP",
                    arguments: [] 
                }
            ] 
        });

        await this.#testAction(parser, {
            modelName: "A",
            client: "kemper",
            actions: [{ 
                name: "RIG_DOWN",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_FOOTER_1"
                    },
                    {
                        name: "text",
                        value: '"Rig dn"'
                    }
                ]
            }] 
        });

        await this.#testAction(parser, {
            modelName: "B",
            client: "kemper",
            actions: [{ 
                name: "BANK_DOWN",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_FOOTER_2"
                    }
                ] 
            }] 
        });
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    async getInputActionsDeferred() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "data/test-presets/get-inputs-assign");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;
        
        await this.#testAction(parser, {
            modelName: "1",
            client: "kemper",
            actions: [{ 
                name: "RIG_UP",
                assign: "_deferred_2",
                arguments: [
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_1"
                    },
                    {
                        name: "text",
                        value: '"foo"'
                    },
                    {
                        name: "id",
                        value: "303"
                    }
                ] 
            }] 
        });

        await this.#testAction(parser, {
            modelName: "2",
            client: "kemper",
            actions: [
                { 
                    name: "BANK_UP",
                    arguments: [] 
                }
            ],
            actionsHold: [
                { 
                    name: "TUNER_MODE",
                    arguments: [
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_2"
                        }
                    ]
                },
                {
                    name: "RIG_DOWN",
                    assign: "_deferred",
                    arguments: [
                        {
                            name: "display",
                            value: "DISPLAY_FOO"
                        }
                    ]
                }
            ]
        });
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    async replaceActions() {
        await this.#replaceActions(
            "1", 
            [
                { 
                    name: "SOME_ACTION",
                    arguments: [
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_5"
                        }
                    ] 
                },
                { 
                    name: "SOME_ACTION_2",
                    arguments: [
                        {
                            name: "useLeds",
                            value: '{"a": 4}'
                        }
                    ] 
                }
            ],
            "local"
        );

        await this.#replaceActions(
            "A", 
            [
                { 
                    name: "SOME_ACTION",
                    arguments: [] 
                }
            ],
            "local"
        );

        await this.#replaceActions(
            "A", 
            [],
            "local"
        );
    }

    async replaceActionsDeferred() {
        await this.#replaceActions(
            "1", 
            [
                { 
                    name: "SOME_ACTION",
                    assign: "_foo",
                    arguments: [
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_5"
                        }
                    ] 
                },
                { 
                    name: "SOME_ACTION_2",
                    assign: "_bar",
                    arguments: [
                        {
                            name: "useLeds",
                            value: '{"3": 4}'
                        }
                    ] 
                }
            ],
            "local"
        );

        await this.#replaceActions(
            "A", 
            [
                { 
                    name: "SOME_ACTION",
                    assign: "_bar2",
                    arguments: [] 
                }
            ],
            "local"
        );

        await this.#replaceActions(
            "A", 
            [],
            "local"
        );
    }

    async replaceActionsPaging() {
        await this.#replaceActions(
            "1", 
            [
                { 
                    name: "PagerAction",
                    assign: "_pager",
                    arguments: [
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_5"
                        },
                        {
                            name: "pages",
                            value: [
                                {
                                    id: "10",
                                    color: "Colors.GREEN",
                                    text: '"sometext"'
                                },
                                {
                                    id: '"other"',
                                    color: "(3, 4, 5)",
                                    text: '"someothertext"'
                                }
                            ]
                        }
                    ] 
                }
            ],
            "local"
        );
    }

    async #replaceActions(modelName, actions, clientId, debug = false) {
        await this.init();

        const config = new WebConfiguration(new MockController(), "data/test-presets/get-inputs-default");
        await config.init(this.pyswitch, "../");

        const parser = config.parser;
        await parser.init();

        if (debug) {
            console.log("REPLACE of actions: ", actions);
            console.log("current: ", parser.inputs())
        }

        const input = await parser.input(modelName);
    
        // Replace actions
        input.setActions(actions);

        if (debug) {
            console.log(" -> added actions: ")
            console.log((await config.get()).inputs_py);
        }

        await this.#testAction(parser, {
            modelName: modelName,
            client: clientId,
            actions: actions
        });

        // Replace actionsHold        
        input.setActions(actions, true);

        if (debug) {
            console.log(" -> added actionsHold: ")
            console.log((await config.get()).inputs_py);
        }

        await this.#testAction(parser, {
            modelName: modelName,
            client: clientId,
            actions: actions,
            actionsHold: actions
        });
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////

    async createNewInputs() {
        await this.init();

        const config = new WebConfiguration(new MockController(), "data/test-presets/empty");
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        const input1 = await parser.input("1");
        expect(input1).toEqual(null);

        const input2 = await parser.input("1", true);
        
        input2.setActions(
            [
                {
                    name: "RIG_SELECT",
                    arguments: [
                        {
                            name: "rig",
                            value: "1"
                        },
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_2"
                        }
                    ]
                }
            ]
        );
        
        // console.log((await parser.config.get()).inputs_py);

        await this.#testAction(parser, {
            modelName: "1",
            client: "kemper",
            actions: [{
                name: "RIG_SELECT",
                arguments: [
                    {
                        name: "rig",
                        value: "1"
                    },
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_2"
                    }
                ]
            }]
        });
    }

    async createNewInputsWithSettings() {
        await this.init();

        const config = new WebConfiguration(new MockController(), "data/test-presets/empty");
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        const input = await parser.input("1", true);

        input.setActions(
            [
                {
                    name: "RIG_SELECT",
                    arguments: []
                }
            ]
        );

        input.setHoldTimeMillis(765)
        input.setHoldRepeat(true)

        expect(input.holdTimeMillis()).toBe(765);
        expect(input.holdRepeat()).toBe(true);
                
        // console.log((await parser.config.get()).inputs_py);

        await this.#testAction(parser, {
            modelName: "1",
            client: "kemper",
            actions: [{
                name: "RIG_SELECT",
                arguments: []
            }],
            holdTimeMillis: 765,
            holdRepeat: true
        });
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////////

    async addOneImport() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "../templates/MIDICaptain Nano 4");
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        const input1 = await parser.input("1");
        
        // Add first actions available
        const clients = await parser.getAvailableActions();
        const action = clients[0].actions[0];
        const client = clients[0].client;

        input1.setActions(
            [
                this.#composeAction(action, client)
            ]
        );
        
        // console.log((await parser.config.get()).inputs_py);

        // Test with PySwitch
        await this.runner.run(config);

        expect(1).toBe(1);
    }

    async addAllImports() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "../templates/MIDICaptain Nano 4");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        const input1 = await parser.input("1");
        
        // Add all actions available
        const clients = await parser.getAvailableActions();
        
        let actions = [];
        for (const client of clients) {
            for (const action of client.actions) {
                if (action.meta.data.target != "AdafruitSwitch") continue;

                actions.push(
                    this.#composeAction(action, client.client)
                )
            }
        }

        actions = actions.filter((item) => item != null)

        expect(actions.length).toBeGreaterThan(0);

        // console.log(actions)

        input1.setActions(
            actions
        );
        
        // console.log((await parser.config.get()).inputs_py);

        // Test with PySwitch
        await this.runner.run(config);

        expect(1).toBe(1);
    }

    async addDisplayImports() {
        await this.init();
        const config = new WebConfiguration(new MockController(), "../templates/MIDICaptain Nano 4");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        const input1 = await parser.input("1");
        
        input1.setActions(
            [
                {
                    name: "RIG_SELECT",
                    arguments: [
                        {
                            name: "rig",
                            value: "1"
                        },
                        {
                            name: "display",
                            value: "DISPLAY_HEADER_2"
                        }
                    ]
                }
            ]
        );
        
        // console.log((await parser.config.get()).inputs_py);

        // Test with PySwitch
        await this.runner.run(config);

        expect(1).toBe(1);
    }

    /**
     * Helper for import tests: Returns an action definition for setting, 
     * from a given action definition loaded by the parser.
     */
    #composeAction(item, client) {
        return {
            name: (item.name == "PagerAction.proxy") ? "_pager.proxy" : item.name,
            assign: (item.name == "PagerAction") ? "_pager" : null,
            client: client,
            arguments: item.parameters.map(                
                function (param) {
                    if (item.name == "PagerAction" && param.name == "pages") {
                        return {
                            name: param.name,
                            value: []
                        }
                    }

                    if (item.name == "PagerAction.proxy" && param.name == "page_id") {
                        return {
                            name: param.name,
                            value: "1"
                        }
                    }

                    return {
                        name: param.name,
                        value: param.meta.getDefaultValue()
                    }
                }
            )
        }
    }

    ///////////////////////////////////////////////////////////////////////////////////////////

    async displayNameGeneric() {
        await this.#checkActionMeta(
            "BANK_UP",
            {
                name: "BANK_UP",
                client: "kemper",
                arguments: []
            },
            "Kemper: Bank Up",   // Default
            "Kemper: Bank Up"    // With actual value
        );

        await this.#checkActionMeta(
            "BANK_DOWN",
            {
                name: "BANK_DOWN",
                client: "kemper",
                arguments: []
            },
            "Kemper: Bank Down",   // Default
            "Kemper: Bank Down"    // With actual value
        );
    }

    async displayNameRigSelect() {
        await this.#checkActionMeta(
            "RIG_SELECT",
            {
                name: "RIG_SELECT",
                client: "kemper",
                arguments: [
                    {
                        name: "rig",
                        value: "2"
                    },
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_2"
                    }
                ]
            },
            "Kemper: Select Rig",   // Default
            "Kemper: Select Rig 2"    // With actual value
        )
    }

    async displayNameRigSelectToggle() {
        await this.#checkActionMeta(
            "RIG_SELECT",
            {
                name: "RIG_SELECT",
                client: "kemper",
                arguments: [
                    {
                        name: "rig",
                        value: "2"
                    },
                    {
                        name: "rig_off",
                        value: "4"
                    },
                    {
                        name: "display",
                        value: "DISPLAY_HEADER_2"
                    }
                ]
            },
            "Kemper: Select Rig",      // Default
            "Kemper: Toggle Rigs 2/4"    // With actual value
        )        
    }

    async displayNameBankSelect() {
        await this.#checkActionMeta(
            "BANK_SELECT",
            {
                name: "BANK_SELECT",
                client: "kemper",
                arguments: [
                    {
                        name: "bank",
                        value: "2"
                    }
                ]
            },
            "Kemper: Select Bank",   // Default
            "Kemper: Select Bank 2"    // With actual value
        );

        await this.#checkActionMeta(
            "BANK_SELECT",
            {
                name: "BANK_SELECT",
                client: "kemper",
                arguments: [
                    {
                        name: "bank",
                        value: "2"
                    },
                    {
                        name: "bank_off",
                        value: "4"
                    }
                ]
            },
            "Kemper: Select Bank",      // Default
            "Kemper: Toggle Banks 2/4"    // With actual value
        );

        await this.#checkActionMeta(
            "BANK_SELECT",
            {
                name: "BANK_SELECT",
                client: "kemper",
                arguments: [
                    {
                        name: "bank",
                        value: "3"
                    },
                    {
                        name: "preselect",
                        value: "True"
                    }
                ]
            },
            "Kemper: Select Bank",      // Default
            "Kemper: Preselect Bank 3"    // With actual value
        );

        await this.#checkActionMeta(
            "BANK_SELECT",
            {
                name: "BANK_SELECT",
                client: "kemper",
                arguments: [
                    {
                        name: "bank",
                        value: "3"
                    },
                    {
                        name: "preselect",
                        value: "False"
                    }
                ]
            },
            "Kemper: Select Bank",      // Default
            "Kemper: Select Bank 3"    // With actual value
        )
    }

    async #checkActionMeta(name, action, expNameDefault, expNameCurrent) {
        await this.#doCheckActionMeta(name, action, expNameDefault, expNameCurrent, false);
        await this.#doCheckActionMeta(name, action, expNameDefault, expNameCurrent, true);
    }

    async #doCheckActionMeta(name, action, expNameDefault, expNameCurrent, hold) {
        await this.init();
        const config = new WebConfiguration(new MockController(), "../templates/MIDICaptain Nano 4");
        
        await config.init(this.pyswitch, "../");
        const parser = config.parser;

        const input1 = await parser.input("1");
        
        input1.setActions(
            [
                action
            ],
            hold
        );
        
        const clients = await parser.getAvailableActions();

        function searchAction(name) {
            for (const client of clients) {
                if (client.client != action.client) continue;
                for (const action2 of client.actions) {
                    if (action2.name == name) return action2;
                }
            }
            throw new Error();
        }

        const action2 = searchAction(name);

        const actions = await input1.actions(hold);
        const current = actions[0];
        
        const meta = action2.meta;

        expect(meta.getDisplayName()).toBe(expNameDefault);
        expect(meta.getDisplayName(current)).toBe(expNameCurrent);
    }

    /**
     * {
     *      modelName,
     *      client,             // Client ID
     *      actions: [
     *          {
     *              name: "name",
     *              arguments: [
     *                  {
     *                      name: "name",
     *                      value: value
     *                  }
     *              ]
     *          }
     *      ],
     *      actionsHold: [...] 
     *      holdTimeMillis:
     *      holdRepeat:
     * }
     */
    async #testAction(parser, config) {
        const input = await parser.input(config.modelName);

        function precheck(item, expItem) {
            if (Array.isArray(item)) {
                if (item.length != expItem.length) {
                    console.warn(item, expItem, input);
                }

                for (let i = 0; i < item.length; ++i) {
                    const it = item[i];
                    const exp = expItem[i];

                    precheck(it, exp);
                }
                return;
            }

            if (typeof item != "string") return;

            if (item == expItem) return;
            console.warn(item, expItem, input)
        }

        async function test(hold, expActions) {
            const actions = await input.actions(hold);
            
            if (actions.length != expActions.length) {
                precheck(actions, expActions)
            }
            expect(actions.length).toBe(expActions.length);
    
            for (let i = 0; i < expActions.length; ++i) {
                const action = actions[i];
                const expAction = expActions[i];
    
                precheck(action.name, expAction.name)
                expect(action.name).toBe(expAction.name);

                if (expAction.assign) {
                    precheck(action.assign, expAction.assign)
                    expect(action.assign).toBe(expAction.assign);
                } else {
                    precheck(action.assign, undefined)
                    expect(action.assign).toBe(undefined);
                }
                
                if (action.client != "local") {
                    precheck(action.client, config.client)
                    expect(action.client).toBe(config.client);
                }

                if (expAction.arguments) {
                    precheck(action.arguments(), expAction.arguments)
                    expect(action.arguments()).toEqual(expAction.arguments);
                } else {
                    precheck(action.arguments(), [])
                    expect(action.arguments()).toEqual([]);
                }
            }
        }

        if (config.actions) {
            await test(false, config.actions);
        }
        if (config.actionsHold) {
            await test(true, config.actionsHold);
        }

        if (config.holdTimeMillis) {
            expect(input.holdTimeMillis()).toBe(config.holdTimeMillis)
        }

        if (config.holdRepeat) {
            expect(input.holdRepeat()).toBe(config.holdRepeat)
        }
    }
}