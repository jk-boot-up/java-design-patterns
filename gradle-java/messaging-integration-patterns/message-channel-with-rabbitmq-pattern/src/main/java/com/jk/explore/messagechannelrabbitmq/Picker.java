package com.jk.explore.messagechannelrabbitmq;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

/**
 * One picker in the warehouse, working at its own pace.
 *
 * <p>Two of these share one channel in the fourth act: one slow, one fast. The slow one
 * stands for a picker whose shelves are at the far end of the building. How long each order
 * takes is part of the picker, not the channel, so the channel never knows which is which.
 */
public class Picker {

    private final Duration perOrder;
    // The broker hands messages over on its own thread, so the list is guarded.
    private final List<String> picked = new ArrayList<>();

    public Picker(Duration perOrder) {
        this.perOrder = perOrder;
    }

    public static Picker slow() {
        return new Picker(Duration.ofMillis(200));
    }

    public static Picker fast() {
        return new Picker(Duration.ZERO);
    }

    /** Walks to the shelf, which takes this picker's time, and records the order as picked. */
    public void pick(PickOrder order) {
        walkToTheShelf();
        synchronized (picked) {
            picked.add(order.orderId());
        }
    }

    public int count() {
        synchronized (picked) {
            return picked.size();
        }
    }

    private void walkToTheShelf() {
        if (perOrder.isZero()) {
            return;
        }
        try {
            Thread.sleep(perOrder.toMillis());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
