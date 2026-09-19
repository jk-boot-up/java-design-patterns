package com.jk.explore.lazyload.pattern;

import java.util.function.Supplier;

/** <strong>Variant three: value holder.</strong> The caller knows it is holding a promise, and asks for the value. */
public class ValueHolder<T> {

    private final Supplier<T> loader;
    private T value;
    private boolean loaded;

    public ValueHolder(Supplier<T> loader) {
        this.loader = loader;
    }

    public T value() {
        if (!loaded) {
            value = loader.get();
            loaded = true;
        }
        return value;
    }
}
