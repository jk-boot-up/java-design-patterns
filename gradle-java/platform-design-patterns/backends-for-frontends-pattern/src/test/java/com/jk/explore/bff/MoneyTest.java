package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MoneyTest {

    @Test
    @DisplayName("pence become pounds with two decimal places")
    void formatsPence() {
        assertEquals("£47.99", Money.format(4799));
        assertEquals("£12.00", Money.format(1200));
    }

    @Test
    @DisplayName("a price under a pound keeps its leading zero")
    void padsTheMinorUnits() {
        assertEquals("£0.05", Money.format(5));
        assertEquals("£1.50", Money.format(150));
    }
}
