package com.jk.explore.specialcase;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class SpecialCaseTest {

    private final Directory d = new Directory();

    @Test
    void findNeverReturnsNull() {
        assertNotNull(d.find(null));
        assertNotNull(d.find("nobody"));
    }

    @Test
    void noIdIsAGuestUnknownIdIsUnknown() {
        assertInstanceOf(SpecialCases.Guest.class, d.find(null));
        assertInstanceOf(SpecialCases.Unknown.class, d.find("C-99"));
    }

    @Test
    void registeredGetsDiscountAndPoints() {
        assertEquals("Priya pays £38.00, points 158, added to newsletter", Checkout.run(d.find("C-17"), 4000));
    }

    @Test
    void guestPaysFullPriceAndEarnsNothing() {
        Customer g = d.find(null);
        assertEquals("Guest pays £40.00, points 0", Checkout.run(g, 4000));
        assertEquals(0, g.points());
    }

    @Test
    void nullVersionCrashesForAGuest() {
        assertThrows(NullPointerException.class, () -> Checkout.withNullChecks(null, 4000));
    }
}
