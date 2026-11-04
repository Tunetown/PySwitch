describe('Protocol (Unicode)', function() {
    async function roundTrip(message, chunkSize, fromFile = false, path = 'unicode.txt') {
        const sender = new JsMidiBridge();
        const receiver = new JsMidiBridge();
        sender.throwExceptionsOnReceive = true;
        receiver.throwExceptionsOnReceive = true;
        const outgoing = [];
        const acknowledgements = [];
        const chunks = [];
        let received = null;
        let announcedChunks = null;
        let finished = false;

        sender.getFile = async function() { return message; };
        sender.sendSysex = async function(manufacturerId, data) {
            outgoing.push({ manufacturerId: manufacturerId, data: data });
        };
        receiver.sendSysex = async function(manufacturerId, data) {
            acknowledgements.push({ manufacturerId: manufacturerId, data: data });
        };
        receiver.onReceiveStart = async function(data) {
            expect(data.path).toBe(path);
            announcedChunks = data.numChunks;
        };
        receiver.onReceiveFinish = async function(data) { received = data.data; };
        sender.onReceiveAck = async function() { finished = true; };

        if (fromFile) await sender.sendFile(path, chunkSize);
        else await sender.sendString(path, message, chunkSize);

        while (outgoing.length) {
            const packet = outgoing.shift();
            if (packet.data[0] == 3) {
                const packed = new Uint8Array(packet.data.slice(12));
                const bytes = sender.unpackBytes(packed);
                const chunk = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
                chunks.push(chunk);
                expect(Array.from(chunk).length).toBeLessThanOrEqual(chunkSize);
            }
            await receiver.receive(packet);
            while (acknowledgements.length) await sender.receive(acknowledgements.shift());
        }
        expect(received).toBe(message);
        expect(chunks.join('')).toBe(message);
        expect(announcedChunks).toBe(Math.ceil(Array.from(message).length / chunkSize));
        expect(chunks.length).toBe(announcedChunks);
        expect(finished).toBe(true);
    }

    it('keeps a surrogate pair together across a string chunk boundary', async function() {
        await roundTrip('a'.repeat(64) + '😀b', 65);
    });

    it('counts astral file characters as one complete chunk character', async function() {
        await roundTrip('😀', 1, true);
    });

    it('round-trips mixed Unicode with one- and two-character chunks', async function() {
        for (const chunkSize of [1, 2]) {
            for (const fromFile of [false, true]) {
                await roundTrip('A😀𐐷é中', chunkSize, fromFile);
            }
        }
    });

    it('preserves literal U+FEFF in paths and at the start of each data chunk', async function() {
        await roundTrip('\ufeffa\ufeffb', 1, false, '\ufeffunicode.txt');
    });

});
