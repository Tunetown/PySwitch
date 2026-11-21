/**
 * Base class for cleint detectors
 */
class ClientDetector {
    
    /**
     * Checks if a client is listening.
     */
    async test(midiHandler, input, output, resolve) {
        throw new Error("Must be implemented in child classes");
    }
}