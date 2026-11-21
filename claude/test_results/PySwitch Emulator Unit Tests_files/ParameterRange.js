/**
 * Parameter range
 */
class ParameterRange {

    #parameterMeta = null;

    constructor(parameterMeta) {
        this.#parameterMeta = parameterMeta;
    }

    async min() {        
        return this.#resolve(this.#parameterMeta.data.range.min);        
    }

    async max() {
        return this.#resolve(this.#parameterMeta.data.range.max);        
    }

    /**
     * Returns all possible values
     */
    async getValues() {
        const values = [];
        
        if (this.#parameterMeta.data.range.additionalValues) {
            for (const av of this.#parameterMeta.data.range.additionalValues) {
                values.push({
                    name: av.name,
                    value: av.value
                })    
            }
        }

        const min = await this.min();
        const max = await this.max();

        if (!this.#parameterMeta.data.range.additionalValues) {
            if (max - min > 100) {
                return null;
            }
        }
        
        for(let i = min; i <= max; ++i) {
            values.push({
                name: "" + i,
                value: i
            })
        }

        return values;
    }

    /**
     * Resolve tokens
     */
    async #resolve(value) {        
        return this.#parameterMeta.client.resolveValueToken(value);
    }
}