package com.jk.explore.money;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class AllocationTest {

    private static Money gbp(String s) {
        return Money.of(s, Currency.GBP);
    }

    @Test
    void tenPoundsBetweenThreeLosesNothing() {
        assertArrayEquals(new Money[] {gbp("3.34"), gbp("3.33"), gbp("3.33")}, gbp("10.00").allocate(1, 1, 1));
    }

    @Test
    void sharesByRatio() {
        assertArrayEquals(new Money[] {gbp("7.00"), gbp("3.00")}, gbp("10.00").allocate(70, 30));
    }

    @Test
    void sharesAlwaysAddBackToTheWhole() {
        for (long pence = 0; pence <= 2000; pence += 7) {
            Money whole = Money.ofMinor(pence, Currency.GBP);
            for (long[] ratios : new long[][] {{1, 1, 1}, {3, 5}, {1, 2, 3, 4}, {97, 2, 1}}) {
                Money sum = Money.zero(Currency.GBP);
                for (Money share : whole.allocate(ratios)) {
                    sum = sum.plus(share);
                }
                assertEquals(whole, sum, () -> "splitting " + whole);
            }
        }
    }

    @Test
    void theCartSpreadsADiscountByLineValue() {
        Cart cart = new Cart(Currency.GBP)
                .add("mug", gbp("9.49"), 3)
                .add("teapot", gbp("24.99"), 1)
                .add("coasters", gbp("4.99"), 2);
        assertEquals(gbp("63.44"), cart.total());
        assertArrayEquals(new Money[] {gbp("2.25"), gbp("1.97"), gbp("0.78")}, cart.discountShares(gbp("5.00")));
    }
}
