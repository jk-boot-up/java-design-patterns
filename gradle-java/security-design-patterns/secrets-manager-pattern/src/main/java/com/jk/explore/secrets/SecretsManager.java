package com.jk.explore.secrets;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The pattern: secrets live in one guarded store, never in code. Each service may read only the
 * secrets it is granted, every read is logged, and a secret can be rotated to a new version without
 * rebuilding anything.
 */
public final class SecretsManager {

    private final Map<String, List<String>> versions = new HashMap<>();
    private final Map<String, Set<String>> readers = new HashMap<>();
    private final List<String> audit = new ArrayList<>();

    public void store(String name, String value, Set<String> allowedServices) {
        versions.computeIfAbsent(name, n -> new ArrayList<>()).add(value);
        readers.put(name, allowedServices);
    }

    public String read(String service, String name) {
        boolean allowed = readers.getOrDefault(name, Set.of()).contains(service);
        audit.add(service + " read " + name + ": " + (allowed ? "granted" : "DENIED"));
        if (!allowed) {
            throw new SecurityException(service + " may not read " + name);
        }
        List<String> v = versions.get(name);
        return v.get(v.size() - 1);
    }

    /** Adds a new current version. Older versions stay in the history but are no longer handed out. */
    public int rotate(String name, String newValue) {
        versions.get(name).add(newValue);
        return versions.get(name).size();
    }

    public List<String> audit() {
        return audit;
    }
}
