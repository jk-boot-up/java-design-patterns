package com.jk.explore.mediator;

/**
 * The base class every widget on the checkout form extends.
 *
 * <p>It exists to make one point structurally: a widget holds exactly one
 * reference to anything else on the form, and that reference is the mediator.
 * A widget cannot reach the shipping list, the total or the button even if it
 * wanted to, because it has no field pointing at them.
 */
public abstract class FormWidget {

    private final String name;
    private final CheckoutMediator mediator;

    protected FormWidget(String name, CheckoutMediator mediator) {
        this.name = name;
        this.mediator = mediator;
    }

    /** The widget's label, used by the mediator to tell one from another. */
    public String name() {
        return name;
    }

    /**
     * Report that the shopper changed this widget. Subclasses call this from
     * their setters; what happens next is not their business.
     */
    protected void announceChange() {
        mediator.changed(this);
    }
}
