package com.jk.explore.edakafka;

/** The version without a log: the order service calls shipping and waits. */
public class DirectShop {

    private final boolean shippingUp;
    private int placed;

    public DirectShop(boolean shippingUp) {
        this.shippingUp = shippingUp;
    }

    public boolean place(String orderId) {
        if (!shippingUp) {
            return false;
        }
        placed++;
        return true;
    }

    public int placed() {
        return placed;
    }
}
