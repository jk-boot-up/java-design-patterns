package com.jk.explore.mvpmvvm;

/** MVVM: the view model exposes state the view binds to. It has no reference to any view. */
public class CartViewModel {

    private final Cart cart;
    public final Observable<String> total = new Observable<>("£0.00");
    public final Observable<Integer> count = new Observable<>(0);
    public final Observable<Boolean> canCheckout = new Observable<>(false);

    public CartViewModel(Cart cart) {
        this.cart = cart;
        update();
    }

    public void add(long priceCents) {
        cart.add(priceCents);
        update();
    }

    public void removeLast() {
        cart.removeLast();
        update();
    }

    private void update() {
        total.set(Cart.money(cart.totalCents()));
        count.set(cart.count());
        canCheckout.set(cart.count() > 0);
    }
}
