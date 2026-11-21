class Tools {

    /**
     * Fetch text from an url, throwing if the response is not OK.
     */
    static async fetch(url) {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error("Error fetching " + decodeURI(url));
        }
        return resp.text();
    }

    /**
     * Reads one File
     */
    static async loadFile(file) {
		return new Promise((resolve, reject) => {
    		var reader = new FileReader();

    	    reader.onload = function(evt) {
    	        try {
    	    		resolve(evt.target.result);

    	        } catch (e) {
    	        	reject(e);
    	        }    	        
    	    }

    	    reader.onerror = function(evt) {
    	    	reject('Error reading ' + file.name);
    	    }

    	    reader.readAsText(file); 
		});
	}

    /**
     * https://stackoverflow.com/questions/105034/how-do-i-create-a-guid-uuid
     */
    static uuid() {
        return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
            (+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16)
        );
    }

    /**
	 * Shallow compare two arrays (i know, could be done more js-like but works)
	 */
	static compareArrays(a, b) {
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
     * Returns an array with [r, g, b] 8 bit values from a hex color string
     */
    static hexToRgb(color) {
        if (!color.startsWith("#")) return color;
        
        const r = parseInt(color.substr(1,2), 16)
        const g = parseInt(color.substr(3,2), 16)
        const b = parseInt(color.substr(5,2), 16)
        
        return [r, g, b];
    }

    /**
     * Convert a RGB color string to hex
     */
    static rgbToHex(rgb) {
        function componentToHex(c) {
            var hex = c.toString(16);
            return hex.length == 1 ? "0" + hex : hex;
        }
            
        const comps = rgb.replace("(", "").replace(")", "").replace("rgba", "").replace("rgb", "").split(",");
        
        const r = parseInt(comps[0]);
        const g = parseInt(comps[1]);
        const b = parseInt(comps[2]);

        return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
    }

    /**
     * Remove all existing quotes and add new ones.
     */
    static autoQuote(str) {
        return "'" + Tools.stripQuotes(str) + "'";
    }

    /**
     * Removes all kinds of quotes
     */
    static stripQuotes(str) {
        return str.replaceAll('"', "").replaceAll("'", "");
    }

    /**
     * Returns the passed element with the passed comment on hover
     */
    static withComment(el, comment, placement = "top-end") {
        if (comment) {
            setTimeout(function() {
                tippy(el[0], {
                    content: comment,
                    theme: "pyswitchtooltip",
                    placement: placement,
                    arrow: false,
                    duration: 0,
                    delay: [600, 0]
                });
            }, 600)
        }

        return el;
    }

    /**
     * Converts a list of ord numbers to a string
     */
    static data2string(data) {
        let ret = "";
        for (const c of data) {
            ret += String.fromCharCode(c);
        }
        return ret;
    }

    /**
     * Helper to get an argument from a raw data node, like coming from the python parser.
     */
    static getArgument(node, argName, defaultValue = null) {
        for (const arg of node.arguments) {
            if (arg.name != argName) continue;

            return arg;
        }
        return defaultValue;
    }

    /**
     * Console output of DOM structures
     *
    static debugDOM(el, callback = null, level = 0, childIndex = 0) {
        const ret = {
            element: el,
            level: level,
            index: childIndex,
            children: []
        }

        if (callback) {
            callback(el, ret);
        }

        let cnt = 0;
        el.children().each(function() {
            ret.children.push(
                Tools.debugDOM(
                    $(this), 
                    callback, 
                    level + 1, 
                    cnt++
                )
            );
        });

        return ret;
    }*/
}