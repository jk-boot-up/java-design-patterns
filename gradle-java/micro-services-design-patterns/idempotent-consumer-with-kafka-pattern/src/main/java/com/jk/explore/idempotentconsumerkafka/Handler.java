package com.jk.explore.idempotentconsumerkafka;

/**
 * What one copy of the notifications service does with an order it has been handed.
 *
 * <p>Four versions follow, from the one that remembers nothing to the pattern itself. Each
 * returns true when it queued a confirmation email, and false when it decided the order
 * had been handled already.
 */
public interface Handler {

    boolean handle(OrderPlaced order);
}
