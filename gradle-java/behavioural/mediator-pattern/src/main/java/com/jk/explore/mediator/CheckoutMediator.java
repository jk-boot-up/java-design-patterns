package com.jk.explore.mediator;

/**
 * The mediator: the one object that knows how the checkout form's parts affect
 * each other.
 *
 * <p>Every widget on the form holds a reference to this and to nothing else.
 * When a widget's value changes it does not decide what that means for the rest
 * of the form — it simply reports the change and lets the mediator work it out.
 */
public interface CheckoutMediator {

    /** Called by a widget after the shopper has changed its value. */
    void changed(FormWidget source);
}
