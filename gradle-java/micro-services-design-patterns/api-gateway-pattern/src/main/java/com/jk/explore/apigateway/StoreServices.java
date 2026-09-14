package com.jk.explore.apigateway;

import java.util.List;

/**
 * The four services, reachable over a named network link.
 *
 * The same four services exist either way; what changes is how far away they
 * are. Two services in the same data centre answer each other in about ten
 * milliseconds. A phone on a train reaching those services over a mobile
 * connection takes about two hundred. Twenty times, per call, and a product page
 * needs four calls.
 *
 * <p>That ratio is the entire argument for a gateway, so it is a number in the
 * code rather than a claim in a comment.
 */
public final class StoreServices {

    /** Service to service, inside the data centre. */
    public static final long INTERNAL_LATENCY_MILLIS = 10;

    /** Phone to data centre, over a mobile connection. */
    public static final long MOBILE_LATENCY_MILLIS = 200;

    private final long latencyMillis;
    private final InventoryService inventoryService = new InventoryService();
    private final RemoteCall<String, Product> catalog;
    private final RemoteCall<String, Money> pricing;
    private final RemoteCall<String, Boolean> inventory;
    private final RemoteCall<String, List<String>> recommendations;

    private StoreServices(long latencyMillis, SimulatedClock clock, CallLog log) {
        this.latencyMillis = latencyMillis;
        this.catalog = new RemoteCall<>("Catalog", latencyMillis,
                new CatalogService()::product, clock, log);
        this.pricing = new RemoteCall<>("Pricing", latencyMillis,
                new PricingService()::price, clock, log);
        this.inventory = new RemoteCall<>("Inventory", latencyMillis,
                inventoryService::inStock, clock, log);
        this.recommendations = new RemoteCall<>("Recommendations", latencyMillis,
                new RecommendationsService()::alsoBought, clock, log);
    }

    /** The services as the gateway sees them: next door, and fast. */
    public static StoreServices onInternalNetwork(SimulatedClock clock, CallLog log) {
        return new StoreServices(INTERNAL_LATENCY_MILLIS, clock, log);
    }

    /** The services as a phone sees them: far away, and slow. */
    public static StoreServices onMobileNetwork(SimulatedClock clock, CallLog log) {
        return new StoreServices(MOBILE_LATENCY_MILLIS, clock, log);
    }

    public RemoteCall<String, Product> catalog() {
        return catalog;
    }

    public RemoteCall<String, Money> pricing() {
        return pricing;
    }

    public RemoteCall<String, Boolean> inventory() {
        return inventory;
    }

    public RemoteCall<String, List<String>> recommendations() {
        return recommendations;
    }

    /** How slow this link is, in simulated milliseconds per call. */
    public long latencyMillis() {
        return latencyMillis;
    }

    /** Lets the demo take a product out of stock. */
    public void setStock(String sku, int units) {
        inventoryService.setStock(sku, units);
    }
}
