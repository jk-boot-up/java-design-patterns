package com.jk.explore.mediator;

/**
 * The delivery country drop-down.
 *
 * <p>Changing the country has consequences all over the form — which shipping
 * methods exist, whether gift wrap is offered, what the total is. None of that
 * is written here. This class knows how to hold a country and how to say that
 * it changed.
 */
public class CountrySelector extends FormWidget {

    private String country = "";

    public CountrySelector(CheckoutMediator mediator) {
        super("country", mediator);
    }

    public String country() {
        return country;
    }

    /** The shopper picks a country. */
    public void select(String country) {
        this.country = country;
        announceChange();
    }
}
