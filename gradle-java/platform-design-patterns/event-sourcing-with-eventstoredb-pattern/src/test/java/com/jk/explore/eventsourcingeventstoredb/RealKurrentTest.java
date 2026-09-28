package com.jk.explore.eventsourcingeventstoredb;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import io.kurrent.dbclient.StreamNotFoundException;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What the real KurrentDB does, asked of it directly.
 *
 * <p>One server is started for the whole class, because starting it is the slow part, and stopped
 * at the end. KurrentDB has no "empty everything" command, so every test uses its own customer and
 * therefore its own stream. Every wait is a bounded poll on something that can be asked; there is
 * no sleep anywhere in this file.
 */
class RealKurrentTest {

    private static final LocalDate DAY = LocalDate.of(2025, 4, 2);
    private static KurrentServer server;
    private static LoyaltyLog log;

    @BeforeAll
    static void startKurrentDB() {
        assumeTrue(KurrentServer.containerRuntimeAvailable(), "needs a container runtime");
        server = new KurrentServer();
        server.start();
        log = new LoyaltyLog(server.connect());
    }

    @AfterAll
    static void stopKurrentDB() {
        if (log != null) {
            log.close();
        }
        if (server != null) {
            server.close();
        }
    }

    @Test
    void eventsAreNumberedFromZeroAndReadBackInOrderByAnotherConnection() {
        long last = EventSourcingWithKurrentDemo.writeMarch(log, "T-1");
        assertEquals(3, last);
        try (LoyaltyLog other = new LoyaltyLog(server.connect())) {
            LoyaltyLog.History history = other.read("T-1");
            assertEquals(EventSourcingWithKurrentDemo.march("T-1"), history.events());
            assertEquals(3, history.revision());
            assertEquals(140, history.balance());
        }
    }

    @Test
    void anAppendExpectingAnOldRevisionIsRefusedAndWritesNothing() {
        EventSourcingWithKurrentDemo.writeMarch(log, "T-2");
        LoyaltyLog.StreamMovedOn refusal = assertThrows(LoyaltyLog.StreamMovedOn.class, () ->
                log.appendExpecting("T-2", 2, EventJson.toEventData(new PointsRedeemed("T-2", 10, "ORD-1", DAY))));
        assertEquals(2, refusal.expected());
        assertEquals(3, refusal.actual());
        assertEquals(4, log.read("T-2").events().size());
    }

    @Test
    void anAppendExpectingNoStreamIsRefusedOnceTheStreamExists() {
        log.appendToNewStream("T-3", EventJson.toEventData(new PointsAwarded("T-3", 5, "ORD-1", DAY)));
        assertThrows(LoyaltyLog.StreamMovedOn.class, () ->
                log.appendToNewStream("T-3", EventJson.toEventData(new PointsAwarded("T-3", 5, "ORD-2", DAY))));
    }

    @Test
    void withTheCheckOffBothCheckoutsSpendTheSamePoints() {
        EventSourcingWithKurrentDemo.writeMarch(log, "T-4");
        EventSourcingWithKurrentDemo.Race race = EventSourcingWithKurrentDemo.race(server, "T-4", LoyaltyLog.Check.NONE);
        assertEquals(new Checkout.Look(140, 3), race.firstLook());
        assertEquals(java.util.List.of(4L, 5L), race.accepted());
        assertTrue(race.refused().isEmpty());
        assertEquals(-60, race.after().balance());
    }

    @Test
    void withTheExpectedRevisionExactlyOneCheckoutWins() {
        EventSourcingWithKurrentDemo.writeMarch(log, "T-5");
        EventSourcingWithKurrentDemo.Race race = EventSourcingWithKurrentDemo.race(server, "T-5",
                LoyaltyLog.Check.EXPECTED_REVISION);
        assertEquals(java.util.List.of(4L), race.accepted());
        assertEquals(1, race.refused().size());
        assertEquals(3, race.refused().get(0).expected());
        assertEquals(4, race.refused().get(0).actual());
        assertEquals(new Checkout.Look(40, 4), race.secondLook());
        assertEquals(40, race.after().balance());
    }

    @Test
    void aRetryWithTheSameEventIdAndExpectationIsWrittenOnce() {
        UUID id = UUID.randomUUID();
        PointsAwarded award = new PointsAwarded("T-6", 45, "ORD-9001", DAY);
        assertEquals(0, log.appendToNewStream("T-6", EventJson.toEventData(id, award)));
        assertEquals(0, log.appendToNewStream("T-6", EventJson.toEventData(id, award)));
        assertEquals(1, log.read("T-6").events().size());
    }

    @Test
    void aRetryWithANewEventIdIsASecondAward() {
        PointsAwarded award = new PointsAwarded("T-7", 45, "ORD-9001", DAY);
        log.append("T-7", EventJson.toEventData(award));
        log.append("T-7", EventJson.toEventData(award));
        assertEquals(90, log.read("T-7").balance());
    }

    @Test
    void aLateDashboardCatchesUpOnHistoryAndThenFollowsNewEvents() {
        EventSourcingWithKurrentDemo.writeMarch(log, "T-8");
        try (SupportDashboard dashboard = new SupportDashboard(server.connect())) {
            dashboard.start();
            Poll.until("the dashboard to catch up", dashboard::caughtUp);
            assertTrue(dashboard.eventsWhenCaughtUp() >= 4);
            assertEquals(140, dashboard.balanceOf("T-8"));
            log.appendExpecting("T-8", 3, EventJson.toEventData(new PointsAwarded("T-8", 20, "ORD-9300", DAY)));
            Poll.until("the dashboard to see the new award", () -> Integer.valueOf(160).equals(dashboard.balanceOf("T-8")));
        }
    }

    @Test
    void aDeletedStreamIsNotFoundButItsEventsStayInTheWholeLogAndItsNumberingCarriesOn() {
        EventSourcingWithKurrentDemo.writeMarch(log, "T-9");
        log.delete("T-9");
        assertThrows(StreamNotFoundException.class, () -> log.read("T-9"));
        assertFalse(log.exists("T-9"));
        assertEquals(4, log.countInWholeLog("T-9"));
        long reused = log.append("T-9", EventJson.toEventData(new PointsAwarded("T-9", 10, "ORD-9400", DAY)));
        assertEquals(4, reused);
        assertEquals(1, log.read("T-9").events().size());
    }
}
