package com.jk.explore.hexagonal;

import com.jk.explore.hexagonal.core.domain.Money;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class MoneyTest {

    @Test
    void poundsAndPenceCombineIntoOneLongValue() {
        assertEquals(24900L, Money.pounds(249, 0).pence());
        assertEquals(8950L, Money.pounds(89, 50).pence());
    }

    @Test
    void plusAddsPence() {
        Money total = Money.pounds(249, 0).plus(Money.pounds(89, 50)).plus(Money.pounds(44, 0));
        assertEquals(Money.pounds(382, 50), total);
    }

    @Test
    void timesMultipliesByQuantity() {
        assertEquals(Money.pounds(44, 0), Money.pounds(22, 0).times(2));
    }

    @Test
    void toStringFormatsAsPoundsAndPence() {
        assertEquals("£382.50", Money.pounds(382, 50).toString());
        assertEquals("£0.00", Money.ZERO.toString());
    }
}
