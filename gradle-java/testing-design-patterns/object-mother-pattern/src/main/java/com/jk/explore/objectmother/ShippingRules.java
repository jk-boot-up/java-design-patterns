package com.jk.explore.objectmother;

/**
 * The code under test: UK orders over 50 ship free, VIPs always ship free in the UK,
 * other UK orders pay 4.99, and orders abroad pay 15.00. Gift wrap adds 2.00.
 */
public final class ShippingRules {

    public static double cost(Order order) {
        double cost;
        if (!order.country().equals("GB")) {
            cost = 15.00;
        } else if (order.customer().vip() || order.total() > 50) {
            cost = 0.00;
        } else {
            cost = 4.99;
        }
        return order.giftWrap() ? cost + 2.00 : cost;
    }

    private ShippingRules() {
    }
}
