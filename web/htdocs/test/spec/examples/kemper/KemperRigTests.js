/**
 * Tests for the Kemper rig actions (RIG_UP, RIG_DOWN)
 */
class KemperRigTests extends KemperTestBase {

    static NUM_RIGS = 125 * 5;

    /**
     * RIG_UP: rig ID +1 per press. LED and label show the color of the bank of the target rig.
     * options: { 
     *     keepBank: true if the action stays in the current bank (stops at the last rig of the bank), 
     *     labelTestCoordinates: [x, y] of a pixel of the label 
     * }
     */
    async testRigUp(name, options = {}) {
        await this.#testRigUpDown(name, 1, 0, options);
    }
    
    /**
     * RIG_DOWN: rig ID -1 per press. LED and label show the color of the bank of the target rig.
     * options: see testRigUp()
     */
    async testRigDown(name, options = {}) {
        await this.#testRigUpDown(name, -1, 23, options);
    }

    /**
     * Presses the switch 5 times starting at the passed rig ID, then tests the overflow (if not keepBank)
     */
    async #testRigUpDown(name, step, startRigId, options) {
        await this.loadInfo();

        const that = this;
        async function check(rigId) {
            expect(that.client.getRigId()).toBe(rigId);

            const bank = Math.floor(that.#target(rigId, step, options.keepBank) / 5);
            that.expectColors(name, that.bankColor(bank, 0.3), options.labelTestCoordinates, that.bankColor(bank, 1));
        }

        await this.setRigId(startRigId);
        await check(startRigId);

        let rigId = startRigId;
        for (let i = 0; i < 5; ++i) {
            await this.press(name);
            rigId = this.#target(rigId, step, options.keepBank);
            await check(rigId);
        }

        if (!options.keepBank) {
            // Overflow
            const lastRigId = (step > 0) ? KemperRigTests.NUM_RIGS - 1 : 0;
            await this.setRigId(lastRigId);
            await this.press(name);
            await check(this.#target(lastRigId, step, false));
        }
    }

    /**
     * Returns the target rig ID of a rig up/down action
     */
    #target(rigId, step, keepBank) {
        if (keepBank) {
            const bankStart = Math.floor(rigId / 5) * 5;
            return Math.min(Math.max(rigId + step, bankStart), bankStart + 4);
        }
        return (rigId + step + KemperRigTests.NUM_RIGS) % KemperRigTests.NUM_RIGS;
    }
}
