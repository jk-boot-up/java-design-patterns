package com.jk.explore.cqrs;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Catalog. Knows what things are called, and tells the shop when a name changes. */
public final class CatalogService {

    public static final long LATENCY_MILLIS = 60;

    private final Map<String, String> names = new LinkedHashMap<>();
    private final EventBus events;
    private final RemoteCall<List<String>, Map<String, String>> namesFor;

    public CatalogService(EventBus events, SimulatedClock clock, CallLog log) {
        this.events = events;
        this.namesFor = new RemoteCall<>("Catalog", LATENCY_MILLIS, this::lookUp, clock, log);
    }

    public void add(String sku, String name) {
        names.put(sku, name);
    }

    /** Renames a product and says so, because other people are holding a copy. */
    public void rename(String sku, String newName) {
        names.put(sku, newName);
        events.publish(new ShopEvent.ProductRenamed(sku, newName));
    }

    public Map<String, String> namesFor(List<String> skus) {
        return namesFor.invoke(skus);
    }

    public void goDown(int count) {
        namesFor.failNext(count);
    }

    public int callsReceived() {
        return namesFor.invocations();
    }

    private Map<String, String> lookUp(List<String> skus) {
        Map<String, String> found = new LinkedHashMap<>();
        for (String sku : skus) {
            found.put(sku, names.getOrDefault(sku, "(unknown product)"));
        }
        return found;
    }
}
