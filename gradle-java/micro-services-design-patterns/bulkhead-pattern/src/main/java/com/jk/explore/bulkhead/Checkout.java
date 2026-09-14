package com.jk.explore.bulkhead;

import java.util.concurrent.Callable;

/**
 * Taking a shopper's money. The one job in the shop that must not wait.
 *
 * It is not slow and it is not broken. Everything about it is fine. The only thing it
 * needs is a thread, and this whole project is about the fact that in a shop with one
 * shared pool, "a thread" is not something it can count on having.
 */
public final class Checkout {

    /** Takes payment for one order. Fast, always. */
    public Callable<String> takePayment(String orderId) {
        return () -> "paid " + orderId;
    }
}
