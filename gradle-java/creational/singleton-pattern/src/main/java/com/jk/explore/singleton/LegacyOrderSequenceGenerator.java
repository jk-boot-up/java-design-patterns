package com.jk.explore.singleton;

import java.io.Serializable;

/**
 * The "classic" singleton: a private constructor plus a lazily-created
 * static instance, the shape most tutorials teach first.
 *
 * <p>It is included here only to demonstrate what it does not protect
 * against. Reflection can call the private constructor directly, and
 * Java's default serialization does not consult any constructor at all, so
 * both routes can mint a second instance despite the private constructor.
 * See {@link OrderSequenceGenerator} for the fix.
 */
public final class LegacyOrderSequenceGenerator implements Serializable {

    private static LegacyOrderSequenceGenerator instance;

    private int counter;

    private LegacyOrderSequenceGenerator() {
    }

    public static LegacyOrderSequenceGenerator getInstance() {
        if (instance == null) {
            instance = new LegacyOrderSequenceGenerator();
        }
        return instance;
    }

    public String nextOrderNumber() {
        counter++;
        return String.format("ORD-%06d", counter);
    }
}
