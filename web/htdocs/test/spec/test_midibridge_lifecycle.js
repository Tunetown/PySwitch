describe('MidiBridge file validation', function() {
    it('Send File: Reject empty contents before sending', async function() {
        const bridge = new JsMidiBridge();
        const packets = [];
        bridge.getFile = async function() { return ''; };
        bridge.sendSysex = async function(manufacturerId, data) { packets.push(data); };
        await expectAsync(bridge.sendFile('empty.txt', 65)).toBeRejectedWithError('empty.txt not found or empty');
        expect(packets).toEqual([]);
    });

});

describe('MidiBridge idle receive cleanup', function() {
    beforeEach(function() { jasmine.clock().install(); });
    afterEach(function() { jasmine.clock().uninstall(); });

    it('Timeout (Receive before first data chunk)', async function() {
        jasmine.clock().mockDate(new Date(1000));
        const sender = new JsMidiBridge();
        const receiver = new JsMidiBridge();
        receiver.throwExceptionsOnReceive = true;
        const packets = [];
        let received = null;
        sender.sendSysex = async function(manufacturerId, data) {
            packets.push({ manufacturerId: manufacturerId, data: data });
        };
        receiver.onReceiveFinish = async function(data) { received = data.data; };
        await sender.sendString('stalled.txt', 'stalled', 100);
        await receiver.receive(packets.shift());
        const delayedData = packets.shift();

        // As with existing receive timeouts, cleanup is triggered by a new transmission.
        jasmine.clock().mockDate(new Date(6001));
        await sender.sendString('active.txt', 'active', 100);
        await receiver.receive(packets.shift());
        await expectAsync(receiver.receive(delayedData)).toBeRejectedWithError(/Receive transmission .* not found/);
        await receiver.receive(packets.shift());
        expect(received).toBe('active');
    });

});
