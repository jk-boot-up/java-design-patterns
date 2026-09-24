package com.jk.explore.competingconsumersrabbitmq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import org.junit.jupiter.api.Test;

/** The parts that need no broker at all. */
class PlainPartsTest {

    @Test
    void anOrderSurvivesTheTripThroughText() {
        PickOrder sent = PickOrder.of(7);
        PickOrder arrived = PickOrder.read(sent.text());
        assertEquals("ORD-7", arrived.orderId());
        assertEquals(2, arrived.quantity());
        assertEquals("MUG-BLUE", arrived.item());
    }

    @Test
    void theStockLedgerCountsEveryReservationSoADuplicateShowsUp() {
        Stock stock = new Stock();
        stock.reserve(PickOrder.of(3));
        stock.reserve(PickOrder.of(3));
        stock.reserve(PickOrder.of(4));
        assertEquals(2, stock.timesReserved("ORD-3"));
        assertEquals(1, stock.timesReserved("ORD-4"));
        assertEquals(0, stock.timesReserved("ORD-5"));
    }

    @Test
    void aWaitThatNeverComesTrueFailsAndSaysWhatItWasWaitingFor() {
        IllegalStateException failure = assertThrows(IllegalStateException.class,
                () -> Poll.until("the sky to fall in", Duration.ofMillis(200), () -> false));
        assertTrue(failure.getMessage().contains("the sky to fall in"), failure.getMessage());
    }

    @Test
    void aWaitReturnsAsSoonAsTheConditionIsTrue() {
        int[] asked = {0};
        Poll.until("the third question", Duration.ofSeconds(5), () -> ++asked[0] == 3);
        assertEquals(3, asked[0]);
    }

    @Test
    void withNoContainerRuntimeTheDemoSaysWhatToDoAboutIt() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("container runtime"), Broker.NO_RUNTIME_ADVICE);
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("./gradlew run again"), Broker.NO_RUNTIME_ADVICE);
    }

    @Test
    void theBrokerImageIsTheSmallAlpineBuildOfTheNewestRelease() {
        assertEquals("rabbitmq:4.3.6-alpine", Broker.IMAGE);
    }
}
