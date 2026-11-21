/**
 * Base class for virtual clients
 */
class VirtualClient {

    name = null;
    messageQueue = [];   // Queue of raw MIDI bytes. Will be filled here message by message, and fetched from the python midi wrappers
    
    constructor(name) {
        this.name = name;
    }
    
    /**
     * Send a MIDI message. Expects a byte array of raw data.
     */
    async send(message) {  
        const msgJs = message.toJs();
        const that = this;
        setTimeout(async function() {
            await that.doSend(msgJs);
        }, 0);
    }

    doSend(message) {
    }

    /**
     * Start processing regular updates to send messages. If not set, the caller has to 
     * call update() regularly.
     */
    run(updateInterval) {
    }

    /**
     * When running, this is called regularly to update the protocol and other timed stuff
     */
    update() {
    }

    /**
     * Stop listening to the input, and remove all UIs
     */
    detach() {        
    }

    /**
     * If supported, can create a user interface in the passed container DOM element
     */
    getUserInterface(container) {
    }

    /**
     * Tries to return a meaningful message name etc.
     */
    getMessageProperties(message) {
        return null;
    }
}