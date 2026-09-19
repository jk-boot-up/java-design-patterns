package com.jk.explore.pactcdc;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class PactTest {

    @BeforeAll
    static void pacts() throws Exception {
        System.setProperty("pact_do_not_track", "true");
        assertTrue(Pacts.writeBoth());
    }

    @Test
    void aRenamedFieldBreaksCheckoutAtRunTime() throws Exception {
        assertEquals(-1, PactDemo.checkoutTotal(Release.RENAMED));
        assertEquals(3200, PactDemo.checkoutTotal(Release.V1));
    }

    @Test
    void thePactFilesListOnlyWhatEachConsumerReads() throws Exception {
        assertEquals(Map.of("priceCents", "integer", "sku", "string"), Pacts.expectations("checkout"));
        assertEquals(Map.of("sku", "string"), Pacts.expectations("reports"));
    }

    @Test
    void theCurrentReleasePassesBothPacts() throws Exception {
        Verifier.Outcome o = Verifier.verify(Release.V1);
        assertEquals(2, o.checked());
        assertEquals(List.of(), o.problems());
    }

    @Test
    void theRenameIsNamedForTheConsumerThatNeedsIt() throws Exception {
        Verifier.Outcome o = Verifier.verify(Release.RENAMED);
        assertEquals(2, o.checked());
        assertEquals(List.of("checkout - body: Actual map is missing the following keys: priceCents"), o.problems());
    }

    @Test
    void addingAFieldIsSafe() throws Exception {
        assertTrue(Verifier.verify(Release.EXTRA_FIELD).passed());
    }

    @Test
    void aChangeOfMeaningPassesThePact() throws Exception {
        assertTrue(Verifier.verify(Release.POUNDS).passed());
        assertFalse(PactDemo.checkoutTotal(Release.POUNDS) == 3200);
        assertEquals(32, PactDemo.checkoutTotal(Release.POUNDS));
    }
}
