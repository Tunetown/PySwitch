/**
 * Manages connection to client devices (like Kemper)
 */
class ClientController {

    #controller = null;
    #clientIds = null;  // Clients of the configuration at the last initialization

    state = null;
    current = null;     // Name of the currently connected client

    constructor(controller) {
        this.#controller = controller;
        
        this.state = new LocalState("client");
    }
    
    /**
     * Initialize client to the given Configuration instance.
     */
    async init(config) {
        if (!config) return;

        this.#clientIds = await ClientFactory.estimateClients(config);

        const savedClient = this.state.get("selectedClient");

        if (savedClient == "auto" || !savedClient) {
            await this.#scan(config);
        } else {
            await this.#connect(savedClient);
        }
    }
            
    /**
     * Has to be called after the configuration has been changed: if the clients used by the configuration
     * have changed (for example the first action of another client has been added), the clients are initialized again.
     */
    async update(config) {
        if (!config) return;

        const clientIds = await ClientFactory.estimateClients(config);
        if (this.#clientIds && (JSON.stringify(clientIds) == JSON.stringify(this.#clientIds))) return;

        await this.init(config);
    }

    /**
     * Scans for all clients of the given Configuration instance (a configuration can control several clients).
     * Each client is searched on its own port. Clients which are not found are connected to their virtual client.
     */
    async #scan(config) {
        const clientIds = await ClientFactory.estimateClients(config);

        const connections = await Promise.all(
            clientIds.map((clientId) => this.#scanClient(clientId))
        );

        const portNames = [];
        const virtualClientIds = [];

        for (let i = 0; i < clientIds.length; ++i) {
            if (!connections[i]) {
                virtualClientIds.push(clientIds[i]);

            } else if (!portNames.includes(connections[i].name)) {
                portNames.push(connections[i].name);
            }
        }

        await this.#connectAll(portNames, virtualClientIds);
    }

    /**
     * Scans all ports for a client. Resolves to the connection object of the first port the client answers on,
     * or null if not found.
     */
    async #scanClient(clientId) {
        const that = this;

        return new Promise(function(resolve) {
            that.#controller.midi.scan(
                // connect
                async function(portName, attempts) {
                    return await that.#scanPort(clientId, portName, attempts);
                },

                // finish
                async function(connection, attempts) {
                    // Reject all older attempts
                    (new Map(attempts)).forEach(async function(attempt) {
                        await attempt.reject();
                    });

                    resolve(connection);
                },

                // onFailure
                async function() {
                    resolve(null);
                }
            );
        });
    }

    /**
     * Checks if the passed port is connected to the passed client. If yes, returns a connection object.
     */
    async #scanPort(clientId, portName, attempts, timeoutMillis = 1000) {
        console.log("Scan for client on " + portName)
        const that = this;

        function findPort(ports) {
            for (const port of ports) {
                const handler = port[1];
                    
                if (handler.name == portName) {
                    return handler;
                }                
            }
            
            throw new Error("Port " + portName + " not found");
        }

        const input = findPort(this.#controller.midi.midiAccess.inputs);
        const output = findPort(this.#controller.midi.midiAccess.outputs);

        return new Promise(async function(resolve, reject) {
            // Get a detector for the client
            const client = ClientFactory.getInstance(clientId);
            const detector = await client.getClientDetector();
            
            function cleanup() {
                if (attempts) {
                    attempts.delete(portName);
                }

                // Stop the timout
                clearTimeout(timeout);

                // Remove listener (else the detector would parse all messages, too)
                if (listener) that.#controller.midi.removeListener(listener);
            }

            function doResolve(/*data*/) {
                cleanup();
                resolve({
                    name: output.name,
                    input: input,
                    output: output
                });
            }

            function doReject() {
                cleanup();
                reject(new Error("Failed to connect to " + output.name)); 
            }

            // Use the detector to check if there is a client listening
            let listener = detector ? (await detector.test(that.#controller.midi, input, output, doResolve)) : null;

            // Timeout
            const timeout = setTimeout(doReject, timeoutMillis);

            // Register the connection attempt
            if (attempts) {
                attempts.set(portName, {
                    reject: doReject
                });
            }            
        });
    }

    /**
     * Connect to a client directly by port name (can be virtual: "virtual-<clientId>")
     */
    async #connect(portName) {
        if (portName.startsWith("virtual-")) {
            await this.#connectAll([], [portName.substring(8)]);
        } else {
            await this.#connectAll([portName], []);
        }
    }

    /**
     * Connects PySwitch to the passed real ports and virtual clients (by client ID). Messages are sent to all 
     * of them, and the messages of all of them are received (like the MIDI routing on the controller).
     */
    async #connectAll(portNames, virtualClientIds) {
        // First throw out the old MIDI wrapper, if any
        this.#controller.pyswitch.setMidiWrapper(null);
        this.current = null;

        const wrappers = [];
        const virtualClients = [];

        // Virtual clients
        for (const clientId of virtualClientIds) {
            const client = ClientFactory.getInstance(clientId);
            const virtualClient = client ? (await client.getVirtualClient()) : null;
            
            if (!virtualClient) {
                console.warn("Client " + clientId + " does not support a virtual client device");
                continue;
            }

            wrappers.push(virtualClient);
            virtualClients.push(virtualClient);
        }

        // Real devices
        const connectedPorts = [];
        for (const portName of portNames) {
            const port = this.#controller.midi.getPortPair(portName);       
            if (!port) continue;

            wrappers.push(new PythonMidiWrapper(this.#controller.midi, port.input, port.output));
            connectedPorts.push(port.name);
        }

        // Show user interfaces of the virtual clients, if any
        this.#controller.ui.showVirtualClients(virtualClients);

        if (wrappers.length == 0) {
            if (virtualClientIds.length == 0) {
                this.#controller.ui.message("No client device connected", "I");
            }
            return;
        }

        // Set a MIDI wrapper to connect the clients to PySwitch
        const midiWrapper = (wrappers.length == 1) ? wrappers[0] : new CombinedMidiWrapper(wrappers);
        this.#controller.pyswitch.setMidiWrapper(midiWrapper);
        
        // Run the virtual clients
        for (const virtualClient of virtualClients) {
            virtualClient.run(5);
        }

        // Report states etc.
        for (const virtualClient of virtualClients) {
            this.#controller.ui.message("Connecting to " + virtualClient.name, "I");
        }
        for (const portName of connectedPorts) {
            this.#controller.ui.message("Connecting to client at " + portName, "I");
        }

        if (connectedPorts.length > 0) {
            this.current = connectedPorts.join(", ");
        }
    }
}