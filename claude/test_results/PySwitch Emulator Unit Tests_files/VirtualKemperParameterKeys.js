class VirtualKemperParameterKeys {
    send = null;
    receive = null;

    /**
     * {
     *      send:     Key instance for sending data to the controller. Also used for receiving requests for values. Cannot be an array. Optional.
     *      receive:  Key instance(s) for receiving data. Can be an array. If not set, the send key will be used.
     * }
     */
    constructor(options) {
        this.send = options.send;
        this.receive = options.receive;

        // Ensure that receiveKey is an Array
        if (this.receive) {
            if (!Array.isArray(this.receive)) {
                // Single entry
                this.receive = [this.receive];
            }

            // Alse receive values for the sending key
            if (this.send) {
                this.receive.push(this.send);
            }
        } else {
            if (!this.send) {
                throw new Error("Invalid definitions for keys");
            }

            // Use send key as receive key
            this.receive = [this.send];
        }

        if (this.send && !(this.send instanceof ParameterKey)) throw new Error("Invalid send key");
        
        for (const r of this.receive) {
            if (!(r instanceof ParameterKey)) throw new Error("Invalid receive key");
        }        
    }

    /**
     * Get ID of the constellation
     */
    getId() {
        if (this.send) return this.send.getId();

        let ret = "";
        for (const r of this.receive) {
            ret += r.getId();
        }
        return ret;
    }

    /**
     * Name to display
     */
    getDisplayName() {
        if (this.send) return this.send.getDisplayName();

        const ret = [];
        for (const r of this.receive) {
            ret.push(r.getDisplayName());
        }
        return ret.join(", ");
    }
}

/**************************************************************/

class ParameterKey {

    /**
     * Must return a unique ID from the key
     */
    getId() {
        throw new Error("Must be implemented in child classes");
    }

    /**
     * Name to display
     */
    getDisplayName() {
        throw new Error("Must be implemented in child classes");
    }

    evaluateValue(valueOrData, valueType) {
        return valueOrData;
    }

    /**
     * Returns a representation for sending
     */
    encodeValue(value) {
        return value;
    }
}

/**
 * Key for a NRPN parameter
 */
class NRPNKey extends ParameterKey {
    constructor(data) {
        super();

        if (!(Array.isArray(data) || (data instanceof Uint8Array))) throw new Error("Invalid NRPN data")
        this.data = Array.from(data);
    }

    getId() {
        return JSON.stringify({ data: this.data });
    }

    getDisplayName() {
        return "NRPN " + this.data.join("|");
    }

    evaluateValue(data, valueType) {
        switch (valueType) {
            case "number":
                return data[0] * 128 + data[1];

            case "string":
                return Tools.data2string(data);

            default:
                throw new Error("Invalid value type: " + valueType);
        }
    }

    /**
     * Returns a byte array containing the value
     */
    encodeValue(value) {
        switch (typeof value) {
            case "number":
                const lsb = value % 128;
                const msb = Math.floor(value / 128);
                return [msb, lsb];

            case "string":
                const ret = [];
                for (var i = 0; i < value.length; ++i) {
                    ret.push(value.charCodeAt(i));                    
                }
                ret.push(0);   // Null termination
                return ret;

            default:
                throw new Error("Invalid value type: " + (typeof value));
        }
    }
}

/**
 * Key for a CC parameter
 */
class CCKey extends ParameterKey {
    constructor(control, options = {}) {
        super();

        if (typeof control != "number") throw new Error("Invalid CC control")

        this.control = control;
        this.options = options;
    }

    getId() {
        return JSON.stringify({ control: this.control });
    }

    getDisplayName() {
        return "CC " + this.control;
    }

    encodeValue(value) {
        if (this.options.hasOwnProperty("scale")) {
            return Math.floor(value / this.options.scale);
        }
        return value;
    }

    evaluateValue(value, valueType = null) {
        if (this.options.hasOwnProperty("scale")) {
            return value * this.options.scale;
        }
        return value;        
    }
}

/**
 * Key for a PC parameter
 */
class PCKey extends ParameterKey {
    getId() {
        return JSON.stringify({ program: true });
    }

    getDisplayName() {
        return "PC";
    }
}