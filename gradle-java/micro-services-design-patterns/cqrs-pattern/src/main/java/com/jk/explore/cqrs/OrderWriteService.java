package com.jk.explore.cqrs;

import java.util.ArrayList;
import java.util.List;

/**
 * The write side. Places orders, and publishes the fact that it did.
 *
 * Notice how little it does. It checks the stock ledger, stores a normalised order, and
 * publishes an event. It does not build a page, does not know what a product is called,
 * and does not know that an order history page exists. Every read model in the shop could
 * be deleted and this class would not need a line changed.
 */
public final class OrderWriteService {

    public static final long WRITE_MILLIS = 20;

    private final StockLedger stock;
    private final EventBus events;
    private final SimulatedClock clock;
    private final CallLog log;
    private final List<Order> orders = new ArrayList<>();
    private int nextId = 5001;

    public OrderWriteService(StockLedger stock, EventBus events, SimulatedClock clock,
                             CallLog log) {
        this.stock = stock;
        this.events = events;
        this.clock = clock;
        this.log = log;
    }

    /**
     * Places an order, or refuses it because the shelf cannot cover it.
     *
     * The stock check is against {@link StockLedger} and nothing else. It is worth
     * saying out loud: the read model has a stock number on it, it is right there, it is
     * faster to read, and using it here would be a bug that only shows up on the busiest
     * day of the year.
     */
    public Order place(String customerId, List<Order.Line> lines) {
        for (Order.Line line : lines) {
            stock.reserve(line.sku(), line.quantity());
        }

        long startedAt = clock.millis();
        clock.advance(WRITE_MILLIS);
        Order order = new Order("ord-" + nextId++, customerId, List.copyOf(lines),
                clock.millis());
        orders.add(order);
        log.record(startedAt, clock.millis(), "WriteSide", "PLACED",
                order.orderId() + " for " + order.total());

        events.publish(new ShopEvent.OrderPlaced(order));
        return order;
    }

    /** Every order ever placed, normalised. The truth, and awkward to read. */
    public List<Order> allOrders() {
        return List.copyOf(orders);
    }
}
