package com.jk.explore.staticfactory;

/**
 * The client. It is handed a {@link Discount} and applies it.
 *
 * <p>There is no {@code if} on the kind of discount here, and no
 * {@code new} either. Whether the customer gets 10% off, £5 off, free
 * shipping or nothing at all, these same few lines run unchanged — because
 * the choosing already happened, inside a static factory method.
 */
public class CheckoutService {

    public Receipt checkout(Order order, Discount discount) {
        Money off = discount.appliedTo(order);
        Money total = order.subtotal().plus(order.shipping()).minus(off);

        System.out.println("Checkout: order " + order.orderId()
                + " subtotal " + order.subtotal() + " + shipping " + order.shipping());
        System.out.println("Checkout: " + discount.describe() + " saves " + off);
        System.out.println("Checkout: total " + total);

        return new Receipt(order.orderId(), order.subtotal(), order.shipping(),
                discount.describe(), off, total);
    }
}
