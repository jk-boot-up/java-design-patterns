package com.jk.explore.observer;

import java.util.Objects;

/**
 * The trap: an order service that calls each interested party by name.
 *
 * <p>This is the version almost everyone writes first, and for one order and
 * two reactions it is genuinely better than the pattern -- shorter, and you can
 * read {@link #markShipped} and see exactly what happens. Keep it while that
 * stays true.
 *
 * <p>What it costs once it stops being true:
 *
 * <ul>
 *   <li><b>A fifth reaction edits this file.</b> The fraud team's new
 *       post-shipping check has nothing to do with inventory or email, but it
 *       lands in the same method, and everything that depended on that method
 *       is re-tested.
 *   <li><b>It cannot be tested without all four.</b> There is no constructor
 *       that leaves one out, so a test of the shipping transition drags in the
 *       email client whether it wants it or not.
 *   <li><b>One failure takes the rest down.</b> There is no {@code try} in the
 *       method below. If the email client throws -- and email clients throw,
 *       they talk to the network -- the warehouse feed is never written, the
 *       order has already been marked shipped, and nothing retries.
 * </ul>
 *
 * <p>That third one is the bug worth remembering. It is not a design smell; it
 * is an outage, and it looks completely reasonable in review.
 */
public final class NaiveOrderService {

    private final InventoryListener inventory;
    private final EmailListener email;
    private final AnalyticsListener analytics;
    private final WarehouseFeedListener warehouseFeed;

    public NaiveOrderService(InventoryListener inventory,
                             EmailListener email,
                             AnalyticsListener analytics,
                             WarehouseFeedListener warehouseFeed) {
        this.inventory = Objects.requireNonNull(inventory, "inventory");
        this.email = Objects.requireNonNull(email, "email");
        this.analytics = Objects.requireNonNull(analytics, "analytics");
        this.warehouseFeed = Objects.requireNonNull(warehouseFeed, "warehouseFeed");
    }

    /**
     * Mark an order shipped and tell the four systems that care.
     *
     * <p>Four hard-wired calls, in a hard-wired order, with no isolation
     * between them.
     */
    public void markShipped(String orderId, OrderStatus from) {
        OrderEvent event = new OrderEvent(orderId, from, OrderStatus.SHIPPED);

        inventory.onStatusChanged(event);
        email.onStatusChanged(event);          // if this throws, the two below never run
        analytics.onStatusChanged(event);
        warehouseFeed.onStatusChanged(event);
    }
}
