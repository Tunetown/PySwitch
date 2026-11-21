/**
 * TOC entry for the browser popup
 */
class BrowserEntry {

    value = null;       // Value for selection
    text = null;        // Display text
    parent = null;      // Parent BrowserEntry
    children = [];      // Child BrowserEntry list
    data = null;        // Options (plus arbitrary application data if needed)

    browser = null;
    
    /**
     * {
     *      value:         Entry value
     *      text:          Entry text (default: use value). Cal also be a function(entry) => string
     *      parent:        Reference to parent entry
     *      onSelect:      Optional onSelect(entry) => void
     *      sortString:    Optional string to use for sorting (if not set, the text or value is used, in this order)
     *      childLayout:   Optional: Array of column definitions. If not specified, only one column with the listing link is generated. Entry format:
     *                     {
     *                        type:        "link", "typeIcon". If not set, get must be passed.
     *                        get:         callback(entry) => DOM Element, used if no (or an invalid) type is set
     *                     }
     * }
     */
    constructor(browser, data = {}) {
        this.browser = browser;
        this.data = data;

        this.value = data.value;
        this.text = data.text;
        this.parent = data.parent;

        // These must be accessed by their direct attributes! (could have been changed from outside)
        data.value = null;
        data.text = null;
        data.parent = null;

        // Default layout
        if (!this.data.childLayout) {
            this.data.childLayout = [
                {
                    type: "typeIcon"
                },
                {
                    type: "link"
                }
            ]
        }
    }

    /**
     * Returns a path inside the hierarchy, as an array of values (or texts if no value defined)
     */
    async getHierarchicalPath() {
        return (
                this.parent 
            ? 
                (await this.parent.getHierarchicalPath())
            : 
                []
        ).concat(
            [
                await this.getText()                
            ]
        );
    }

    /**
     * Resolves a path generated with getHierarchicalPath(). Returns the targeted entry if found, the nearest one, or this if not found.
     */
    async resolvePath(path) {
        // Ignore first entry as this is the lowest one (this one)
        let current = this;
        for (let i = 1; i < path.length; ++i) {
            const token = path[i];
            
            for (const child of current.children) {
                const text = await child.getText();
                if (text == token) {
                    current = child;
                    break;
                }
            }
        }

        return current;
    }

    /**
     * Returns a path inside the hierarchy, as an array of DOM elements.
     */
    async getHierarchicalPathHTML() {
        const that = this;

        return (
                this.parent 
            ? 
                (await this.parent.getHierarchicalPathHTML()).concat([
                    $('<span/>')
                    .text("/")
                ]) 
            : 
                []
        ).concat(
            [
                $('<span class="path-link"/>')
                .text(await this.getText())
                .on("click", async function() {
                    try {
                        await that.browser.browse(that);

                    } catch (e) {
                        that.browser.handle(e);
                    }
                })
            ]
        );
    }

    /**
     * Returns the sort string to be used to compare this entry to its siblings
     */
    async getSortString() {
        return this.data.sortString ? this.data.sortString : this.getText();
    }

    /**
     * Returns the text to show
     */
    async getText() {
        return (typeof this.text == "function") ? this.text(this) : (this.text ? this.text : this.value);
    }

    /**
     * Creates the listing elements
     */
    async getElement(layout) {
        const that = this;

        const tr = $('<tr/>');

        const iconOpen = this.browser.options.iconOpen ? this.browser.options.iconOpen : 'fa-play';

        for(const col of layout) {
            const td = $('<td/>');
            tr.append(td);                

            switch (col.type) {
                case "link":
                    td.append(
                        // Listing entry link
                        $('<span class="listing-link" />')
                        .text(await this.getText())
                        .on('click', async function() {
                            try {
                                await that.browser.browse(that);

                            } catch (e) {
                                that.browser.handle(e);
                            }
                        })
                    )
                    break;
                
                case "typeIcon":
                    td.append(
                        // Listing entry link
                        $('<span class="fa"/>')
                        .addClass(this.isCallable() ? iconOpen : "fa-folder")
                    )
                    break;

                default:
                    td.append(
                        await col.get(this)
                    );
                    break;
            }
        }

        return tr;
    }

    /**
     * Is the entry callable?
     */
    isCallable() {
        return !!this.data.onSelect;
    }

    /**
     * Calls the entry
     */
    async call() {        
        await this.data.onSelect(this);
    }
}