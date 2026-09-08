package com.jk.explore.state;

import java.util.List;

/** Paid for, waiting to be picked and boxed. */
public final class PaidState implements OrderState {

    public static final OrderState INSTANCE = new PaidState();

    private PaidState() {
    }

    @Override
    public String name() {
        return "PAID";
    }

    @Override
    public List<String> allowedActions() {
        return List.of("pack", "cancel");
    }

    @Override
    public void pack(Order order) {
        order.transitionTo(PackedState.INSTANCE, "pack",
                order.itemCount() + " item(s) boxed at Reading");
    }

    @Override
    public void cancel(Order order, String reason) {
        Money back = order.ledger().charged().minus(order.ledger().refunded());
        order.ledger().refund(back);
        order.transitionTo(CancelledState.INSTANCE, "cancel",
                reason + " — refunded " + back + ", nothing had shipped");
    }
}
