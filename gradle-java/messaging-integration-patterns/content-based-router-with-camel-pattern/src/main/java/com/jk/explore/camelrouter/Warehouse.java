package com.jk.explore.camelrouter;

/**
 * The receiving service as it looks before anybody writes a router: one queue for every order, and an
 * if for every kind of order inside the warehouse itself. The warehouse can put a physical item in a box.
 * It can do nothing at all with a gift card or a subscription, so those are counted and set aside.
 */
public class Warehouse {

    private int shipped;
    private int couldNotHandle;

    public void handle(Order order) {
        if (order.kind().equals("physical")) {
            shipped++;
        } else {
            couldNotHandle++;
        }
    }

    public int shipped() {
        return shipped;
    }

    public int couldNotHandle() {
        return couldNotHandle;
    }
}
