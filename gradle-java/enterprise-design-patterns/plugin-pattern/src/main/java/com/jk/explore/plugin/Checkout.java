package com.jk.explore.plugin;

import java.util.List;

/**
 * Checkout, which only knows the interfaces it is given.
 */
public final class Checkout {

    public static List<String> placeOrder(Services.PaymentGateway gateway, Services.Emailer emailer) {
        return List.of(gateway.charge("ORD-1", 6344), emailer.send("priya@example.com", "Thanks for your order"));
    }

    private Checkout() {
    }
}
