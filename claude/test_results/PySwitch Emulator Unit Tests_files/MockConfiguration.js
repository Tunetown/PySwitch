class MockConfiguration extends Configuration {

    #inputs_py = null;
    #display_py = null;

    constructor(inputs_py, display_py) {
        super(new MockController(), "Dummy");

        this.#inputs_py = inputs_py;
        this.#display_py = display_py;
    }

    /**
     * Some dummy code that just does not throw any errors.
     */
    async load() {
        return {
            inputs_py: this.#inputs_py,
            display_py: this.#display_py
        }
    }
}