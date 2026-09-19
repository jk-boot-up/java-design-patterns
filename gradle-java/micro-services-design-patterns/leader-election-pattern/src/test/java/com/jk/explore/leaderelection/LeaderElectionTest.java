package com.jk.explore.leaderelection;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LeaderElectionTest {

    private final Clock clock = new Clock();
    private final LeaseStore store = new LeaseStore(clock);

    @Test
    void theFirstToAskLeadsAndOthersAreRefused() {
        assertTrue(store.acquireOrRenew("A", 30).isPresent());
        assertTrue(store.acquireOrRenew("B", 30).isEmpty());
        assertEquals("A", store.leader().orElseThrow());
    }

    @Test
    void theHolderRenewsAndKeepsTheSameToken() {
        long token = store.acquireOrRenew("A", 30).orElseThrow().token();
        clock.advance(20);
        assertEquals(token, store.acquireOrRenew("A", 30).orElseThrow().token());
        clock.advance(20);
        assertTrue(store.acquireOrRenew("B", 30).isEmpty());
    }

    @Test
    void anExpiredLeaseCanBeTakenAndTheTokenGoesUp() {
        long first = store.acquireOrRenew("A", 30).orElseThrow().token();
        clock.advance(30);
        assertTrue(store.leader().isEmpty());
        long second = store.acquireOrRenew("B", 30).orElseThrow().token();
        assertEquals(first + 1, second);
    }

    @Test
    void withNoElectionEveryCopySendsTheReport() {
        ReportSink sink = new ReportSink(false);
        new Node("A", store, sink, 30).sendReportAlways();
        new Node("B", store, sink, 30).sendReportAlways();
        assertEquals(2, sink.written().size());
    }

    @Test
    void onlyTheLeaderSends() {
        ReportSink sink = new ReportSink(false);
        Node a = new Node("A", store, sink, 30);
        Node b = new Node("B", store, sink, 30);
        a.tryToLead();
        b.tryToLead();
        a.sendReportIfLeader();
        b.sendReportIfLeader();
        assertEquals(java.util.List.of("A"), sink.written());
    }

    @Test
    void aPausedLeaderStillSendsWithoutFencingAndIsRefusedWithIt() {
        for (boolean fencing : new boolean[]{false, true}) {
            Clock c = new Clock();
            LeaseStore s = new LeaseStore(c);
            ReportSink sink = new ReportSink(fencing);
            Node a = new Node("A", s, sink, 30);
            Node b = new Node("B", s, sink, 30);
            a.tryToLead();
            c.advance(35);
            b.tryToLead();
            b.sendReportIfLeader();
            if (fencing) {
                assertThrows(ReportSink.StaleToken.class, a::sendReportIfLeader);
                assertEquals(java.util.List.of("B"), sink.written());
            } else {
                a.sendReportIfLeader();
                assertEquals(java.util.List.of("B", "A"), sink.written());
            }
        }
    }

    @Test
    void aDeadNodeNeitherLeadsNorSends() {
        ReportSink sink = new ReportSink(false);
        Node a = new Node("A", store, sink, 30);
        a.die();
        a.tryToLead();
        assertFalse(a.sendReportIfLeader());
        assertTrue(store.leader().isEmpty());
    }

    @Test
    void aLeaseShorterThanTheRenewalIntervalLosesLeadership() {
        assertEquals(5, LeaderElectionDemo.secondLeadershipWasLost(5, 7));
        assertEquals(-1, LeaderElectionDemo.secondLeadershipWasLost(30, 7));
    }
}
