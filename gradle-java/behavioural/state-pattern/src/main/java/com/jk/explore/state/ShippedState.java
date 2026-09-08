package com.jk.explore.state;

import java.util.List;

/** With the courier. The shop no longer has the goods. */
public final class ShippedState implements OrderState {

    public static final OrderState INSTANCE = new ShippedState();

    private ShippedState() {
    }

    @Override
    public String name() {
        return "SHIPPED";
    }

    @Override
    public List<String> allowedActions() {
        return List.of("deliver");
    }

    @Override
    public void deliver(Order order) {
        order.transitionTo(DeliveredState.INSTANCE, "deliver",
                "signed for, " + order.consignment());
    }

    /**
     * The transition this whole project is about. Cancelling here would refund
     * a customer who is about to receive the goods anyway, and the shop has
     * nothing to put back on the shelf.
     */
    @Override
    public void cancel(Order order, String reason) {
        throw refuse("cancel", "it is already with the courier — the customer "
                + "must refuse delivery or return it");
    }
}
