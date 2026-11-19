/**
 * MIDI Bridge to transfer string data between devices via MIDI.
 * 
 * (C) Thomas Weber 2024 tom-vibrant@gmx.de
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * This class can transfer data from/to a MIDI connection, by interfacing with itself (or a port of 
 * it) on the other device using SystemExclusive messages.
 */

/**
 * Bridge version
 */
const JMB_VERSION = "0.6.0";

/**
 * Manufacturer ID of JsMidiBridge
 */
const JMB_MANUFACTURER_ID = [0x00, 0x7c, 0x7d];

/**
 * Command prefix to request a file to be transfered.
 * Syntax: [
 *     *PMB_REQUEST_MESSAGE,
 *     <CRC-16, 3 half-bytes (only first 16 bits used, calculated over the rest of the message)>,
 *     <Requested chunk size, 4 half-bytes>
 *     <Path name as utf-8 bytes with no null termination>
 * ]
 */
const JMB_REQUEST_MESSAGE = [0x01];

/** 
 * Command prefix to signal start of transfer. The file ID is a random requence used to identify 
 * the file during the transfer, and is not used afterwards.
 *
 * Syntax: [
 *     *PMB_START_MESSAGE,
 *     <CRC-16, 3 half-bytes (only first 16 bits used, calculated over the rest of the message)>,
 *     <Transmission id, 4 half-bytes>,
 *     <Transmission type, 1 half-byte>,
 *     <Amount of chunks to be expected, 4 half-bytes>
 *     <Path name as utf-8 bytes with no null termination>
 * ]
 */
const JMB_START_MESSAGE = [0x02];

/**
 * Command prefix for sending data chunks
 * Syntax: [
 *     *PMB_DATA_MESSAGE,
 *     <CRC-16, 3 half-bytes (only first 16 bits used, calculated over the rest of the message)>,
 *     <Transmission id, 4 half-bytes>,
 *     <Chunk index, 4 half-bytes>,
 *     <Payload, variable length>
 * ]
 */
const JMB_DATA_MESSAGE = [0x03];

/**
 * Command prefix for the acknowledge message, which is sent to acknowledge a chunk.
 * Syntax: [
 *     *PMB_ACK_MESSAGE,
 *     <CRC-16, 3 half-bytes (only first 16 bits used, calculated over the rest of the message)>,
 *     <Transmission id, 4 half-bytes>,
 *     <Chunk index, 4 half-bytes>
 * ]
 */
const JMB_ACK_MESSAGE = [0x04];


//////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Transmission types
const JMB_TRANSMISSION_TYPE_FILE = [0x00];
const JMB_TRANSMISSION_TYPE_ERROR = [0x01];


//////////////////////////////////////////////////////////////////////////////////////////////////////////////


/** 
 * All command prefixes above have to be exactly this long
 */ 
const JMB_PREFIXES_LENGTH_HALFBYTES = 1; 

/** 
 * Size of the chunk index (BEFORE packing! Therefore, 3 bytes will use 4 bytes in the end.)
 */ 
const JMB_NUMBER_SIZE_FULLBYTES = 3;
const JMB_NUMBER_SIZE_HALFBYTES = 4;

/** 
 * Length of the file id (BEFORE packing! Therefore, 3 bytes will use 4 bytes in the end.) 
 */ 
const JMB_TRANSMISSION_ID_LENGTH_FULLBYTES = 3;
const JMB_TRANSMISSION_ID_LENGTH_HALFBYTES = 4;

/** 
 * Length of the checksum in the message. Must fit for 16 bits, so we need at least 3 MIDI half-bytes. 
 */ 
const JMB_CHECKSUM_LENGTH_FULLBYTES = 2;
const JMB_CHECKSUM_LENGTH_HALFBYTES = 3;


/**
 * Chunk size for sending errors. Keep this small to be compatible to all clients.
 */
const JMB_ERROR_CHUNK_SIZE = 100;

/**
 * Timout for inactive transmissions (milliseconds)
 */
const JMB_TIMEOUT_MILLIS = 5000;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////


/**
 * MIDI Bridge
 */
class JsMidiBridge {

    static nextId = -1;                     // Next transmission ID

	#sendTransmissions = null;               // Transmissions map for sending (key is the transmission ID)
    #receiveTransmissions = null;            // Transmissions map for receiving (key is the transmission ID)

    throwExceptionsOnReceive = false;        // When receiving messages, throw exceptions instead of sending an error message (for testing)
    
    console = {
        log: function() {},
        error: function() {}
    }

    /**
     * Callback on errors received from the other side. message will be a string.
     */
    onError = async function(message) { console.error("Error from MIDI client: " + message) };

    /**
     * Callback to send System Exclusive MIDI messages. Both parameters will be arrays of integers in range [0..127].
     */
    send = async function(manufacturerId, data) { };

    /**
     * Callback to get file contents for the given path or file ID. Path will be a string.
     */
    getFile = async function(path) { throw new Error("No getFile callback set, cannot get data for " + path) };

    /**
     * Called on every sent chunk. Data:
     * {
     *     path: 
     *     transmissionId:
     *     chunk:      Index of the current chunk
     *     numChunks:
     * }
     */
    onSendProgress = async function(data) {};

    /**
     * Called when receiving starts. Data:
     * {
     *     path: 
     *     transmissionId:
     *     transmissionType:
     *     numChunks:
     * }
     */
    onReceiveStart = async function(data) {};
    
    /**
     * Called on every received chunk. Data:
     * {
     *     path: 
     *     transmissionId:
     *     chunk:      Index of the current chunk
     *     numChunks:
     * }
     */
    onReceiveProgress = async function(data) {};

    /**
     * Called when a file has fully been received.
     * {
     *     path: 
     *     transmissionId:
     *     data:       The string data
     *     numChunks:
     * }
     */
    onReceiveFinish = async function(data) {};

    /**
     * Called when a client sent the final ack message. Data:
     * {
     *     transmissionId:
     * }
     */
    onReceiveAck = async function(data) {};


    constructor() {
        this.#sendTransmissions = new Map();
        this.#receiveTransmissions = new Map();
    }

    // Send Messages ##########################################################################################################

    /**
	 * Opens a file, and send it in chunks (also called internally when a request comes in)
	 */
    async sendFile(path, chunkSize) {
        if (!path) {
			throw new Error("No path");
		}

        if (chunkSize < 1) {
			throw new Error("Invalid chunk size: " + chunkSize);
		}
       
        // Check if file exists and see how many chunks we will need
        let data = await this.getFile(path);
        if (data === null) {
            throw new Error(path + " not found or empty");
        }

        await this.#startSendTransmission({
            path: path, 
            amountChunks: Math.ceil(data.length / chunkSize),
            chunkSize: chunkSize, 
            message: data,
            type: JMB_TRANSMISSION_TYPE_FILE
        });
    }


    /**
	 * Directly send a string in chunks.
	 */
    async sendString(path, message, chunkSize, transmission_type = JMB_TRANSMISSION_TYPE_FILE) {
        if (!message || message.length == 0) {
			throw new Error("No message");
		}

        if (chunkSize < 1) {
			throw new Error("Invalid chunk size: " + chunkSize);
		}

        await this.#startSendTransmission({
            path: path, 
            amountChunks: Math.ceil(message.length / chunkSize),
            chunkSize: chunkSize,             
            message: message,
            type: transmission_type
        });
    }


    /**
     * Adds a send transmission definition and sends the start message
     */
    async #startSendTransmission(transmission) {
        transmission.nextChunk = 0;
        transmission.id = this.generateTransmissionId();

        this.#cleanupTransmissions();
        this.#sendTransmissions.set(JSON.stringify(transmission.id), transmission);

        this.console.log("Start sending", transmission);
        this.console.log("Number of send transmissions: " + this.#sendTransmissions.size);
        
        // Send start message and first chunk
        await this.#sendStartMessage(transmission);
        await this.#sendNextChunk(transmission);
    }


    /**
     * Send next chunk for the passed transmission
     */
    async #sendNextChunk(transmission) {
        // Read data        
        const chunk = transmission.message.slice(0, transmission.chunkSize);
        transmission.message = transmission.message.slice(transmission.chunkSize);
        
        await this.#sendChunk(transmission, chunk);

        transmission.nextChunk += 1;

        // Update timestamp
        transmission.time = Date.now();
    }
    

    /**
	 * Sends a MIDI message to request a file
	 */ 
    async request(path, chunkSize) {
        if (!path) {
			throw new Error("No path");
		}
        
        if (chunkSize < 1) {
			throw new Error("Invalid chunk size: " + chunkSize);
		}

        const payload = Array.from(this.number2bytes(chunkSize, JMB_NUMBER_SIZE_FULLBYTES)).concat(Array.from(this.string2bytes(path)));
        const checksum = Array.from(this.getChecksum(new Uint8Array(payload)));

        await this.#sendSysex(
			JMB_MANUFACTURER_ID,
            JMB_REQUEST_MESSAGE.concat(checksum, payload)
		);
    }
    

    /** 
	 * Send the "Start of transmission" message
	 */ 
    async #sendStartMessage(transmission) {
        const amountChunksArray = Array.from(this.number2bytes(transmission.amountChunks, JMB_NUMBER_SIZE_FULLBYTES));   
        
        const payload = [].concat(
            Array.from(transmission.id),
            Array.from(transmission.type), 
            amountChunksArray, 
            Array.from(this.string2bytes(transmission.path))
        );
        const checksum = Array.from(this.getChecksum(new Uint8Array(payload)));
        
        this.console.log("Start message" + JSON.stringify(transmission));
        
        await this.#sendSysex(
			JMB_MANUFACTURER_ID,
            JMB_START_MESSAGE.concat(checksum, payload)
		);
    }


    /**
	 * Sends one chunk of data
	 */ 
    async #sendChunk(transmission, chunk) {
        const dataBytes = Array.from(this.string2bytes(chunk));
        const chunkIndexBytes = Array.from(this.number2bytes(transmission.nextChunk, JMB_NUMBER_SIZE_FULLBYTES));
        
        const payload = [].concat(
            Array.from(transmission.id),
            chunkIndexBytes, 
            dataBytes
        );
        const checksum = Array.from(this.getChecksum(new Uint8Array(payload)));
        
        const isFile = JSON.stringify(Array.from(transmission.type)) == JSON.stringify(Array.from(JMB_TRANSMISSION_TYPE_FILE));

        await this.onSendProgress({
			path: transmission.path,
			transmissionId: transmission.id,
			chunk: transmission.nextChunk,
			numChunks: transmission.amountChunks,
            type: isFile ? "file" : "error"
        });

        this.console.log("Send data chunk " + transmission.nextChunk + ", " + (checksum.length + payload.length) + " bytes");
        
        await this.#sendSysex(
			JMB_MANUFACTURER_ID,
            JMB_DATA_MESSAGE.concat(checksum, payload)
		);
	}


    /** 
	 * Generate a transmission ID (4 bytes)
	 */ 
    generateTransmissionId() {
        if (JsMidiBridge.nextId < 0) {
            function getRandomInt(min, max) {
                min = Math.ceil(min);
                max = Math.floor(max);
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }

            // Initialize with random seed
            JsMidiBridge.nextId = getRandomInt(0, 16777216);
        }
        
        const result = this.number2bytes(JsMidiBridge.nextId, JMB_TRANSMISSION_ID_LENGTH_FULLBYTES);

        JsMidiBridge.nextId += 1;
        if (JsMidiBridge.nextId >= 16777216) {
            JsMidiBridge.nextId = 0;
        }

        return result;
    }


    // Receive Messages ##########################################################################################################


    /** 
	 * Must be called for every incoming MIDI message to receive data. This class only uses SysEx, so the incoming messages
     * have to feature the attributes "manufacturerId" and "data" to be regarded
	 */
    async receive(midiMessage) {
        // Check if the message has the necessary attributes
        if (!midiMessage || midiMessage[0] != 0xf0) {
			return false;
		}
        
        // Is the message for us?
        if (JSON.stringify(midiMessage.slice(1, 4)) != JSON.stringify(JMB_MANUFACTURER_ID)) {
			return false;
		}
        
        // This determines what the sender of the message wants to do
        const commandId = JSON.stringify(midiMessage.slice(
			4, 
			4 + JMB_PREFIXES_LENGTH_HALFBYTES
		))

        // Next there is the checksum for all messages
        const checksumBytes = new Uint8Array(midiMessage.slice(
			4 + JMB_PREFIXES_LENGTH_HALFBYTES,
			4 + JMB_PREFIXES_LENGTH_HALFBYTES + JMB_CHECKSUM_LENGTH_HALFBYTES
		));
        let payload = new Uint8Array(midiMessage.slice(
			4 + JMB_PREFIXES_LENGTH_HALFBYTES + JMB_CHECKSUM_LENGTH_HALFBYTES,
            -1
		));
		
		try {			
            // Checksum test
            if (!this.#compareArrays(this.getChecksum(payload), checksumBytes)) {
                throw new Error("Checksum mismatch");
            }    

            // Receive: Message to request sending a file
            if (commandId == JSON.stringify(JMB_REQUEST_MESSAGE)) {
                // Send file
                await this.#receiveRequest(payload);
                return true;
            }            

            // All other messages have a file ID coming next, so we split that off the payload
            const transmissionIdBytes = payload.slice(
				0, 
				JMB_TRANSMISSION_ID_LENGTH_HALFBYTES
			);
						
            payload = payload.slice(
				JMB_TRANSMISSION_ID_LENGTH_HALFBYTES
			);
			
            // Receive: Start of transmission
            if (commandId == JSON.stringify(JMB_START_MESSAGE)) {				
				await this.#receiveStart(transmissionIdBytes, payload);
            }

            // Receive: Data
            else if (commandId == JSON.stringify(JMB_DATA_MESSAGE)) {  
                await this.#receiveData(transmissionIdBytes, payload);
            }

            // Ack message
            else if (commandId == JSON.stringify(JMB_ACK_MESSAGE)) { 
                await this.#receiveAck(transmissionIdBytes, payload);                              
			}               

        } catch(ex) {
			if (this.throwExceptionsOnReceive) {
				throw ex;
			}

            //console.error(ex)
            await this.error(ex.message);
		}

        return true;
	}
	
    /**
     * Request message received
     */
    async #receiveRequest(payload) {
        const chunkSize = this.bytes2number(payload.slice(0, JMB_NUMBER_SIZE_HALFBYTES));
        const path = this.bytes2string(payload.slice(JMB_NUMBER_SIZE_HALFBYTES));

        await this.sendFile(path, chunkSize);
    }

    /**
	 * Start receiving file data
	 */
    async #receiveStart(transmissionIdBytes, payload) {
        // Create a new transmission in the list
        const transmission = {
            lastChunk: -1,
            id: transmissionIdBytes,
            type: payload.slice(0, JMB_PREFIXES_LENGTH_HALFBYTES),
            amountChunks: this.bytes2number(payload.slice(JMB_PREFIXES_LENGTH_HALFBYTES, JMB_NUMBER_SIZE_HALFBYTES + JMB_PREFIXES_LENGTH_HALFBYTES)),
            path:this.bytes2string(payload.slice(JMB_NUMBER_SIZE_HALFBYTES + JMB_PREFIXES_LENGTH_HALFBYTES)),
            buffer: ""
        };

        this.#cleanupTransmissions();
        this.#receiveTransmissions.set(JSON.stringify(transmissionIdBytes), transmission);
                
        // Signal start of transmission        
        await this.onReceiveStart({
			path: transmission.path,
			transmissionId: transmissionIdBytes,
            transmissionType: transmission.type,
			numChunks: transmission.amountChunks
		});

        this.console.log("Start receiving " + JSON.stringify(transmission));
        this.console.log("Number of receive transmissions: " + this.#receiveTransmissions.size);
	}      

    /**
	 * Receive file data
	 */ 
    async #receiveData(transmissionIdBytes, payload) {   
        const transmission = this.#receiveTransmissions.get(JSON.stringify(transmissionIdBytes));
        if (!transmission) {
            throw new Error("Receive transmission " + transmissionIdBytes + " not found");
        }

        // Index of the chunk
        const index = this.bytes2number(payload.slice(0, JMB_NUMBER_SIZE_HALFBYTES));

        // Chunk data
        const strData = this.bytes2string(payload.slice(JMB_NUMBER_SIZE_HALFBYTES));
    
        // Only accept if the chunk index is the one expected
        if (index != transmission.lastChunk + 1) {			
            throw new Error("Invalid chunk " + index + ", expected " + (transmission.lastChunk + 1));
        }
        
        transmission.lastChunk = index;

        // Append to file
        transmission.buffer += strData;

        // Send the ack message
        await this.#sendAckMessage(transmission.id, index);
            
        // Update timestamp
        transmission.time = Date.now();

        await this.onReceiveProgress({
			path: transmission.path,
			transmissionId: transmission.id,
			chunk: index,
			numChunks: transmission.amountChunks
		});
        
        // If this has been the last chunk, close the file handle and send ack message
        if (index == transmission.amountChunks - 1) {
            await this.#receiveFinish(transmission);
        }
        
        this.console.log("Received chunk " + index);
    }

    /**
	 * Finish receiving and send acknowledge message
	 */
    async #receiveFinish(transmission) {
        const type = JSON.stringify(Array.from(transmission.type));

        switch(type) {
            case JSON.stringify(JMB_TRANSMISSION_TYPE_FILE): {
                await this.onReceiveFinish({
                    transmissionId: transmission.id,
                    path: transmission.path,
                    data: transmission.buffer,
                    numChunks: transmission.amountChunks
                });
        
                break;
            }
            
            case JSON.stringify(JMB_TRANSMISSION_TYPE_ERROR): {
                await this.onError(transmission.buffer);

                break;
            }

            default: {
                throw new Error("Unknown transmission type: " + type);
            }
        }
        
        this.#receiveTransmissions.delete(JSON.stringify(transmission.id));

        this.console.log("Finished receiving " + JSON.stringify(transmission));
        this.console.log("Number of receive transmissions: " + this.#receiveTransmissions.size);
    }

    /**
     * Receive the chunk ack message
     */
    async #receiveAck(transmissionIdBytes, payload) {
        const transmission = this.#sendTransmissions.get(JSON.stringify(transmissionIdBytes));
        if (!transmission) {
            throw new Error("Send transmission " + transmissionIdBytes + " not found");
        }

        const chunkIndex = this.bytes2number(payload);

        if (chunkIndex != transmission.nextChunk - 1) {
            throw new Error("Invalid ack chunk: " + chunkIndex);
        }

        if (transmission.nextChunk == transmission.amountChunks) {
            this.#sendTransmissions.delete(JSON.stringify(transmissionIdBytes));

            this.console.log("Finished sending " + JSON.stringify(transmission));
            this.console.log("Number of send transmissions: " + this.#sendTransmissions.size);
            
            await this.onReceiveAck({
            	transmissionId: transmissionIdBytes
            });
        } else {
            await this.#sendNextChunk(transmission);
        }
    }

    /**
	 * Sends the "acknowledge successful transfer" message
	 */
    async #sendAckMessage(transmissionIdBytes, chunkIndex) {
		const payload = [].concat(
            Array.from(transmissionIdBytes),
            Array.from(this.number2bytes(chunkIndex, JMB_NUMBER_SIZE_FULLBYTES))
        );
        const checksum = Array.from(this.getChecksum(new Uint8Array(payload)));
        
        this.console.log("Send ack message" + chunkIndex);
        
        await this.#sendSysex(
			JMB_MANUFACTURER_ID,
            JMB_ACK_MESSAGE.concat(checksum, payload)
		);        
	}

    /**
	 * Sends an error message
	 */
    async error(message) {
		await this.sendString(
            "",
            message,
            JMB_ERROR_CHUNK_SIZE,
            JMB_TRANSMISSION_TYPE_ERROR
        );
	}

    /**
	 * Send a MIDI message via callback
	 */
    async #sendSysex(manufacturerId, data) {
		if (!Array.isArray(manufacturerId)) throw new Error("Cannot send manufacturer id " + manufacturerId);
		if (!Array.isArray(data)) throw new Error("Cannot send data " + data);
		
        await this.send(
            [0xf0].concat(
                manufacturerId, 
                data, 
                [0xf7]
            )
        );
	}

	/**
	 * Compare two Uint arrays (could be done more js like but works)
	 */
	#compareArrays(a, b) {
		if (a.length != b.length) {
			return false;
		}
		 
		for (let i = 0; i < a.length; ++i) {
			if (a[i] != b[i]) {
				return false;
			} 
		}
		
		return true;
	}

    /**
     * Cleans up all transmissions which ran out of time
     */
    #cleanupTransmissions() {
        this.#cleanupTransmissionsArray(this.#sendTransmissions);
        this.#cleanupTransmissionsArray(this.#receiveTransmissions);
    }

    /**
     * Clean up the passed transmissions array
     */
    #cleanupTransmissionsArray(transmissions) {
        const that = this;

        new Map(transmissions).forEach((transmission, key) => {
            if (!transmission.hasOwnProperty("time")) return;

            if (Date.now() - transmission.time > JMB_TIMEOUT_MILLIS) {
                that.console.log("Cleanup transmission " + key);
                // Timeout
                transmissions.delete(key);
            }
        });
    }


    // Checksum ###########################################################################################################


    /**
	 * Get checksum of bytes (only returns MIDI half-bytes)
	 */
    getChecksum(data) {
		if (!(data instanceof Uint8Array)) {
			throw new Error("Invalid input data, must be an Uint8Array");
		}
		
        const crc = this.#crc16(data);
        return this.number2bytes(crc, JMB_CHECKSUM_LENGTH_FULLBYTES);
	}

    /**
	 * CRC-16-CCITT Algorithm
	 * Taken from https://gist.github.com/oysstu/68072c44c02879a2abf94ef350d1c7c6 and ported to JS
	 */
    #crc16(data, poly = 0x6756) {
        let crc = 0xFFFF;
        
        for (const b of data) {
            let current = 0xFF & b;
            
            for (let x = 0; x < 8; ++x) {
                if ((crc & 0x0001) ^ (current & 0x0001)) {
					crc = (crc >> 1) ^ poly;
				} else {
					crc >>= 1;
				}                                       
                current >>= 1;
            }
        }
        
        crc = (~crc & 0xFFFF);
        crc = (crc << 8) | ((crc >> 8) & 0xFF);

        return crc & 0xFFFF;
    }


    // Conversions ##########################################################################################################


    /**
	 * String to bytearray conversion (only returns MIDI half-bytes)
	 */
    string2bytes(str) {
		let utf8Encode = new TextEncoder();
		const bytes = utf8Encode.encode(str);
        return this.packBytes(bytes);
	}

    /**
	 * Bytearray to string conversion
	 */ 
    bytes2string(data) {
		const bytes = this.unpackBytes(data);
		let utf8Decode = new TextDecoder();
		return utf8Decode.decode(new Uint8Array(bytes));
    }    

    /**
	 * Number to bytearray conversion (only returns MIDI half-bytes)
	 */
    number2bytes(num, numBytes) {	
		if (numBytes > 4) {
			throw new Error("JavaScript natively only supports up to 32bit integer arithmentic");
		}
			
		const arr = []

		for(let i = 0; i < numBytes; ++i) {
			const mask = 0xff << ((numBytes - i - 1) * 8);
			arr.push(
				(num & mask) >> ((numBytes - i - 1) * 8)
			);
		}

		return this.packBytes(new Uint8Array(arr));
	}

    /**
	 * Bytes to number conversion
	 */
    bytes2number(data) {
		const bytes = this.unpackBytes(data);
		const numBytes = bytes.length;
		
		let result = 0;
	    
	    for (let i = 0; i < numBytes; ++i) {			
	        result += bytes[i] << ((numBytes - i - 1) * 8);
	    }
	    
	    return result;
	}
    

    //#########################################################################################################################


    /**
	 * Packs full bytes into MIDI compatible half-bytes
	 */
    packBytes(data) {
        return this.#convertBitlength(data, 8, 7, true);
    }

    /**  
	 * Unpacks full bytes from MIDI compatible half-bytes
	 */ 
    unpackBytes(data) {
        return this.#convertBitlength(data, 7, 8, false);
    }
    

    /**
	 * Change bit length per byte
	 */
    #convertBitlength(data, bitlengthFrom, bitlengthTo, appendLeftovers) {
		if (!(data instanceof Uint8Array)) {
			throw new Error("Invalid input data, must be an Uint8Array");
		}
		
        let result = [];
        let buffer = [];

        function flush() {
            let newEntry = 0x00;
            
            while(buffer.length < bitlengthTo) {
                buffer.push(0);
            }

            for (let i = 0; i < buffer.length; ++i) {
                const e = buffer[i];
                if (e != 1) continue;

                const mask = (1 << (bitlengthTo - 1 - i));
                newEntry |= mask;
            }

            result.push(newEntry);
            buffer = [];
		}
		
        for (const b of data) {
            for (let i = 0; i < bitlengthFrom; ++i) {
                const mask = (1 << (bitlengthFrom - 1 - i));
                buffer.push(((b & mask) == mask) ? 1 : 0);

                if (buffer.length == bitlengthTo) {
                    flush();
                }
            }
        }

        if (appendLeftovers && buffer.length > 0) {
            flush();
        }

        return new Uint8Array(result);
    }
}