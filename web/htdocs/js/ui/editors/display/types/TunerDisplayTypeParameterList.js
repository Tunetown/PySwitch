class TunerDisplayTypeParameterList extends DisplayParameterList {
    
    #type = null; // Type handler

    constructor(type) {
        super(type.handler);
        this.#type = type;
    }
    /**
     * Sets up parameters on the passed ParameterList instance, according to the type of display element.
     */
    async setupTypeParameters() {
        await this.setupPositionParameters();
        await this.setupSizeParameters();

        await this.#setupParameters();

        // await this.#type.layout.setupParameters(this);
    }

    /**
     * Updates the parameters on the passed ParameterList instance according to the node.
     */
    updateTypeParameters() {
        // Bounds
        const bounds = this.handler.getModelBounds();
        this.setParameter('x', bounds.x);
        this.setParameter('y', bounds.y);
        this.setParameter('width', bounds.width);
        this.setParameter('height', bounds.height);
    }

    async #setupParameters() {
        const that = this;

        // General
        const mappingOptions = await (new MappingOptions()).generate(this.handler.editor.getConfig().parser, true);

        await this.createInput({
            type: "select",
            name: "mapping_note",
            comment: "Mapping which delivers the note",
            displayName: "Note Mapping",
            value: this.handler.getParameter("mapping_note", "None"),
            options: mappingOptions,
            onChange: async function(value) {
                that.handler.setParameter('mapping_note', value);
            }
        });

        let mdev = this.handler.getParameter("mapping_deviance", "None");
        if (mdev != "None") {
            mdev = mdev.name + "()";  // NOTE: This ignores mapping parameters, but those are never used for tuner mappings, so this is tolerated for now. TODO
        }

        await this.createInput({
            type: "select",
            name: "mapping_deviance",
            comment: "Mapping which delivers the deviance from the in tune note",
            displayName: "Deviance Mapping",
            value: mdev,
            options: mappingOptions,
            onChange: async function(value) {
                that.handler.setParameter('mapping_deviance', value);
            }
        });


        // Needle params
        await this.createInput({
            type: "number",
            name: "deviance_height",
            comment: "Height of the deviance needle",
            displayName: "Needle Height",
            value: this.handler.getParameter("deviance_height", 40),
            onChange: async function(value) {
                that.handler.setParameter('deviance_height', value);
            }
        });

        await this.createInput({
            type: "number",
            name: "deviance_width",
            comment: "Width of the deviance needle",
            displayName: "Needle Width",
            value: this.handler.getParameter("deviance_width", 5),
            onChange: async function(value) {
                that.handler.setParameter('deviance_width', value);
            }
        });

        await this.createInput({
            type: "number",
            name: "deviance_zoom",
            comment: "Scaling of deviance values. Set higher to make the tuner more sensitive. 2.4 is a good starting point.",
            displayName: "Sensitivity",
            value: this.handler.getParameter("deviance_zoom", 2.4),
            onChange: async function(value) {
                that.handler.setParameter('deviance_zoom', value);
            }
        });

        await this.createInput({
            type: "color",
            name: "color_in_tune",
            comment: "Color when in tune",
            displayName: "Color (in tune)",
            value: this.handler.getParameter("color_in_tune", "Colors.LIGHT_GREEN"),
            onChange: async function(value) {
                that.handler.setParameter('color_in_tune', value);
            }
        });

        await this.createInput({
            type: "color",
            name: "color_out_of_tune",
            comment: "Color when out of tune",
            displayName: "Color (out of tune)",
            value: this.handler.getParameter("color_out_of_tune", "Colors.ORANGE"),
            onChange: async function(value) {
                that.handler.setParameter('color_out_of_tune', value);
            }
        });

        await this.createInput({
            type: "color",
            name: "color_neutral",
            comment: "Color for the marker in the middle",
            displayName: "Marker Color",
            value: this.handler.getParameter("color_neutral", "Colors.WHITE"),
            onChange: async function(value) {
                that.handler.setParameter('color_neutral', value);
            }
        });

        await this.createInput({
            type: "text",
            name: "calibration_high",
            comment: "Threshold value above which the note is out of tune",
            displayName: "Calibration (high)",
            value: this.handler.getParameter("calibration_high", "8192 + 350"),
            onChange: async function(value) {
                that.handler.setParameter('calibration_high', value);
            }
        });

        await this.createInput({
            type: "text",
            name: "calibration_low",
            comment: "Threshold value below which the note is out of tune",
            displayName: "Calibration (low)",
            value: this.handler.getParameter("calibration_low", "8192 - 350"),
            onChange: async function(value) {
                that.handler.setParameter('calibration_low', value);
            }
        });

        // Note display params
        function getFontSize(item) {
            return parseInt(item.replace(/[^0-9]/g, ''));
        }
        const layout = this.handler.getParameter("layout", {});
        const font = layout?.arguments ? ('"'+Tools.stripQuotes(Tools.getArgument(layout, 'font')?.value)+'"') : null;
        const fontOptions = (await this.handler.editor.getConfig().parser.getAvailableFonts())
            .map((font) => {
                return {
                    value: '"' + font + '"',
                    text: font.replace('/fonts/', '') + " (" + getFontSize(font) + "px)"
                }
            });
        await this.createInput({
            type: "select",
            name: "font",
            displayName: "Note Name: Font",
            value: font,
            options: fontOptions,
            onChange: async function(value) {
                that.handler.setParameter('layout', { 
                    arguments: [
                        {
                            name: "font",
                            value: Tools.autoQuote(value)
                        }
                    ]
                });
            }
        });

        await this.createNumericInput({
            name: "scale",
            comment: "Note Name: Scale",
            displayName: "Scale by",
            value: this.handler.getParameter('scale', 1),
            range: {
                min: 1
            },
            onChange: async function(value) {
                that.handler.setParameter('scale', value, 1);
            }
        });
    }
}