/**
 * Implementations for PaintAudio devices
 */
class PaintAudioDevice extends Device {

    #filename = null;

    constructor(filename) {
        super();
        this.#filename = filename;
    }

    /**
     * Returns the hardware definition script file name in the lib/pyswitch/hardware/devices/ folder
     */
    getHardwareImportPath() {
        return "pyswitch.hardware.devices." + this.#filename
    }

    /**
     * Returns the class(es) to set on the device element
     */
    getDeviceClass() {
        switch (this.#filename) {
            case 'pa_midicaptain_nano_4':
                return "midicaptain midicaptain-nano-4";

            case 'pa_midicaptain_mini_6':
                return "midicaptain midicaptain-mini-6";

            case 'pa_midicaptain_10':
                return "midicaptain midicaptain-10";
        }

        throw new Error("Unknown device file: " + this.#filename);
    }

    /**
     * Returns if the device has any additional inputs
     */
    hasAdditionalInputs() {
        return this.#filename == 'pa_midicaptain_10';
    }

    /**
     * For a given input data model (as returned by parser.getHardwareInfo()), this returns if the 
     * input is additional and should be rendered in a separate panel.
     */
    isAdditionalInput(model) {
        switch(model.port) {
            case 27: return true;  // Exp. Pedal 1
            case 28: return true;  // Exp. Pedal 2
            case 2: return true;   // Wheel Encoder
            case 0: return true;   // Wheel Button            
        }
        return false;
    }

    /**
     * For the parser frontend, this can create additional content DOM added to the inputs container.
     */
    async createAdditionalInputs(controller) {
        if (!this.hasAdditionalInputs()) return null;

        return $('<span class="midicaptain midicaptain-10 additional-inputs-link" data-toggle="tooltip" title="Show/hide additional inputs" />')
        .on('click', async function() {
            try {
                controller.ui.showAdditionalInputs(!controller.ui.additionalInputsShown());
            } catch (e) {
                controller.handle(e);
            }
        });
    }

    /**
     * Must return an array with [width, height]
     */
    getDisplayDimensions() {
        return [240, 240]
    }
}