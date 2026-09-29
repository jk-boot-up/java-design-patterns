package com.jk.explore.money;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.RoundingMode;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class MoneyTest {

    private static Money gbp(String s) {
        return Money.of(s, Currency.GBP);
    }

    @Test
    void storesTheSmallestUnitExactly() {
        assertEquals(1999, gbp("19.99").minor());
        assertEquals(1500, Money.of("1500", Currency.JPY).minor());
    }

    @Test
    void tenPenceAndTwentyPenceIsThirtyPence() {
        assertEquals(gbp("0.30"), gbp("0.10").plus(gbp("0.20")));
    }

    @Test
    void aThousandTenPencesAreExactlyOneHundredPounds() {
        Money sum = Money.zero(Currency.GBP);
        for (int i = 0; i < 1000; i++) {
            sum = sum.plus(gbp("0.10"));
        }
        assertEquals(gbp("100.00"), sum);
    }

    @Test
    void refusesToMixCurrencies() {
        var e = assertThrows(IllegalArgumentException.class,
                () -> gbp("10.00").plus(Money.of("10.00", Currency.USD)));
        assertEquals("cannot combine GBP with USD", e.getMessage());
    }

    @ParameterizedTest
    @ValueSource(strings = {"9.999", "0.001", "1.123"})
    void refusesMoreDigitsThanTheCurrencyHas(String amount) {
        assertThrows(IllegalArgumentException.class, () -> gbp(amount));
    }

    @Test
    void roundingByARateIsExplicit() {
        assertEquals(gbp("0.20"), gbp("0.99").times("0.20", RoundingMode.HALF_UP));
        assertEquals(gbp("0.19"), gbp("0.99").times("0.20", RoundingMode.DOWN));
    }

    @Test
    void equalAmountsInDifferentCurrenciesAreNotEqual() {
        assertNotEquals(gbp("5.00"), Money.of("5.00", Currency.USD));
    }

    @Test
    void neverChanges() {
        Money price = gbp("9.49");
        price.plus(gbp("1.00"));
        price.times(3);
        assertEquals(gbp("9.49"), price);
    }

    @Test
    void printsWithItsSymbolAndDigits() {
        assertEquals("£19.99", gbp("19.99").toString());
        assertEquals("¥1500", Money.of("1500", Currency.JPY).toString());
        assertEquals("$5.00", Money.of("5", Currency.USD).toString());
    }

    @Test
    void comparesWithinOneCurrency() {
        assertTrue(gbp("2.00").isGreaterThan(gbp("1.99")));
    }
}
