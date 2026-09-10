package com.jk.explore.mediator;

/**
 * The order total shown at the bottom of the form.
 *
 * <p>A label the shopper cannot edit, so it never announces anything. It is
 * written to by the mediator and read by everyone else.
 */
public class TotalLabel extends FormWidget {

    private int pounds;

    public TotalLabel(CheckoutMediator mediator) {
        super("total", mediator);
    }

    public int pounds() {
        return pounds;
    }

    public String text() {
        return "Total: £" + pounds;
    }

    /** Called by the mediator after any change that moves the price. */
    void show(int pounds) {
        this.pounds = pounds;
    }
}
