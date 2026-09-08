package com.jk.explore.observer;

import java.util.Objects;
import java.util.function.Consumer;

/**
 * Releases the stock reservation once the goods have left, and puts stock back
 * if the order is cancelled.
 *
 * <p>Note what it does on {@code PAID} and {@code DELIVERED}: nothing at all,
 * silently. A listener is allowed to be interested in a subset of events, and
 * it says so by simply returning. It does not need permission from the order,
 * and the order does not need to know which statuses it cares about.
 */
public final class InventoryListener implements OrderListener {

    private final Consumer<String> sink;
    private int released;
    private int restocked;

    public InventoryListener(Consumer<String> sink) {
        this.sink = Objects.requireNonNull(sink, "sink");
    }

    @Override
    public String name() {
        return "inventory";
    }

    @Override
    public void onStatusChanged(OrderEvent event) {
        switch (event.to()) {
            case SHIPPED -> {
                released++;
                sink.accept("  [inventory] released the reservation for " + event.orderId());
            }
            case CANCELLED -> {
                restocked++;
                sink.accept("  [inventory] returned " + event.orderId() + " to available stock");
            }
            default -> {
                // Not our concern. Doing nothing here is the whole point: the
                // order never had to be told which statuses matter to stock.
            }
        }
    }

    public int released() {
        return released;
    }

    public int restocked() {
        return restocked;
    }
}
