package com.jk.explore.mvpmvvm;

/** The version where the screen decides everything: the rules are welded to the widgets. */
public class FatCartScreen extends Window {

    private final Cart cart = new Cart();
    private String totalLabel = "£0.00";
    private boolean checkoutEnabled;

    public void onAddClicked(long priceCents) {
        cart.add(priceCents);
        totalLabel = Cart.money(cart.totalCents());
        checkoutEnabled = cart.count() > 0;
    }

    public String totalLabel() {
        return totalLabel;
    }

    public boolean checkoutEnabled() {
        return checkoutEnabled;
    }
}
