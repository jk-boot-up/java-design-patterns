package com.jk.explore.pubsubredis;

/**
 * One fact about an order: it was placed, or it was cancelled.
 *
 * <p>Redis moves text, not Java objects, so an event is turned into text on the way out and
 * read back from text on the way in. This record owns both halves, so no other class has to
 * think about it.
 */
public record OrderEvent(String kind, String orderId) {

    public static OrderEvent placed(int n) {
        return new OrderEvent("OrderPlaced", "ORD-" + n);
    }

    public static OrderEvent cancelled(int n) {
        return new OrderEvent("OrderCancelled", "ORD-" + n);
    }

    /** The Redis channel name this kind of event is published under. */
    public String channel() {
        return kind.equals("OrderPlaced") ? OrderService.PLACED : OrderService.CANCELLED;
    }

    /** The text that actually travels: the kind, then the order number. */
    public String text() {
        return kind + " " + orderId;
    }

    public static OrderEvent read(String text) {
        String[] parts = text.split(" ");
        return new OrderEvent(parts[0], parts[1]);
    }

    @Override
    public String toString() {
        return text();
    }
}
