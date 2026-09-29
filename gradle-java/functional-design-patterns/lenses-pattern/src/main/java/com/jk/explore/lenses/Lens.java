package com.jk.explore.lenses;

import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.UnaryOperator;

/**
 * The pattern: a pair of functions that focus on one part of an immutable whole.
 * {@code get} reads the part; {@code set} returns a new whole with the part replaced.
 */
public record Lens<S, A>(Function<S, A> get, BiFunction<S, A, S> set) {

    /** A new whole with the part changed by a function. */
    public S modify(S whole, UnaryOperator<A> change) {
        return set.apply(whole, change.apply(get.apply(whole)));
    }

    /** Focus further in: this lens, then the next one. */
    public <B> Lens<S, B> andThen(Lens<A, B> inner) {
        return new Lens<>(
                whole -> inner.get().apply(get.apply(whole)),
                (whole, value) -> set.apply(whole, inner.set().apply(get.apply(whole), value)));
    }
}
