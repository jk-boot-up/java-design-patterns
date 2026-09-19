package com.jk.explore.producerconsumer.pattern;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.domain.Packing;

import java.util.Collections;
import java.util.List;
import java.util.ArrayList;

/**
 * The consumer: takes one order at a time from the queue and packs it, at
 * its own pace, on its own thread.
 *
 * <p>A poison-pill order — {@link #POISON} — is how a clean shutdown is
 * expressed: it is enqueued like any other order, so every order queued
 * before it is still drained and packed, and the packer stops only once it
 * sees the pill. Interrupting the thread instead stops it immediately,
 * mid-{@code take}, leaving whatever was still queued unpacked — the other
 * shutdown this project has to show.
 */
public final class Packer implements Runnable {

    public static final Order POISON = new Order("__POISON__", "");

    private final BoundedOrderQueue queue;
    private final Packing packing;
    private final List<Order> packedLog = Collections.synchronizedList(new ArrayList<>());

    public Packer(BoundedOrderQueue queue, Packing packing) {
        this.queue = queue;
        this.packing = packing;
    }

    @Override
    public void run() {
        while (true) {
            Order order;
            try {
                order = queue.take();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                // abrupt shutdown, caught between orders: whatever was still
                // queued is simply never taken, and so never packed.
                return;
            }
            if (order == POISON) {
                return;
            }
            packing.pack(order);
            if (Thread.currentThread().isInterrupted()) {
                // abrupt shutdown, caught mid-pack: the packing step noticed
                // the interrupt itself (for instance, a harness Gate that was
                // never opened) and returned without finishing. The order in
                // progress does not count as packed, and nothing queued
                // behind it is ever reached.
                return;
            }
            packedLog.add(order);
        }
    }

    public List<Order> packed() {
        return List.copyOf(packedLog);
    }
}
