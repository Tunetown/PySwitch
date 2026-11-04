describe('DeviceController file operations', function() {
    let device;
    let bridge;
    let packets;

    async function flush() {
        await new Promise(function(resolve) { setTimeout(resolve, 0); });
    }

    function track(promise) {
        const result = { state: 'pending' };
        promise.then(function(value) {
            result.state = 'fulfilled';
            result.value = value;
        }, function(error) {
            result.state = 'rejected';
            result.error = error;
        });
        return result;
    }

    async function acknowledge(packet) {
        const payload = packet.slice(4, 12);
        await bridge.receive({
            manufacturerId: [0, 124, 125],
            data: [4].concat(Array.from(bridge.getChecksum(new Uint8Array(payload))), payload)
        });
    }

    beforeEach(async function() {
        spyOn(console, 'error');
        bridge = new JsMidiBridge();
        packets = [];
        bridge.sendSysex = async function(manufacturerId, data) {
            packets.push(data);
        };
        device = new DeviceController({ midi: {}, ui: { progress: function() {} } });
        device.bridge.connect = async function() { return { name: 'test', bridge: bridge }; };
        await device.connect('test');
    });

    it('rejects an empty read path instead of leaving the caller pending', async function() {
        const result = track(device.loadFile(''));
        await flush();
        expect(result.state).toBe('rejected');
        expect(result.error && result.error.message).toBe('No path');
        expect(packets.length).toBe(0);
    });

    it('rejects unsupported empty saves instead of leaving the caller pending', async function() {
        const result = track(device.saveFile('inputs.py', ''));
        await flush();
        expect(result.state).toBe('rejected');
        expect(result.error && result.error.message).toBe('No message');
        expect(packets.length).toBe(0);
    });

    it('propagates initial read and write transport failures', async function() {
        const error = new Error('MIDI output unavailable');
        bridge.sendSysex = async function() { throw error; };
        const read = track(device.loadFile('inputs.py'));
        await flush();
        expect(read.state).toBe('rejected');
        expect(read.error).toBe(error);
        const write = track(device.saveFile('inputs.py', 'content'));
        await flush();
        expect(write.state).toBe('rejected');
        expect(write.error).toBe(error);
    });

    it('returns received file contents', async function() {
        const result = track(device.loadFile('inputs.py'));
        const peer = new JsMidiBridge();
        const incoming = [];
        peer.sendSysex = async function(manufacturerId, data) {
            incoming.push({ manufacturerId: manufacturerId, data: data });
        };
        await peer.sendString('inputs.py', 'print("hello")', 100);
        for (const packet of incoming) await bridge.receive(packet);
        await flush();
        expect(result.state).toBe('fulfilled');
        expect(result.value).toBe('print("hello")');
    });

    it('rejects errors received from the device', async function() {
        const result = track(device.loadFile('missing.py'));
        const peer = new JsMidiBridge();
        const incoming = [];
        peer.sendSysex = async function(manufacturerId, data) {
            incoming.push({ manufacturerId: manufacturerId, data: data });
        };
        await peer.error('File not found');
        for (const packet of incoming) await bridge.receive(packet);
        await flush();
        expect(result.state).toBe('rejected');
        expect(result.error).toBe('File not found');
    });

    it('waits for the single data chunk transport and its final acknowledgement', async function() {
        let release;
        const blocked = new Promise(function(resolve) { release = resolve; });
        bridge.sendSysex = async function(manufacturerId, data) {
            packets.push(data);
            if (data[0] == 3) await blocked;
        };
        const result = track(device.saveFile('inputs.py', 'content'));
        await flush();
        expect(packets.map(function(packet) { return packet[0]; })).toEqual([2, 3]);
        expect(result.state).toBe('pending');
        await expectAsync(acknowledge(packets[1])).toBeRejectedWithError('Invalid ack chunk: 0');
        expect(result.state).toBe('pending');
        release();
        await flush();
        expect(result.state).toBe('pending');
        await acknowledge(packets[1]);
        await flush();
        expect(result.state).toBe('fulfilled');
    });

    it('waits for the matching final acknowledgement of a multi-chunk file', async function() {
        const result = track(device.saveFile('inputs.py', 'x'.repeat(BRIDGE_CHUNK_SIZE_SEND + 1)));
        await flush();
        expect(result.state).toBe('pending');
        await acknowledge(packets[1]);
        await flush();
        expect(packets.length).toBe(3);
        expect(result.state).toBe('pending');
        await bridge.onReceiveAck({ transmissionId: new Uint8Array([127, 127, 127, 127]) });
        await flush();
        expect(result.state).toBe('pending');
        await acknowledge(packets[2]);
        await flush();
        expect(result.state).toBe('fulfilled');
    });

    it('does not start display.py until inputs.py has been acknowledged', async function() {
        const result = track(device.saveConfig({ get: async function() {
            return { inputs_py: 'inputs', display_py: 'display' };
        } }, 'test'));
        await flush();
        expect(packets.length).toBe(2);
        expect(result.state).toBe('pending');
        await acknowledge(packets[1]);
        await flush();
        expect(packets.length).toBe(4);
        expect(result.state).toBe('pending');
        await acknowledge(packets[3]);
        await flush();
        expect(result.state).toBe('fulfilled');
    });
});
