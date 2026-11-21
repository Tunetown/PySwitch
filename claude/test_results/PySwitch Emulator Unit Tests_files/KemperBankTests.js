class KemperBankTests extends KemperTestBase {

    async testBankUp(switchDef, options = {}) {
        await this.loadInfo();

        await this.runner.setRigId(0);
        
        expect(this.runner.runner.client.getRigId()).toBe(0);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 0.2));

        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(5);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(1, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(1, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);
        
        expect(this.runner.runner.client.getRigId()).toBe(10);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(2, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(2, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(15);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(3, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(3, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(20);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(25); 
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(5, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(5, 0.2));

        // Overflow
        await this.runner.setRigId(125 * 5 - 1);
        
        expect(this.runner.runner.client.getRigId()).toBe(125 * 5 - 1);  
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(124, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(124, 0.2));

        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(4);  
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 0.2));
    }
    

    async testBankDown(switchDef, options = {}) {
        await this.loadInfo();

        await this.runner.setRigId(23);

        expect(this.runner.runner.client.getRigId()).toBe(23);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 0.2));

        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(18);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(3, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(3, 0.2));

        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(13);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(2, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(2, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(8);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(1, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(1, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(3);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 0.2));
        
        await this.runner.simulateSwitchPress(switchDef);
        
        expect(this.runner.runner.client.getRigId()).toBe(125 * 5 - 2);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(124, 0.02));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(124, 0.2));
    }
}