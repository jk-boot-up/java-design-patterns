package com.jk.explore.translatorcamel;

import java.util.ArrayList;
import java.util.List;

/**
 * The warehouse: it only accepts the canonical order. Camel must convert the message body to
 * OrderMessage before this is called, and refuses if it cannot.
 */
public final class Warehouse {

    private final List<String> picks = new ArrayList<>();

    public void pick(OrderMessage order) {
        picks.add("pick " + order.quantity() + " x " + order.sku() + " for " + order.orderId());
    }

    public List<String> picks() {
        return picks;
    }
}
