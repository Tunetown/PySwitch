/**
 * Base class for controller devices
 */
class Device {

    /**
     * Returns the device handler from the passed Configuration instance
     */
    static async getInstance(config) {
        const data = await config.get();

        if (data.inputs_py.includes("pyswitch.hardware.devices.pa_midicaptain_nano_4")) {
            return new PaintAudioDevice('pa_midicaptain_nano_4')
        }
        if (data.inputs_py.includes("pyswitch.hardware.devices.pa_midicaptain_mini_6")) {
            return new PaintAudioDevice('pa_midicaptain_mini_6')
        }
        if (data.inputs_py.includes("pyswitch.hardware.devices.pa_midicaptain_10")) {
            return new PaintAudioDevice('pa_midicaptain_10')
        }
        
        // Default device type: MidiCaptain 10
        return new PaintAudioDevice('pa_midicaptain_10');  //throw new Error("Unknown device type");
    }

    /**
     * Returns the hardware definition script file name in the lib/pyswitch/hardware/devices/ folder
     */
    getHardwareImportPath() {
        throw new Error("Implement this in child classes");
    }

    /**
     * Returns the class(es) to set on the device element
     */
    getDeviceClass() {
        throw new Error("Implement this in child classes");
    }

    /**
     * Returns if the device has any additional inputs
     */
    hasAdditionalInputs() {
        return false;
    }    

    /**
     * For a given input data model (as returned by parser.getHardwareInfo()), this returns if the 
     * input is additional and should be rendered in a separate panel.
     */
    isAdditionalInput(model) {
        return false;
    }

    /**
     * Must return an array with [width, height]
     */
    getDisplayDimensions() {
        return [0, 0]
    }

    /**
     * For the parser frontend, this can create additional content DOM added to the inputs container.
     */
    async createAdditionalInputs(controller) {
        return null;
    }
}