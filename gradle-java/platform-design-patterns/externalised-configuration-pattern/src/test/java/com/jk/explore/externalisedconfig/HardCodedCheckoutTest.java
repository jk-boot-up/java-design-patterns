package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The naive checkout is correct, and these tests say so.
 *
 * <p>That is the point worth making before the pattern arrives. There is no
 * behaviour to fix here. The only thing wrong with this class is how long it takes
 * to change the number in it, and no unit test can see that.
 */
class HardCodedCheckoutTest {

    private final Checkout checkout = new HardCodedCheckout();

    @Test
    @DisplayName("a basket over the threshold ships free")
    void overTheThresholdShipsFree() {
        DeliveryQuote quote = checkout.quote(new Basket("ORD-7101", Money.pounds(62)));

        assertTrue(quote.isFree());
        assertEquals(Money.zero(), quote.deliveryCost());
    }

    @Test
    @DisplayName("a basket under the threshold pays standard delivery")
    void underTheThresholdPays() {
        DeliveryQuote quote = checkout.quote(new Basket("ORD-7102", Money.pounds(48)));

        assertFalse(quote.isFree());
        assertEquals(HardCodedCheckout.standardDelivery(), quote.deliveryCost());
    }

    @Test
    @DisplayName("the quote says the threshold came from the compiled program")
    void theQuoteNamesItsSource() {
        DeliveryQuote quote = checkout.quote(new Basket("ORD-7103", Money.pence(3150)));

        assertEquals(Money.pounds(50), quote.thresholdApplied());
        assertTrue(quote.thresholdCameFrom().contains("compiled"));
    }

    @Test
    @DisplayName("nothing in the program can change the threshold at runtime")
    void theThresholdCannotBeChangedWhileRunning() {
        Money before = checkout.quote(new Basket("ORD-1", Money.pounds(10))).thresholdApplied();
        Money after = checkout.quote(new Basket("ORD-2", Money.pounds(10))).thresholdApplied();

        // There is no method to call here, which is the whole of the problem: the
        // only way to get a different number is to build a different program.
        assertEquals(before, after);
        assertEquals(HardCodedCheckout.threshold(), after);
    }
}
