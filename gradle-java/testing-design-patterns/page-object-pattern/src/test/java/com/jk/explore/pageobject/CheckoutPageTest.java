package com.jk.explore.pageobject;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

/**
 * Checkout tests written the way the pattern recommends: no selectors, no waiting, just the shop's words.
 */
class CheckoutPageTest {

    private final CheckoutPage checkout = new CheckoutPage(new FakeBrowser("#apply-coupon"));

    @Test
    void totalBeforeAnyCoupon() {
        assertEquals("50.00", checkout.total());
    }

    @Test
    void save10TakesTenPercentOff() {
        assertEquals("45.00", checkout.applyCoupon("SAVE10").total());
    }

    @Test
    void unknownCouponChangesNothing() {
        assertEquals("50.00", checkout.applyCoupon("BOGUS").total());
    }

    @Test
    void placingAnOrderShowsItsNumber() {
        assertEquals("ORD-1042", checkout.placeOrder().orderNumber());
    }
}
