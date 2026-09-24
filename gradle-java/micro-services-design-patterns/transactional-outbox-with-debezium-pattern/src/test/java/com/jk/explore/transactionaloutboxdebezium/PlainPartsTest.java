package com.jk.explore.transactionaloutboxdebezium;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need nothing installed. */
class PlainPartsTest {

    @Test
    void anOrderIsNumberedAndCarriesItsTotalInPence() {
        Order order = Order.number(1);
        assertEquals("ORD-1", order.orderId());
        assertEquals(2995, order.totalPence());
        assertEquals("{\"orderId\":\"ORD-1\",\"customer\":\"customer-1\",\"totalPence\":2995}", order.asJson());
    }

    @Test
    void anEventIdIsTheSameEveryTimeItIsMade() {
        assertEquals("ORD-7/OrderPaid", OutboxCheckout.eventId("ORD-7", "OrderPaid"));
        assertEquals(OutboxCheckout.eventId("ORD-7", "OrderPaid"), OutboxCheckout.eventId("ORD-7", "OrderPaid"));
    }

    @Test
    void partitionsAreDescribedInWords() {
        List<OrderEvent> events = List.of(
                new OrderEvent(1, 0, "ORD-1", "OrderPlaced", "ORD-1/OrderPlaced"),
                new OrderEvent(2, 0, "ORD-2", "OrderPlaced", "ORD-2/OrderPlaced"),
                new OrderEvent(2, 1, "ORD-3", "OrderPlaced", "ORD-3/OrderPlaced"));
        assertEquals("partition 0 holds none, partition 1 holds only ORD-1, partition 2 holds ORD-2 and ORD-3 taking turns.",
                OutboxWithDebeziumDemo.describePartitions(events));
    }

    @Test
    void withoutAContainerRuntimeTheAdviceIsASentenceABeginnerCanActOn() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("./gradlew run"));
    }

    @Test
    void aPollThatNeverSucceedsGivesUpWithTheQuestionInTheMessage() {
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -> Poll.until("something that never happens", Duration.ofMillis(200), () -> false));
        assertTrue(e.getMessage().contains("something that never happens"));
    }

    @Test
    void aPollReturnsAsSoonAsTheAnswerIsYes() {
        Poll.until("an answer that is already yes", Duration.ofMillis(200), () -> true);
    }
}
