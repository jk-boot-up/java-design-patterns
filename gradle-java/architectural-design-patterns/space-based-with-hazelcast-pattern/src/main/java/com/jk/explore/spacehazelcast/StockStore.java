package com.jk.explore.spacehazelcast;

import com.hazelcast.map.MapStore;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

/**
 * Hazelcast's bridge to the database. With write-behind, Hazelcast calls this later, in the
 * background, and only with the latest value of each key.
 */
public final class StockStore implements MapStore<String, Integer> {

    static SlowDatabase database;

    @Override
    public void store(String key, Integer value) {
        database.store(value);
    }

    @Override
    public void storeAll(Map<String, Integer> map) {
        map.values().forEach(database::store);
    }

    @Override
    public void delete(String key) {
    }

    @Override
    public void deleteAll(Collection<String> keys) {
    }

    @Override
    public Integer load(String key) {
        return null;
    }

    @Override
    public Map<String, Integer> loadAll(Collection<String> keys) {
        return new HashMap<>();
    }

    @Override
    public Iterable<String> loadAllKeys() {
        return null;
    }
}
