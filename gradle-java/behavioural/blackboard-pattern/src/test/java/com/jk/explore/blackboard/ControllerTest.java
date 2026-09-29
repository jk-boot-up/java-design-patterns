package com.jk.explore.blackboard;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ControllerTest {

    @Test
    void goodOrderRunsEveryCheckAndIsApproved() {
        Controller c = new Controller(Checks.standard());
        assertEquals("APPROVE", c.decide(new Blackboard(BlackboardDemo.goodOrder())));
        assertEquals(6, c.ran());
    }

    @Test
    void riskyOrderStopsBeforeTheExpensiveCheck() {
        Blackboard b = new Blackboard(BlackboardDemo.riskyOrder());
        Controller c = new Controller(Checks.standard());
        assertEquals("REJECT", c.decide(b));
        assertEquals(70, b.risk());
        assertFalse(b.has("deviceChecked"));
        assertEquals(102, c.spentMs());
    }

    @Test
    void comparisonWaitsForBothLookups() {
        KnowledgeSource match = Checks.countryMatch();
        Blackboard b = new Blackboard(Map.of("card", "4000-GB"));
        assertFalse(match.ready(b));
        b.post("t", "cardCountry", "GB");
        b.post("t", "ipCountry", "GB");
        assertTrue(match.ready(b));
    }

    @Test
    void cheapestReadyCheckGoesFirst() {
        Blackboard b = new Blackboard(BlackboardDemo.goodOrder());
        new Controller(List.of(Checks.deviceFingerprint(), Checks.orderValue())).decide(b);
        assertTrue(b.log().get(0).startsWith("order value"));
    }

    @Test
    void newCheckCatchesGiftCards() {
        List<KnowledgeSource> sources = new java.util.ArrayList<>(Checks.standard());
        sources.add(Checks.giftCards());
        assertEquals("REJECT", new Controller(sources).decide(new Blackboard(BlackboardDemo.giftCardOrder())));
    }

    @Test
    void oldMethodAgreesButSpendsMore() {
        FraudCheckAll all = new FraudCheckAll();
        assertEquals("REJECT", all.decide(BlackboardDemo.riskyOrder()));
        assertEquals(902, all.spentMs());
    }
}
