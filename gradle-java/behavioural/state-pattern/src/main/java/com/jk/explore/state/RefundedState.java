package com.jk.explore.state;

import java.util.List;

/** Terminal. The goods came back and so did the money. */
public final class RefundedState implements OrderState {

    public static final OrderState INSTANCE = new RefundedState();

    private RefundedState() {
    }

    @Override
    public String name() {
        return "REFUNDED";
    }

    @Override
    public List<String> allowedActions() {
        return List.of();
    }
}
