package com.jk.explore.state;

/**
 * One line of an order's history: what was asked for, where the order was
 * when it was asked, and where it ended up.
 *
 * <p>Rejections are recorded too. An order that refused to be cancelled is
 * more interesting than one that was never asked, and a customer-services
 * screen needs to show both.
 */
public record OrderEvent(String action, String from, String to, String detail) {

    /** A transition that happened. */
    static OrderEvent moved(String action, String from, String to, String detail) {
        return new OrderEvent(action, from, to, detail);
    }

    /** A transition that was refused. The order did not move. */
    static OrderEvent refused(String action, String from, String reason) {
        return new OrderEvent(action, from, from, "refused: " + reason);
    }

    public boolean wasRefused() {
        return detail.startsWith("refused: ");
    }

    @Override
    public String toString() {
        return String.format("%-8s %-10s -> %-10s %s", action, from, to, detail);
    }
}
