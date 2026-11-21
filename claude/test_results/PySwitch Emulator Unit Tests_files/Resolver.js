/**
 * Used to resolve raw data values (assigns and const() calls are regarded)
 */
class Resolver {

    /**
     * Returns the raw value of the node
     */
    resolve(nodeOrValue) {
        if (typeof nodeOrValue == "object") {
            if (nodeOrValue.hasOwnProperty("value")) {
                return this.resolve(nodeOrValue.value);
            }

            if (nodeOrValue.hasOwnProperty("name") && nodeOrValue.name == "const") {
                return this.resolve(nodeOrValue.arguments[0]);
            }
        } 
          
        return nodeOrValue;        
    }
}