package com.jk.explore.eda;

/** The version without events: the order service calls the others and waits for each. */
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
