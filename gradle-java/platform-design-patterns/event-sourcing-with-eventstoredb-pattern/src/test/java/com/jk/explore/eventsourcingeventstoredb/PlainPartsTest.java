package com.jk.explore.eventsourcingeventstoredb;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need no server: the events, the fold, the JSON, and a checkout's own rule. */
class PlainPartsTest {

    private static final LocalDate DAY = LocalDate.of(2025, 3, 1);

    @Test
    void marchAddsUpTo140() {
        assertEquals(140, Balance.of(EventSourcingWithKurrentDemo.march("C-4417")));
    }

    @Test
    void anEmptyStreamIsZero() {
        assertEquals(0, Balance.of(List.of()));
    }

    @Test
    void eachEventMovesTheBalanceItsOwnWay() {
        assertEquals(60, new PointsAwarded("C-1", 60, "ORD-1", DAY).effectOnBalance());
        assertEquals(-25, new PointsRedeemed("C-1", 25, "ORD-2", DAY).effectOnBalance());
        assertEquals(-15, new PointsExpired("C-1", 15, DAY).effectOnBalance());
    }

    @Test
    void everyEventSurvivesTheTripToJsonAndBack() {
        for (LoyaltyEvent event : EventSourcingWithKurrentDemo.march("C-4417")) {
            String json = EventJson.toJson(event);
            assertEquals(event, EventJson.fromJson(EventJson.typeOf(event), json), json);
        }
    }

    @Test
    void theJsonIsPlainTextABeginnerCanRead() {
        assertEquals("{\"customerId\":\"C-4417\",\"points\":60,\"orderId\":\"ORD-8801\",\"on\":\"2025-03-01\"}",
                EventJson.toJson(new PointsAwarded("C-4417", 60, "ORD-8801", DAY)));
        assertEquals("{\"customerId\":\"C-4417\",\"points\":15,\"on\":\"2025-03-14\"}",
                EventJson.toJson(new PointsExpired("C-4417", 15, LocalDate.of(2025, 3, 14))));
    }

    @Test
    void anUnknownEventTypeIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> EventJson.fromJson("PriceChanged", "{}"));
    }

    @Test
    void aCheckoutDeclinesToSpendMoreThanItSaw() {
        Checkout checkout = new Checkout("the website", null);
        assertThrows(IllegalStateException.class, () -> checkout.redeem("C-1", new Checkout.Look(40, 4), 100,
                "ORD-1", DAY, LoyaltyLog.Check.EXPECTED_REVISION));
    }

    @Test
    void everyCustomerHasAStreamNamedAfterThem() {
        assertEquals("loyalty-C-4417", LoyaltyLog.streamFor("C-4417"));
    }

    @Test
    void theAdviceWithNoRuntimeSaysWhatToDo() {
        assertEquals(true, KurrentServer.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
        assertEquals(true, KurrentServer.NO_RUNTIME_ADVICE.contains("./gradlew run again"));
    }
}
