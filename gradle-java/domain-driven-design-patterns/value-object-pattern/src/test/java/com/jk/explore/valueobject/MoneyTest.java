package com.jk.explore.valueobject;

import com.jk.explore.valueobject.domain.CurrencyMismatch;
import com.jk.explore.valueobject.domain.Money;
import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class MoneyTest {

    @Test
    void arithmeticIsExact() {
        assertEquals(Money.gbp(330), Money.gbp(110).times(3));
        assertEquals(Money.gbp(30), Money.gbp(10).plus(Money.gbp(20)));
    }

    @Test
    void differentCurrenciesCannotBeCombined() {
        assertThrows(CurrencyMismatch.class, () -> Money.gbp(1).plus(Money.usd(1)));
        assertThrows(CurrencyMismatch.class, () -> Money.gbp(1).minus(Money.usd(1)));
    }

    @Test
    void aCurrencyMustBeThreeLetters() {
        assertThrows(IllegalArgumentException.class, () -> new Money(1, "POUNDS"));
        assertThrows(IllegalArgumentException.class, () -> new Money(1, null));
    }

    @Test
    void equalByValueAndSameHash() {
        assertEquals(Money.gbp(500), Money.gbp(500));
        assertEquals(Money.gbp(500).hashCode(), Money.gbp(500).hashCode());
        assertNotEquals(Money.gbp(500), Money.usd(500));
        Set<Money> set = new HashSet<>(List.of(Money.gbp(500), Money.gbp(500)));
        assertEquals(1, set.size());
    }

    @Test
    void operationsReturnNewValuesAndLeaveTheOriginalAlone() {
        Money price = Money.gbp(2000);
        Money discounted = price.minus(Money.gbp(500));
        assertEquals(Money.gbp(2000), price);
        assertEquals(Money.gbp(1500), discounted);
    }

    @Test
    void allocationAlwaysAddsBackToTheWholeAndSharesDifferByAtMostOnePenny() {
        for (long pence = -50; pence <= 200; pence++) {
            for (int parts = 1; parts <= 9; parts++) {
                List<Money> shares = Money.gbp(pence).allocate(parts);
                assertEquals(parts, shares.size());
                assertEquals(Money.gbp(pence), shares.stream().reduce(Money.gbp(0), Money::plus));
                long min = shares.stream().mapToLong(Money::pence).min().orElseThrow();
                long max = shares.stream().mapToLong(Money::pence).max().orElseThrow();
                assertTrue(max - min <= 1, pence + " into " + parts);
            }
        }
    }

    @Test
    void tenPoundsThreeWaysGivesTheOddPennyToTheFirst() {
        assertEquals(List.of(Money.gbp(334), Money.gbp(333), Money.gbp(333)), Money.gbp(1000).allocate(3));
        assertThrows(IllegalArgumentException.class, () -> Money.gbp(1000).allocate(0));
    }

    @Test
    void toStringIsReadable() {
        assertEquals("GBP 59.97", Money.gbp(5997).toString());
        assertEquals("GBP -0.05", Money.gbp(-5).toString());
    }
}
