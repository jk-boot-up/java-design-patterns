package com.jk.explore.externalisedconfig;

/**
 * Works out what delivery costs for one basket.
 *
 * <p>There are two implementations, and the whole lesson is the difference
 * between them. {@link HardCodedCheckout} keeps the free-delivery threshold as
 * a constant in the source, so changing it means changing the program.
 * {@link ConfiguredCheckout} reads the threshold from outside the program every
 * time it quotes, so changing it means changing a value.
 *
 * <p>Both satisfy this interface identically, which is the point: no caller has
 * to know which one it is holding, and nothing about the shop's behaviour
 * changes when you swap them. What changes is what it costs to alter the
 * number — and, as the demo is at pains to show, what it costs to alter the
 * number <em>wrongly</em>.
 */
public interface Checkout {

    /** Quotes delivery for one basket, and says which threshold it used. */
    DeliveryQuote quote(Basket basket);

    /** How this checkout would describe itself in a report. */
    String describe();
}
