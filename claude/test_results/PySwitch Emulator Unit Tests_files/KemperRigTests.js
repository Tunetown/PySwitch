class KemperRigTests extends KemperTestBase {

    async testRigUp(switchDef, options = {}) {
        await this.loadInfo();

        await this.runner.setRigId(0);

        expect(this.runner.runner.client.getRigId()).toBe(0);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));

        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(1);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(2);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(3);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(4);
        if (options.keepBank) {
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));
        
            await this.runner.simulateSwitchPress(switchDef);

            expect(this.runner.runner.client.getRigId()).toBe(4);        
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));

        } else {
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(1, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(1, 1));
        
            await this.runner.simulateSwitchPress(switchDef);

            expect(this.runner.runner.client.getRigId()).toBe(5);    
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(1, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(1, 1));
        
            // Overflow
            await this.runner.setRigId(125 * 5 - 1);
            expect(this.runner.runner.client.getRigId()).toBe(624);
            await this.runner.simulateSwitchPress(switchDef);

            expect(this.runner.runner.client.getRigId()).toBe(0);
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(0, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(0, 1));
        }
    }
    
    async testRigDown(switchDef, options = {}) {
        await this.loadInfo();

        await this.runner.setRigId(23);

        expect(this.runner.runner.client.getRigId()).toBe(23);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 1));

        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(22);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 1));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(21);
        expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.3));
        if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 1));
        
        await this.runner.simulateSwitchPress(switchDef);

        expect(this.runner.runner.client.getRigId()).toBe(20);
        if (options.keepBank) {
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 1));
        
            await this.runner.simulateSwitchPress(switchDef);
            
            expect(this.runner.runner.client.getRigId()).toBe(20);    
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(4, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(4, 1));

        } else {
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(3, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(3, 1));
        
            await this.runner.simulateSwitchPress(switchDef);

            expect(this.runner.runner.client.getRigId()).toBe(19);
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(3, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(3, 1));

            // Overflow
            await this.runner.setRigId(0);
            await this.runner.simulateSwitchPress(switchDef);
            
            expect(this.runner.runner.client.getRigId()).toBe(125 * 5 - 1);    
            expect(this.runner.getSwitchColor(switchDef)).toEqual(this.bankColor(124, 0.3));
            if (options.labelTestCoordinates) expect(this.runner.getDisplayColorAt(options.labelTestCoordinates)).toEqual(this.bankColor(124, 1));    
        }
    }
}