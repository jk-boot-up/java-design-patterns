package com.jk.explore.optimisticlock;

/** A row as it was read, and the version it had at that moment. */
public record Versioned<T>(T value, int version) {

    public Versioned<T> with(T changed) {
        return new Versioned<>(changed, version);
    }
}
