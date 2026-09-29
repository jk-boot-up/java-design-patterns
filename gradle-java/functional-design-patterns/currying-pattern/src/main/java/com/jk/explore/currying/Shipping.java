package com.jk.explore.currying;

import java.util.function.BiFunction;
import java.util.function.Function;

/**
 * The shipping price, first as an ordinary three-argument method, then curried:
 * a chain of one-argument functions, so the first arguments can be fixed early.
 */
public final class Shipping {

    /** The ordinary way: everything at once. */
    public static double price(Zone zone, Service service, double kg) {
        return Math.round((zone.base + zone.perKg * kg) * service.multiplier * 100) / 100.0;
    }

    /** Curried: give a zone, get back a function that wants a service, which gives back one that wants a weight. */
    public static final Function<Zone, Function<Service, Function<Double, Double>>> CURRIED =
            zone -> service -> kg -> price(zone, service, kg);

    /** Turns any two-argument function into a curried one. It fixes the FIRST argument first. */
    public static <A, B, R> Function<A, Function<B, R>> curry(BiFunction<A, B, R> f) {
        return a -> b -> f.apply(a, b);
    }

    private Shipping() {
    }
}
