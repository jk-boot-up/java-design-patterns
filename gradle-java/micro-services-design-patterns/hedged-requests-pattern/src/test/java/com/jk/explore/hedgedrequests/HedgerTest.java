package com.jk.explore.hedgedrequests;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class HedgerTest {

    @Test
    void fastPrimaryNeedsNoHedge() throws Exception {
        try (Hedger hedger = new Hedger()) {
            String answer = hedger.call(new Replica("A", 5).price("X"), new Replica("B", 5).price("X"), 200);
            assertTrue(answer.endsWith("from A"));
            assertEquals(0, hedger.hedgesSent());
        }
    }

    @Test
    void slowPrimaryIsHedged() throws Exception {
        try (Hedger hedger = new Hedger()) {
            String answer = hedger.call(new Replica("A", 2000).price("X"), new Replica("B", 5).price("X"), 20);
            assertTrue(answer.endsWith("from B"));
            assertEquals(1, hedger.hedgesSent());
        }
    }

    @Test
    void hedgingOnlyCutsTheTail() {
        LatencyModel.Stats s = LatencyModel.simulate(1000, 50);
        assertEquals(20, s.p50());
        assertTrue(s.worst() <= 50 + LatencyModel.FAST);
    }
}
