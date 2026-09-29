package com.jk.explore.filtercamel;

import java.util.ArrayList;
import java.util.List;

/**
 * What one service was handed, in order.
 */
public final class Received {

    private final List<String> orders = new ArrayList<>();

    public void take(OrderEvent order) {
        orders.add(order.getOrderId());
    }

    public List<String> orders() {
        return orders;
    }

    public void clear() {
        orders.clear();
    }
}
