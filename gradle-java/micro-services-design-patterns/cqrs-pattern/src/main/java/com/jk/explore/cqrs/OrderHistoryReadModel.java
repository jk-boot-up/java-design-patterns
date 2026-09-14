package com.jk.explore.cqrs;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The read model: the order history page, kept ready in advance.
 *
 * Two halves, and it is worth reading them separately.
 *
 * <p>The {@code on...} methods are the write half. They run when an event arrives, which
 * is to say when somebody places an order or renames a product — thousands of times less
 * often than the page is looked at. All the expensive work lives here, including the one
 * call to Catalog needed to turn skus into names. CQRS does not make the work disappear;
 * it moves the work from the read, which happens constantly, to the write, which does not.
 *
 * <p>{@link #historyFor} is the read half, and there is almost nothing in it: one lookup
 * in a map, no join, no composition, no other service involved. That is why it costs five
 * milliseconds instead of ninety, and why it keeps working when Catalog is down.
 *
 * <p>{@link #stockOnDisplay} deserves its own warning, which is in
 * {@link StockLedger}: show that number, never sell against it.
 */
public final class OrderHistoryReadModel {

    public static final long LOOKUP_MILLIS = 5;

    private final CatalogService catalog;
    private final SimulatedClock clock;
    private final CallLog log;
    private final Map<String, List<OrderHistoryRow>> byCustomer = new LinkedHashMap<>();
    private final Map<String, Integer> stock = new LinkedHashMap<>();
    private int eventsApplied;

    public OrderHistoryReadModel(CatalogService catalog, SimulatedClock clock, CallLog log) {
        this.catalog = catalog;
        this.clock = clock;
        this.log = log;
    }

    /** Subscribes this read model to the bus. One line, and it is the whole wiring. */
    public void listenTo(EventBus events) {
        events.subscribe(this::apply);
    }

    /**
     * Applies one event.
     *
     * A read model believes what it is told. There is no validation here and no refusing:
     * the order has already been placed, so the only question is what the page should now
     * look like.
     */
    public void apply(ShopEvent event) {
        eventsApplied++;
        switch (event) {
            case ShopEvent.OrderPlaced placed -> project(placed.order());
            case ShopEvent.ProductRenamed renamed -> rename(renamed.sku(), renamed.newName());
            case ShopEvent.StockChanged changed ->
                    stock.put(changed.sku(), changed.nowAvailable());
        }
    }

    /** The page. One lookup, and nobody else is called. */
    public List<OrderHistoryRow> historyFor(String customerId) {
        long startedAt = clock.millis();
        clock.advance(LOOKUP_MILLIS);
        List<OrderHistoryRow> rows = byCustomer.getOrDefault(customerId, List.of());
        log.record(startedAt, clock.millis(), "ReadModel", "SERVED",
                rows.size() + " row(s), 0 other services called");
        return List.copyOf(rows);
    }

    /**
     * A stock number for display only.
     *
     * It is behind by however long the last event took to arrive. Fine on a product page,
     * a bug in a checkout.
     */
    public int stockOnDisplay(String sku) {
        return stock.getOrDefault(sku, 0);
    }

    /**
     * Throws the read model away and builds it again from the events.
     *
     * Every read model needs this method, and the reason is the honest cost of the
     * pattern: the read model is a second store, it will at some point be wrong, and the
     * only comfortable answer to "how do we fix it" is that it can be discarded and
     * rebuilt from facts that are held somewhere else. A read model that cannot be
     * rebuilt is not a projection, it is a second copy of the truth.
     */
    public void rebuildFrom(List<ShopEvent> history) {
        byCustomer.clear();
        stock.clear();
        eventsApplied = 0;
        log.note("ReadModel", "REBUILDING", history.size() + " event(s) replayed");
        history.forEach(this::apply);
    }

    public int eventsApplied() {
        return eventsApplied;
    }

    private void project(Order order) {
        // The one expensive call in this class, made once per order rather than once per
        // page view. A shop sells an order a second and shows the page a thousand times.
        Map<String, String> names = catalog.namesFor(order.skus());

        List<OrderHistoryRow> rows =
                byCustomer.computeIfAbsent(order.customerId(), key -> new ArrayList<>());
        for (Order.Line line : order.lines()) {
            rows.add(new OrderHistoryRow(order.orderId(), line.sku(),
                    names.get(line.sku()), line.quantity(), line.lineTotal(),
                    order.placedAtMillis()));
        }
        log.note("ReadModel", "PROJECTED", order.orderId() + " into "
                + order.lines().size() + " ready-made row(s)");
    }

    private void rename(String sku, String newName) {
        int touched = 0;
        for (List<OrderHistoryRow> rows : byCustomer.values()) {
            for (int i = 0; i < rows.size(); i++) {
                if (rows.get(i).sku().equals(sku)) {
                    rows.set(i, rows.get(i).renamedTo(newName));
                    touched++;
                }
            }
        }
        log.note("ReadModel", "RENAMED", touched + " row(s) now say " + newName);
    }
}
