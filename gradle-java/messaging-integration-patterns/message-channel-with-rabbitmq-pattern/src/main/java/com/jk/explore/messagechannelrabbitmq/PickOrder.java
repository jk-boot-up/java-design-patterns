package com.jk.explore.messagechannelrabbitmq;

/**
 * One instruction for the warehouse: pick this many of this item for this order.
 *
 * <p>A broker only moves bytes, so a message has to be turned into text on the way in and
 * read back out of text on the way out. This record owns both halves of that so no other
 * class has to think about it.
 */
public record PickOrder(String orderId, int quantity, String item) {

    public static PickOrder of(int n) {
        return new PickOrder("ORD-" + n, 2, "MUG-BLUE");
    }

    /** The text that actually travels: the order, the count and the item, separated by spaces. */
    public String text() {
        return orderId + " " + quantity + " " + item;
    }

    public static PickOrder read(String text) {
        String[] parts = text.split(" ");
        return new PickOrder(parts[0], Integer.parseInt(parts[1]), parts[2]);
    }
}
