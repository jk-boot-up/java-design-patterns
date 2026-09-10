package com.jk.explore.mediator;

import java.util.ArrayList;
import java.util.List;

/**
 * The shipping-method drop-down.
 *
 * <p>Its list of options is not fixed: the mediator refills it whenever the
 * delivery country changes, because a courier that serves the United Kingdom
 * is not the one that serves the United States.
 */
public class ShippingSelector extends FormWidget {

    private final List<String> options = new ArrayList<>();
    private String chosen = "";

    public ShippingSelector(CheckoutMediator mediator) {
        super("shipping", mediator);
    }

    public List<String> options() {
        return List.copyOf(options);
    }

    public String chosen() {
        return chosen;
    }

    /**
     * Replace the offered methods. Anything the shopper had already picked is
     * cleared, because it may not be on the new list at all.
     *
     * <p>The mediator calls this, so it does not announce a change — that would
     * be the form reacting to itself.
     */
    void showOptions(List<String> newOptions) {
        options.clear();
        options.addAll(newOptions);
        chosen = "";
    }

    /** The shopper picks a method. */
    public void select(String method) {
        this.chosen = method;
        announceChange();
    }
}
