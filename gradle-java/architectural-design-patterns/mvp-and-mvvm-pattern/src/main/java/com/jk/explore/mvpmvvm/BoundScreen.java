package com.jk.explore.mvpmvvm;

/** A screen for MVVM: it binds its labels to the view model once, and then only draws. */
public class BoundScreen {

    private String totalLabel = "?";
    private String countLabel = "?";
    private String checkoutLabel = "?";

    public BoundScreen(CartViewModel vm, boolean forgetToBindTotal) {
        if (!forgetToBindTotal) {
            vm.total.bind(t -> totalLabel = t);
        }
        vm.count.bind(c -> countLabel = c + " items");
        vm.canCheckout.bind(b -> checkoutLabel = b ? "checkout on" : "checkout off");
    }

    public String drawn() {
        return totalLabel + " | " + countLabel + " | " + checkoutLabel;
    }
}
