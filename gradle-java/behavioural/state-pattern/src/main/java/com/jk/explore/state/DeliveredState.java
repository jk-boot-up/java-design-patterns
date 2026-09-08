package com.jk.explore.state;

import java.util.List;

/** Signed for. The only thing left is a return. */
public final class DeliveredState implements OrderState {

    public static final OrderState INSTANCE = new DeliveredState();

    private DeliveredState() {
    }

    @Override
    public String name() {
        return "DELIVERED";
    }

    @Override
    public List<String> allowedActions() {
        return List.of("refund");
    }

    @Override
    public void refund(Order order, String reason) {
        Money back = order.ledger().charged().minus(order.ledger().refunded());
        order.ledger().refund(back);
        order.transitionTo(RefundedState.INSTANCE, "refund",
                reason + " — returned and refunded " + back);
    }

    @Override
    public void cancel(Order order, String reason) {
        throw refuse("cancel", "the customer already has it — this is a return, "
                + "and returns are refunds");
    }
}
