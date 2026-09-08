package com.jk.explore.state;

import java.util.List;

/** Ordered, not yet paid for. Nothing has been taken from the customer. */
public final class PlacedState implements OrderState {

    public static final OrderState INSTANCE = new PlacedState();

    private PlacedState() {
    }

    @Override
    public String name() {
        return "PLACED";
    }

    @Override
    public List<String> allowedActions() {
        return List.of("pay", "cancel");
    }

    @Override
    public void pay(Order order) {
        order.ledger().charge(order.total());
        order.transitionTo(PaidState.INSTANCE, "pay", order.total() + " taken");
    }

    /**
     * The cheapest cancellation there is: no money has moved, so none has to
     * move back. Every other state's cancel has to undo something.
     */
    @Override
    public void cancel(Order order, String reason) {
        order.transitionTo(CancelledState.INSTANCE, "cancel",
                reason + " — nothing had been charged");
    }
}
