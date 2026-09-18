package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ClientEstateTest {

    private final ClientEstate estate = new ClientEstate()
            .add("phone app", true, "six fields on a four-inch screen")
            .add("desktop store", true, "description, specification, images, reviews")
            .add("tablet app", false, "the phone's fields in a wider column");

    @Test
    @DisplayName("a backend is justified by disagreement about the product, not by device count")
    void countsDisagreementsRatherThanClients() {
        assertEquals(3, estate.backendsIfOnePerClient());
        assertEquals(2, estate.backendsJustified());
    }

    @Test
    @DisplayName("a client that wants the same fields in a different layout justifies nothing")
    void aLayoutDifferenceIsNotADisagreement() {
        assertTrue(estate.backendsJustified() < estate.backendsIfOnePerClient());
    }

    @Test
    @DisplayName("the cost of a backend is stated as recurring work, not as servers")
    void namesTheRecurringCosts() {
        assertEquals(4, ClientEstate.whatEachBackendCosts().size());
    }
}
