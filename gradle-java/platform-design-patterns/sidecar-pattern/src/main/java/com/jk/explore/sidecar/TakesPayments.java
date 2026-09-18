package com.jk.explore.sidecar;

/**
 * Anything in the shop that needs to take money from a customer.
 *
 * <p>There are four of them and they have nothing else in common: checkout takes money
 * while a customer waits, refunds gives it back, subscription billing runs overnight
 * against thousands of saved cards, and marketplace payouts pays sellers on a Friday.
 * Different teams, different repositories, different release cadences. The only thing
 * they share is the payment gateway at the other end — and, as it turns out, four copies
 * of the code that talks to it.
 */
public interface TakesPayments {

    /** The name the gateway knows this service by. */
    String name();

    /**
     * Takes the money, or throws {@link PaymentFailed}.
     *
     * <p>One call to this method may become several attempts at the gateway. How many is
     * exactly the question this project is about.
     */
    Receipt pay(Payment payment);
}
