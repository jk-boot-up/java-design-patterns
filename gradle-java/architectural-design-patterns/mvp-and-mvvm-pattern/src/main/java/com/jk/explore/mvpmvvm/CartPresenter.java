package com.jk.explore.mvpmvvm;

/** MVP: the presenter holds the rules and tells the view what to show, step by step. */
public class CartPresenter {

    private final Cart cart;
    private final CartView view;

    public CartPresenter(Cart cart, CartView view) {
        this.cart = cart;
        this.view = view;
        refresh();
    }

    public void onAdd(long priceCents) {
        cart.add(priceCents);
        refresh();
    }

    public void onRemoveLast() {
        cart.removeLast();
        refresh();
    }

    private void refresh() {
        view.showTotal(Cart.money(cart.totalCents()));
        view.showCount(cart.count());
        view.enableCheckout(cart.count() > 0);
    }
}
