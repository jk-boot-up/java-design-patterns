package com.jk.explore.mediator;

/**
 * The button at the foot of the form.
 *
 * <p>Whether it may be pressed depends on the state of two other widgets, which
 * is exactly the kind of question a button should not be answering for itself.
 * The mediator answers it and pushes the result here.
 */
public class PlaceOrderButton extends FormWidget {

    private boolean enabled;

    public PlaceOrderButton(CheckoutMediator mediator) {
        super("placeOrder", mediator);
    }

    public boolean isEnabled() {
        return enabled;
    }

    /** Called by the mediator after it has re-checked the form. */
    void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}
