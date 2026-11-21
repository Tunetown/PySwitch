class VirtualKemperParameterDefault extends VirtualKemperParameter {
    
    /**
     * Parse a parameter request message. Must return if successful.
     */
    parse(message) {
        if (this.#parseNRPNRequest(message)) return true;
        if (this.#parseNRPNSet(message)) return true;
        if (this.#parseCC(message)) return true;
        if (this.#parsePC(message)) return true;
        return false;
    }

    #parseNRPNRequest(message) {
        // Is it a request message for a NRPN parameter?
        if (!Tools.compareArrays(
            message.slice(0, 8),
            [240, 0, 32, 51, this.client.options.productType, 127, this.requestFunctionCode, 0]
        )) return false;

        // Requested an unknown parameter: Create it
        const newParam = this.client.parameters.get(new NRPNKey(message.slice(8, 10)));

        // Send parameter value
        newParam.send();

        return true;
    }

    #parseNRPNSet(message) {
        // Is it a set message for a NRPN parameter?
        if (!Tools.compareArrays(
            message.slice(0, 8),
            [240, 0, 32, 51, this.client.options.productType, 127, this.setFunctionCode, 0]
        )) return false;

        // Set an unknown parameter: Create it
        const newParam = this.client.parameters.get(new NRPNKey(message.slice(8, 10)));
        if (!newParam.parse(message)) throw new Error("Failed to create parameter for message: ", message);

        return true;
    }

    #parseCC(message) {
        // Is it a CC message?
        if (message[0] != 176) return false;

        // Requested an unknown parameter: Create it
        const newParam = this.client.parameters.get(new CCKey(message[1]));
        if (!newParam.parse(message)) throw new Error("Failed to create parameter for message: ", message);

        return true;
    }

    #parsePC(message) {
        // Is it a PC message?
        if (message[0] != 192) return false;

        // Requested an unknown parameter: Create it
        const newParam = this.client.parameters.get(new PCKey());
        if (!newParam.parse(message)) throw new Error("Failed to create parameter for message: ", message);

        return true;
    }

    /**
     * Send a single parameter (numeric or string)
     */
    send() {
        throw new Error("This shall not be called");
    }

    /**
     * Name for display
     */
    getDisplayName() {
        return "Default: " + (typeof this.value);
    }
}