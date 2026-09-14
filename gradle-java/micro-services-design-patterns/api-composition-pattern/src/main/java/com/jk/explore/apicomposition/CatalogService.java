package com.jk.explore.apicomposition;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Catalog. Answers with the names of several skus in one call.
 *
 * The batch call is not a detail. A composer that asks for one name at a time turns a
 * two-line order into two calls and a fifty-line order into fifty, and then no amount
 * of running them in parallel will save it.
 */
public final class CatalogService {

    public static final long LATENCY_MILLIS = 60;

    /** The name to print for a sku when Catalog did not answer at all. */
    public static final String NAME_UNAVAILABLE = "(name unavailable)";

    private static final Map<String, String> NAMES = Map.of(
            "SKU-KETTLE", "Stainless Steel Kettle",
            "SKU-MUG", "Blue Stoneware Mug");

    private final RemoteCall<List<String>, Map<String, String>> namesFor;

    public CatalogService(SimulatedClock clock, CallLog log) {
        this.namesFor = new RemoteCall<>("Catalog", LATENCY_MILLIS,
                skus -> lookUp(skus), clock, log);
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

    private static Map<String, String> lookUp(List<String> skus) {
        Map<String, String> found = new LinkedHashMap<>();
        for (String sku : skus) {
            found.put(sku, NAMES.getOrDefault(sku, NAME_UNAVAILABLE));
        }
        return found;
    }
}
