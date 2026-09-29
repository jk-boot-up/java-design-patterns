package com.jk.explore.remotefacademvc;

import org.springframework.stereotype.Component;

/**
 * Holds the one order the demo works with.
 */
@Component
public class OrderStore {

    private Order order = new Order();

    public Order order() {
        return order;
    }

    public void reset() {
        order = new Order();
    }
}
