package com.jk.explore.cleanspring;

import com.jk.explore.cleanspring.entities.Money;
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
    void toStringFormatsAsPoundsAndPence() {
        assertEquals("£382.50", Money.pounds(382, 50).toString());
    }
}
