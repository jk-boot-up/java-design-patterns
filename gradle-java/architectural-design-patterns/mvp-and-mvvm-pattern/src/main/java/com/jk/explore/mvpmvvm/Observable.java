package com.jk.explore.mvpmvvm;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/** A value that tells whoever is bound to it when it changes. */
public class Observable<T> {

    private T value;
    private final List<Consumer<T>> listeners = new ArrayList<>();

    public Observable(T initial) {
        this.value = initial;
    }

    public T get() {
        return value;
    }

    public void set(T newValue) {
        if (!newValue.equals(value)) {
            value = newValue;
            listeners.forEach(l -> l.accept(newValue));
        }
    }

    /** Calls the listener now with the current value, and again at every change. */
    public void bind(Consumer<T> listener) {
        listeners.add(listener);
        listener.accept(value);
    }
}
