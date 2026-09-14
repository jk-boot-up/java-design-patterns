package com.jk.explore.databaseperservice;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The Catalog service. Owns the product tables, and answers questions about products.
 *
 * It offers {@link #namesFor} as well as {@link #nameOf}, and that is not a
 * convenience — it is the difference between one call and twenty. When a page needs
 * fifty products, asking fifty times is the mistake this method exists to prevent.
 */
public final class CatalogService {

    public static final long LATENCY_MILLIS = 10;

    /** What a page shows when the catalogue has never heard of a sku. */
    public static final String UNKNOWN_PRODUCT = "(no longer in the catalogue)";

    private final CatalogDatabase database;
    private final SimulatedClock clock;
    private final CallLog log;
    private int callsReceived;

    public CatalogService(CatalogDatabase database, SimulatedClock clock, CallLog log) {
        this.database = database;
        this.clock = clock;
        this.log = log;
    }

    /** The name of one product. */
    public String nameOf(String sku) {
        return namesFor(List.of(sku)).get(sku);
    }

    /** The names of several products, in one call. */
    public Map<String, String> namesFor(List<String> skus) {
        callsReceived++;
        long startedAt = clock.millis();
        clock.advance(LATENCY_MILLIS);

        Map<String, String> names = new LinkedHashMap<>();
        for (String sku : skus) {
            String name = database.nameOf("Catalog", sku);
            names.put(sku, name == null ? UNKNOWN_PRODUCT : name);
        }
        log.record(startedAt, clock.millis(), "Catalog", "OK",
                names.size() + " name(s) in one call");
        return names;
    }

    public int callsReceived() {
        return callsReceived;
    }
}
