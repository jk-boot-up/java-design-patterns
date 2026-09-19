package com.jk.explore.registry.pattern;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * <strong>A well-known object that other objects find things in.</strong>
 * {@code Registry.get(PaymentGateway.class)}. It is a global variable with
 * better manners, and it brings everything that implies. The map is concurrent
 * only because a static map shared by every thread has to be.
 */
public final class Registry {

    private static final Map<Class<?>, Object> ENTRIES = new ConcurrentHashMap<>();

    private Registry() {
    }

    public static <T> void register(Class<T> type, T instance) {
        ENTRIES.put(type, instance);
    }

    public static <T> T get(Class<T> type) {
        Object found = ENTRIES.get(type);
        if (found == null) {
            throw new IllegalStateException("nothing is registered for " + type.getSimpleName());
        }
        return type.cast(found);
    }

    public static void clear() {
        ENTRIES.clear();
    }

    /** "What is in the registry at this moment" is not answerable by reading any one file; this is the only way. */
    public static List<String> contents() {
        List<String> names = new ArrayList<>();
        ENTRIES.keySet().forEach(k -> names.add(k.getSimpleName()));
        names.sort(String::compareTo);
        return names;
    }
}
