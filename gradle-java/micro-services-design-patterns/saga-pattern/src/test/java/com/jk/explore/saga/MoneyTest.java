package com.jk.explore.saga;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** Money has to print refunds too, and a refund is a negative amount. */
class MoneyTest {

    @Test
    @DisplayName("a charge prints as pounds and pence")
    void positiveAmounts() {
        assertEquals("£70.95", Money.pence(7095).toString());
        assertEquals("£0.00", Money.pence(0).toString());
        assertEquals("£0.09", Money.pence(9).toString());
    }

    @Test
    @DisplayName("a refund prints with one minus sign, in front")
    void negativeAmounts() {
        assertEquals("-£70.95", Money.pence(-7095).toString());
        assertEquals("-£0.09", Money.pence(-9).toString());
    }

    @Test
    @DisplayName("line totals and sums")
    void arithmetic() {
        assertEquals(Money.pence(3596), Money.pence(899).times(4));
        assertEquals(Money.pence(7095), Money.pence(3499).plus(Money.pence(3596)));
        assertEquals(Money.pence(0), Money.pence(7095).minus(Money.pence(7095)));
    }
}
