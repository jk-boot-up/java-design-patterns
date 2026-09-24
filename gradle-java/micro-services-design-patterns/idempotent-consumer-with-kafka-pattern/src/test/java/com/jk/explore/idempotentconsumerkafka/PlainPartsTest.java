package com.jk.explore.idempotentconsumerkafka;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need no broker and no database at all. */
class PlainPartsTest {

    @Test
    void anOrderSurvivesTheTripThroughTextWithItsIdUnchanged() {
        OrderPlaced sent = OrderPlaced.of(2);
        Instant stamped = Instant.parse("2026-09-24T10:15:30Z");
        OrderPlaced arrived = OrderPlaced.read(sent.text(), stamped);
        assertEquals("placed-ORD-2", arrived.messageId());
        assertEquals("ORD-2", arrived.orderId());
        assertEquals(7195, arrived.pence());
        assertEquals(stamped, arrived.placedAt());
    }

    @Test
    void theSameOrderSentTwiceCarriesTheSameMessageId() {
        assertEquals(OrderPlaced.of(1).messageId(), OrderPlaced.of(1).messageId());
        assertEquals("your order ORD-1 for 7095 pence is confirmed", OrderPlaced.of(1).confirmation());
    }

    @Test
    void placesAreListedTheWayTheDemoPrintsThem() {
        assertEquals("0, 1, 2", KafkaIdempotentConsumerDemo.places(List.of(0L, 1L, 2L)));
    }

    @Test
    void aWaitThatNeverComesTrueFailsAndSaysWhatItWasWaitingFor() {
        IllegalStateException failure = assertThrows(IllegalStateException.class,
                () -> Poll.until("the order to arrive", Duration.ofMillis(200), () -> false));
        assertTrue(failure.getMessage().contains("the order to arrive"), failure.getMessage());
    }

    @Test
    void theAdviceWithNoContainerRuntimeSaysWhatToDo() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("./gradlew run"));
    }
}
