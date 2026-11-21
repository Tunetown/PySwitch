/**
 * Base class for data providers which should be used with BrowserPopup
 */
class BrowserProvider {
    
    /**
     * Must return a hierarchical TOC
     */
    async getToc(browser) {
        throw new Error("Must be implemented in child classes");
    }    
}