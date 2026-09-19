package com.jk.explore.pipesfilters;

import java.util.Optional;

/** One step: takes an item, and gives back a changed one, or nothing if the item should go no further. */
public interface Filter<I, O> {

    String name();

    /** @param rejects where this step records why it dropped an item */
    Optional<O> apply(I item, java.util.List<String> rejects);

    static <I, O> Filter<I, O> of(String name, java.util.function.Function<I, O> function) {
        return new Filter<>() {
            public String name() {
                return name;
            }

            public Optional<O> apply(I item, java.util.List<String> rejects) {
                return Optional.of(function.apply(item));
            }
        };
    }
}
