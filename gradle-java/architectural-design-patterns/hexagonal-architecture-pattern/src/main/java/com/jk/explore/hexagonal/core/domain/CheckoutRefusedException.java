package com.jk.explore.hexagonal.core.domain;

/**
 * The shop will not take this order, and the reason is the customer's business
 * rather than the system's: the product does not exist, or there are not enough
 * of it.
 *
 * <p>A declined card is <em>not</em> this. That one comes from the card
 * network, which is infrastructure, and it arrives as a different exception —
 * which is a distinction worth keeping, because one is a rule of the shop and
 * the other is a fact about the outside world.
 */
public class CheckoutRefusedException extends RuntimeException {

    public CheckoutRefusedException(String reason) {
        super(reason);
    }
}
