class ResolverTests {

    async testResolve() {
        const resolver = new Resolver();

        expect(resolver.resolve({
            name: "foo",
            value: 99
        })).toBe(99);

        expect(resolver.resolve({
            name: "foo",
            value: {
                name: "const",
                arguments: [
                    "bar"
                ]
            }
        })).toBe("bar");

        expect(resolver.resolve({
            name: "foo",
            value: {
                name: "const",
                arguments: [
                    { 
                        value: "bar"
                    }
                ]
            }
        })).toBe("bar");

        expect(resolver.resolve({
            name: "foo",
            value: {
                name: "const",
                arguments: [
                    { 
                        name: "const",
                        arguments: [
                            67
                        ]
                    }
                ]
            }
        })).toBe(67);

        expect(resolver.resolve({
            name: "foo",
            value: {
                name: "const",
                arguments: [
                    { 
                        name: "const",
                        arguments: [
                            {
                                value: 55
                            }
                        ]
                    }
                ]
            }
        })).toBe(55);
    }
}