package com.jk.explore.state;

import java.util.List;

/** Boxed and labelled, sitting on the outbound shelf. */
public final class PackedState implements OrderState {

    public static final OrderState INSTANCE = new PackedState();

    private PackedState() {
    }

    @Override
    public String name() {
        return "PACKED";
    }

    @Override
    public List<String> allowedActions() {
        return List.of("ship", "cancel");
    }

    @Override
    public void ship(Order order) {
        String consignment = "CON-" + order.id();
        order.recordConsignment(consignment);
        order.transitionTo(ShippedState.INSTANCE, "ship",
                "courier collected, consignment " + consignment);
    }

    /**
     * Still cancellable, but it costs more than it did a state ago: the box
     * has to be opened and the stock put back. That difference is exactly the
     * kind of thing that gets lost in a shared chain of conditionals.
     */
    @Override
    public void cancel(Order order, String reason) {
        Money back = order.ledger().charged().minus(order.ledger().refunded());
        order.ledger().refund(back);
        order.transitionTo(CancelledState.INSTANCE, "cancel",
                reason + " — refunded " + back + ", box opened and stock returned");
    }
}
