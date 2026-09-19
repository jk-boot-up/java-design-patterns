package com.jk.explore.identitymap.pattern;

import java.util.HashMap;
import java.util.Map;

/** <strong>A map from id to the one loaded object.</strong> Scoped to a session. */
public class IdentityMap<T> {

    private final Map<Integer, T> loaded = new HashMap<>();

    public T get(int id) {
        return loaded.get(id);
    }

    public void put(int id, T object) {
        loaded.put(id, object);
    }

    public int size() {
        return loaded.size();
    }
}
