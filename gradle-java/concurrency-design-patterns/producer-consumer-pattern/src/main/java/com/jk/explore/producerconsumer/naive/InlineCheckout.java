package com.jk.explore.producerconsumer.naive;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.domain.Packing;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The first naive version: the checkout thread packs the order
 * itself.</strong>
 *
 * <p>Correct, and simple, and the shopper pays for it directly: every
 * checkout call does not return until the packing step it does not care
 * about has finished. One slow pack blocks every checkout behind it,
 * because there is only one thread and packing is what it spends its time
 * on.
 */
public final class InlineCheckout {

    private final Packing packing;
    private final List<Order> packed = new ArrayList<>();

    public InlineCheckout(Packing packing) {
        this.packing = packing;
    }

    /** Returns how long this call took, in nanoseconds — all of it spent packing. */
    public long checkout(Order order) {
        long start = System.nanoTime();
        packing.pack(order);
        packed.add(order);
        return System.nanoTime() - start;
    }

    public List<Order> packed() {
        return List.copyOf(packed);
    }
}
