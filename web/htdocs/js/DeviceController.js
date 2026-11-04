/**
 * Manages connection to controller devices (like a MidiCaptain controller)
 */
class DeviceController {

    #controller = null;           // PySwitch runner
    bridge = null;                // MIDI bridge handler (connects to the Controller running PyMidiBridge, and is reused for connecting to the client, too)

    #connection = null;           // Current connection, holding the bridge instance and ports etc.

    constructor(controller) {
        this.#controller = controller;
        this.bridge = new MidiBridgeHandler(controller.midi);        
    }

    /**
     * Returns the current connected port name.
     */
    portName() {
        if (!this.#connection) return "";
        return this.#connection.name;
    }

    /**
     * Scans for controllers
     * 
     * onSuccess(connection) => void
     * onFailure() => void
     */
    async scan(onSuccess, onFailure = null) {
        const that = this;

        await this.#controller.midi.scan(
            // connect
            async function(portName, attempts) {
                return that.bridge.connect(portName, attempts, 2000);
            },

            // onSuccess
            async function(connection, attempts) {
                // Reject all older attempts
                (new Map(attempts)).forEach(async function(attempt) {
                    await attempt.reject();
                });

                await onSuccess(connection);
            },

            // onFailure
            onFailure
        );
    }
    
    /**
     * Connect a bridge to the passed port name
     */
    async connect(portName) {
        if (this.#connection && this.#connection.name == portName) return;   // Already connected to the bridge
        this.#connection = null;
        
        this.#controller.ui.progress(0, "Connecting to controller " + portName);

        let connection = null;
        try {
            connection = await this.bridge.connect(portName, null, 3000);

        } catch (e) {
            console.error(e)
            this.#controller.ui.progress(1);
            throw new Error("Failed to connect to controller " + portName);
        }

        const bridge = connection.bridge;
        const that = this;

        // Receive start
        bridge.onReceiveStart = async function(data) {
            that.#controller.ui.progress(0, "Loading " + data.path);
        };

        // Progress (receive)
        bridge.onReceiveProgress = async function(data) {
            that.#controller.ui.progress((data.chunk + 1) / data.numChunks, "Loading chunk " + data.chunk + " of " + data.numChunks);
        };

        // Receive finish
        bridge.onReceiveFinish = async function(data) {
            that.#controller.ui.progress(1);
            console.info("Loaded " + portName);
        };

        // Error handling for MIDI errors coming from the bridge
        bridge.onError = async function(message) {
            that.#controller.ui.progress(1);
            that.#controller.message(message);
        }      
        
        this.#connection = connection;
        console.log("Connected to controller " + portName);
    }

    /**
     * Saves the passed Configuration to the given port
     */
    async saveConfig(config, portName) {
        console.log("Saving configuration to " + portName);

        await this.connect(portName);

        const code = await config.get();

        await this.saveFile('inputs.py', code.inputs_py);
        await this.saveFile('display.py', code.display_py);

        // this.#controller.ui.notifications.message("Successfully saved configuration to " + portName, "S");
    }

    /**
     * Returns the content of the passed file path, loaded from the device behind the currently connected bridge.
     */
    async loadFile(path, noProgress = false) {
        if (!this.#connection) {
            throw new Error("No controller connected");
        }

        const bridge = this.#connection.bridge;
        const that = this;
        return new Promise(function(resolve, reject) {
            bridge.throwExceptionsOnReceive = true;

            bridge.onReceiveStart = async function(data) {                
                if (noProgress) return;
                that.#controller.ui.progress(0, "Loading " + data.path);
            };

            bridge.onReceiveProgress = async function(data) {
                if (noProgress) return;
                that.#controller.ui.progress((data.chunk + 1) / data.numChunks, "Loading " + data.path); //"Loading chunk " + data.chunk + " of " + data.numChunks);
            };

            bridge.onReceiveFinish = async function(data) {
                if (!noProgress) that.#controller.ui.progress(1);
                resolve(data.data);
            }

            bridge.onError = async function(message) {
                console.error(message);
                reject(message)
            }  
    
            bridge.request(path, BRIDGE_CHUNK_SIZE_REQUEST).catch(reject);
        })        
    }

    /**
     * Saves the passed content to the passed file on the connected device
     */
    async saveFile(path, content) {
        if (!this.#connection) {
            throw new Error("No controller connected");
        }

        const bridge = this.#connection.bridge;
        const that = this;
        return new Promise(function(resolve, reject) {
            bridge.throwExceptionsOnReceive = true;

            let transmissionId = null;

            // Progress (send)
            bridge.onSendProgress = async function(data) {            
                if (data.type == "error") return;

                if (data.path != path) return;
                transmissionId = JSON.stringify(Array.from(data.transmissionId));

                that.#controller.ui.progress((data.chunk + 1) / data.numChunks, "Writing " + data.path); // + ": Writing chunk " + data.chunk + " of " + data.numChunks);

            };

            bridge.onError = async function(message) {
                console.error(message);
                reject(message)
            }  
    
            // The bridge calls this only after the final chunk has been sent and acknowledged.
            bridge.onReceiveAck = async function(data) {
                if (JSON.stringify(Array.from(data.transmissionId)) == transmissionId) resolve();
            };

            bridge.sendString(path, content, BRIDGE_CHUNK_SIZE_SEND).catch(reject);
        })        
    }
}