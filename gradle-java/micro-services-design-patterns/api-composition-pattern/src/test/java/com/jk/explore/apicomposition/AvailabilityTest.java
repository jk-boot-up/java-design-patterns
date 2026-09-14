package com.jk.explore.apicomposition;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The arithmetic, pinned down so the explainer's numbers cannot drift. */
class AvailabilityTest {

    @Test
    @DisplayName("three services at 99.9% make a page at 99.7%")
    void availabilitiesMultiply() {
        double page = Availability.whenAllAreRequired(0.999, 0.999, 0.999);

        assertEquals("99.700%", Availability.asPercent(page));
        assertTrue(page < 0.999);
    }

    @Test
    @DisplayName("the page is down about three times as long as any one service")
    void downtimeAddsUp() {
        double perService = Availability.downtimeMinutesPerMonth(0.999);
        double page = Availability.downtimeMinutesPerMonth(
                Availability.whenAllAreRequired(0.999, 0.999, 0.999));

        // Forty-three minutes each becomes over two hours for the page. Not exactly
        // three times: the outages very occasionally overlap, which is the only good
        // news in the whole calculation.
        assertEquals(43.2, perService);
        assertEquals(129.5, page);
        assertTrue(page > 2 * perService);
    }

    @Test
    @DisplayName("making two of the three optional gives the page its availability back")
    void optionalDependenciesDoNotMultiply() {
        assertEquals("99.900%",
                Availability.asPercent(Availability.whenOnlyOneIsRequired(0.999)));
    }

    @Test
    @DisplayName("more dependencies is always worse, never better")
    void everyExtraDependencyCosts() {
        double three = Availability.whenAllAreRequired(0.999, 0.999, 0.999);
        double four = Availability.whenAllAreRequired(0.999, 0.999, 0.999, 0.999);

        assertTrue(four < three);
    }
}
