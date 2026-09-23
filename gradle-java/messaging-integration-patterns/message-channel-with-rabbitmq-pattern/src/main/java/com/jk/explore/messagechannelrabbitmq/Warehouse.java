package com.jk.explore.messagechannelrabbitmq;

import java.util.ArrayList;
import java.util.List;

/**
 * The warehouse system: the one that actually picks an order off a shelf.
 *
 * <p>It is a separate system from the shop, and it is not always running. That single fact is
 * the reason the shop needs a channel rather than a phone call.
 */
public class Warehouse {

    // A broker hands messages over on its own thread, so the list is guarded.
    private final List<String> picked = new ArrayList<>();
    private volatile boolean running = true;

    public void goDown() {
        running = false;
    }

    public void comeBack() {
        running = true;
    }

    /** Picks an order, or refuses outright if the warehouse is not running. */
    public void pick(PickOrder order) {
        if (!running) {
            throw new IllegalStateException("the warehouse system is not answering");
        }
        synchronized (picked) {
            picked.add(order.orderId());
        }
    }

    public List<String> picked() {
        synchronized (picked) {
            return List.copyOf(picked);
        }
    }
}
