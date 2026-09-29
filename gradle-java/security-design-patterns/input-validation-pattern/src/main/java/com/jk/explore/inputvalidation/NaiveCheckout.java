package com.jk.explore.inputvalidation;

/**
 * Before: the form's text is used as it arrives.
 */
public final class NaiveCheckout {

    public static double total(OrderForm form, double price) {
        return Integer.parseInt(form.quantity()) * price;
    }

    private NaiveCheckout() {
    }
}
