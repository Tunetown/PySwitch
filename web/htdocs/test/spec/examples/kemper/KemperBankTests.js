/**
 * Tests for the Kemper bank actions (BANK_UP, BANK_DOWN)
 */
class KemperBankTests extends KemperTestBase {

    /**
     * BANK_UP: rig ID +5 per press, LED and label in the color of the bank, overflow to bank 1.
     * options: { labelTestCoordinates: [x, y] of a pixel of the label }
     */
    async testBankUp(name, options = {}) {
        await this.loadInfo();

        await this.setRigId(0);
        expect(this.client.getRigId()).toBe(0);
        this.expectColors(name, this.bankColor(0, 0.02), options.labelTestCoordinates, this.bankColor(0, 0.2));

        for (let bank = 1; bank <= 5; ++bank) {
            await this.press(name);

            expect(this.client.getRigId()).toBe(bank * 5);
            this.expectColors(name, this.bankColor(bank, 0.02), options.labelTestCoordinates, this.bankColor(bank, 0.2));
        }

        // Overflow
        await this.setRigId(125 * 5 - 1);
        await this.press(name);

        expect(this.client.getRigId()).toBe(4);
        this.expectColors(name, this.bankColor(0, 0.02), options.labelTestCoordinates, this.bankColor(0, 0.2));
    }

    /**
     * BANK_DOWN: rig ID -5 per press, LED and label in the color of the bank, overflow to the last bank.
     * options: { labelTestCoordinates: [x, y] of a pixel of the label }
     */
    async testBankDown(name, options = {}) {
        await this.loadInfo();

        await this.setRigId(23);
        expect(this.client.getRigId()).toBe(23);
        this.expectColors(name, this.bankColor(4, 0.02), options.labelTestCoordinates, this.bankColor(4, 0.2));

        for (let bank = 3; bank >= 0; --bank) {
            await this.press(name);

            expect(this.client.getRigId()).toBe(bank * 5 + 3);
            this.expectColors(name, this.bankColor(bank, 0.02), options.labelTestCoordinates, this.bankColor(bank, 0.2));
        }

        // Overflow
        await this.press(name);

        expect(this.client.getRigId()).toBe(125 * 5 - 2);
        this.expectColors(name, this.bankColor(124, 0.02), options.labelTestCoordinates, this.bankColor(124, 0.2));
    }
}
