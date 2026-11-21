/**
 * Generates the icons for actions in the parser frontend.
 */
class ParserFrontendIcons {
 
    #pageColors = null;
    #nextPageColorId = 0;
    #parser = null;

    constructor(parser) {
        this.#parser = parser;
        this.#pageColors = new Map();
    }

    /**
     * Returns icon DOM for the passed action proxy
     */
    async get(actionCallProxy, actionDefinition) {
        const icons = [];
        
        // Action using LEDs?        
        if (this.#usesLeds(actionCallProxy, actionDefinition)) {
            icons.push(
                $('<span data-toggle="tooltip" title="This action uses the switch LEDs" />')
                .addClass('fas fa-lightbulb action-icon icon-uses-leds')
            )
        }

        // Display assignment
        const display = actionCallProxy.argument('display');
        if (display && (display != 'None')) {
            icons.push(
                $('<span data-toggle="tooltip" title="This action is assigned to display ' + display + '" />')
                .addClass('fas fa-tv action-icon icon-has-display')
            )
        }

        // Page icon if involved in paging, if not: enable callback
        const page = actionCallProxy.page()
        const pager = actionCallProxy.pager()
        
        const ec = actionCallProxy.argument('enable_callback');
        if (page) {
            const el = $('<span class="action-icon icon-page" data-toggle="tooltip" title="This action is part of pager \"' + pager + '\", page ' + page + '" />')
                
            const color = await this.getPageColor(pager, page);
            
            if (color) {
                el.css('background-color', "rgb" + color);
            } else {
                const colorId = await this.#getPageColorId(pager, page);
                el.addClass('icon-page-' + colorId)
            }

            icons.push(el);

        } else if (ec && (ec != 'None')) {
            icons.push(
                $('<span data-toggle="tooltip" title="This action has an Enable Callback not involved in a PagerAction" />')
                .addClass('fas fa-chevron-circle-right action-icon icon-enable-callback')
            )
        }

        // Deferred definitions
        if (actionCallProxy.assign) {
            icons.push(
                $('<span data-toggle="tooltip" title="This action is defined globally in an Assign statement" />')
                .addClass('fas fa-arrow-right action-icon icon-assign')
            )
        }

        return $('<span class="action-icons" />').append(icons)
    }

    /**
     * Returns color for a page, if any
     */
    async getPageColor(pager, page) {
        const action = await this.#parser.getPagerAction(pager);
        if (!action) return null;

        const pages = action.argument("pages");
        if (!pages) return null;

        for (const pageProxy of pages) {
            if (pageProxy.id == page && pageProxy.color) {                
                return this.#parser.resolveColor(pageProxy.color);
            }
        }
        return null;
    }
    
    /**
     * Returns a numeric color ID
     */
    async #getPageColorId(pager, page) {
        if (this.#pageColors.has(pager + page)) return this.#pageColors.get(pager + page);

        this.#pageColors.set(pager + page, this.#nextPageColorId++);

        if (this.#nextPageColorId >= 5) {
            this.#nextPageColorId = 0;
        }

        return this.#pageColors.get(pager + page);
    }

    /**
     * Does the action use LEDs?
     */
    #usesLeds(actionCallProxy, actionDefinition) {
        const useLedsVal = actionCallProxy.argument('use_leds');
        if (useLedsVal) {
            // Argument exists
            return useLedsVal == 'True';
        }
        
        if (!actionDefinition) {
            // No definition: No icon
            return false;
        }

        // Use default
        return this.#getParameterDefault(actionDefinition, 'use_leds') == 'True';
    }

    /**
     * Get the default value
     */
    #getParameterDefault(actionDefinition, name) {        
        for (const param of actionDefinition.parameters) {
            if (param.name == name) return param.meta.getDefaultValue();
        }
    }
}