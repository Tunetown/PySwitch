class KemperInfoProvider {

    data = null;

    #runner = null;

    constructor(runner) {
        this.#runner = runner;
    }

    /**
     * Get general info from the kemper client script (like number of banks/rigs, colors etc.)
     */
    async init() {
        this.data = (await this.#runner.pyswitch.pyodide.runPython(`
            import sys
            from unittest.mock import patch

            from mocks import *
            from wrappers.wrap_adafruit_display import *
            
            with patch.dict(sys.modules, {
                "micropython": MockMicropython,
                "displayio": WrapDisplayIO(),
                "adafruit_display_text": WrapAdafruitDisplayText("pyswitch"),
                "adafruit_display_shapes.rect": WrapDisplayShapes().rect(),
            }):    
                from pyswitch.clients.kemper import BANK_COLORS, NUM_BANKS, NUM_RIGS_PER_BANK
            
            {
                "bankColors": BANK_COLORS,
                "numBanks": NUM_BANKS,
                "numRigsPerBank": NUM_RIGS_PER_BANK
            }
        `)).toJs();
    }
}