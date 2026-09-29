package com.jk.explore.resequencer;

/**
 * "Order ORD-1 is now PAID": numbered by the order service so the receiver can tell the right order.
 */
public record StatusUpdate(String orderId, int seq, String status) {

    @Override
    public String toString() {
        return orderId + "#" + seq + " " + status;
    }
}
