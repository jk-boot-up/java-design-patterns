package com.jk.explore.aggregate.infrastructure;

import java.util.HashMap;
import java.util.Map;
import java.util.function.UnaryOperator;

/**
 * Keeps whole aggregates, one per key, each with a version. A save is accepted only if nobody has saved
 * since the load, which is how an aggregate is the unit of consistency: it is read whole, changed whole and
 * saved whole, and two people changing the same one cannot both win.
 */
public class VersionedStore<T> {

    private final Map<String, T> values = new HashMap<>();
    private final Map<String, Integer> versions = new HashMap<>();
    private final UnaryOperator<T> copier;

    public VersionedStore(UnaryOperator<T> copier) {
        this.copier = copier;
    }

    public synchronized void insert(String key, T value) {
        values.put(key, copier.apply(value));
        versions.put(key, 1);
    }

    public synchronized Loaded<T> load(String key) {
        return new Loaded<>(copier.apply(values.get(key)), versions.get(key));
    }

    public synchronized void save(String key, Loaded<T> loaded) {
        if (versions.get(key) != loaded.version()) {
            throw new ConcurrentModification(key);
        }
        values.put(key, copier.apply(loaded.value()));
        versions.put(key, loaded.version() + 1);
    }
}
