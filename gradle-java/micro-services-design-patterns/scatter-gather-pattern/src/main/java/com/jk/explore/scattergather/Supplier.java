package com.jk.explore.scattergather;

/** Something that can be asked for a price. It may be slow, or it may fail. */
public interface Supplier {

    String name();

    Quote quote(String sku);

    /** A supplier that answers at once. */
    static Supplier fixed(String name, long pence) {
        return new Supplier() {
            public String name() {
                return name;
            }

            public Quote quote(String sku) {
                return new Quote(name, pence);
            }
        };
    }

    /** A supplier that does not answer until its gate is opened. */
    static Supplier held(String name, long pence, Gate gate) {
        return new Supplier() {
            public String name() {
                return name;
            }

            public Quote quote(String sku) {
                gate.await();
                return new Quote(name, pence);
            }
        };
    }

    static Supplier failing(String name) {
        return new Supplier() {
            public String name() {
                return name;
            }

            public Quote quote(String sku) {
                throw new IllegalStateException(name + " is down");
            }
        };
    }
}
