package com.jk.explore.delegation;

/** Hands each call on to its shipping helper, one method at a time. */
public class OrderWithShipping implements Shipping {

    private final Shipping shipping;

    public OrderWithShipping(Shipping shipping) {
        this.shipping = shipping;
    }

    @Override
    public long quoteCents(String destination) {
        return shipping.quoteCents(destination);
    }

    @Override
    public String carrier() {
        return shipping.carrier();
    }

    @Override
    public int daysToDeliver(String destination) {
        return shipping.daysToDeliver(destination);
    }

    @Override
    public boolean canDeliverTo(String destination) {
        return shipping.canDeliverTo(destination);
    }
}
