/**
 * (C) Thomas Weber 2024 tom-vibrant@gmx.de
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>. 
 */

/**
 * Chunk size for requesting data. The Web MIDI API does silently fail on incoming messages
 * too big, by experiment 111 was the value which was working any time. Should be fixed with
 * issue https://github.com/WebAudio/web-midi-api/issues/158 of the Web MIDI API, which sadly is 
 * still open at the time of writing this (12/2024). Later this could be enlarged to reduce
 * protocol overhead.
 */
const BRIDGE_CHUNK_SIZE_REQUEST = 100;

/**
 * Chunk size for sending data. This also has been determined empirically.
 */
const BRIDGE_CHUNK_SIZE_SEND = 65;

/**
 * Timeout until it is assumed there is no client listening
 */
const BRIDGE_TIMEOUT_INTERVAL_MILLIS = 10000;

/**
 * Use this class to initialize the bridge and connect it to Web MIDI API ports. 
 */
class MidiBridgeHandler {

    #midi = null;                // MidiHandler instance
    
    constructor(midi) {
        this.#midi = midi;
    }

    /**
     * Connect to a port input/output pair by port name. If you pass attemps (Map), an attempt will 
     * be added/removed from it to manage connection attempts in a scan.
     */
    async connect(portName, attempts = null, timeoutMillis = BRIDGE_TIMEOUT_INTERVAL_MILLIS) {
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

        const input = findPort(this.#midi.midiAccess.inputs);
        const output = findPort(this.#midi.midiAccess.outputs);

        // We use a name most likely not existing. If it does exist, this would also work,
        // but the overhead is bigger.
        const path = "/mostlikelynotexistingfolder/ping";

        return new Promise(function(resolve, reject) {
            const bridge = new JsMidiBridge();

            // Connect bridge output to the output
            bridge.send = async function(message) {
                await output.send(message);
            }

            function cleanup() {
                if (attempts) {
                    attempts.delete(portName);
                }

                // Stop the timout
                clearTimeout(timeout);
            }

            function doResolve(/*data*/) {
                cleanup();

                // Remove callbacks only used for pinging
                bridge.onReceiveFinish = async function() {};
                bridge.onError = async function() {};
                
                resolve({
                    bridge: bridge,
                    name: output.name,
                    input: input,
                    output: output
                });
            }

            function doReject() {
                cleanup();
                that.detach(bridge);
                reject(new Error("Failed to connect to " + output.name)); 
            }

            // Listen to both finish and error events to know there is a bridge listening
            bridge.onReceiveFinish = doResolve;
            bridge.onError = doResolve;
            
            // Attach listener
            that.#listenTo(input, bridge);

            // Request the non-existing file (async but not awaited)
            bridge.request(path, BRIDGE_CHUNK_SIZE_REQUEST);

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
     * Called with the result of connect(), this detaches the connection.
     */
    detach(bridge) {
        // Detach MIDI input
        this.#midi.removeListener(bridge.midiListener); 

        // Detach bridge
        bridge.send = async function() {};
        bridge.onReceiveFinish = async function() {};
        bridge.onError = async function() {};
        bridge.midiListener = null;
    }

    /**
     * Start listening to a port (connects the bridge to it)
     */
    #listenTo(input, bridge) {
        this.#midi.addListener(
            bridge.midiListener = new MidiListener(input.name, async function(data) {
                await bridge.receive(Array.from(data));
            })
        );
    }
}