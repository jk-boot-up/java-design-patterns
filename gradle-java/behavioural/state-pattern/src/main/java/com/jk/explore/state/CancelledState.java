package com.jk.explore.state;

import java.util.List;

/**
 * Terminal. Anything owed has already been given back, which is why this
 * state accepts nothing — including, and especially, a second refund.
 */
public final class CancelledState implements OrderState {

    public static final OrderState INSTANCE = new CancelledState();

    private CancelledState() {
    }

    @Override
    public String name() {
        return "CANCELLED";
    }

    @Override
    public List<String> allowedActions() {
        return List.of();
    }
}
