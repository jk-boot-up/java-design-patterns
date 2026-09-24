package com.jk.explore.pubsubredis;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The parts that need no Redis at all. */
class PlainPartsTest {

    @Test
    void anOrderEventSurvivesTheTripThroughText() {
        OrderEvent sent = OrderEvent.cancelled(7);
        OrderEvent arrived = OrderEvent.read(sent.text());
        assertEquals("OrderCancelled", arrived.kind());
        assertEquals("ORD-7", arrived.orderId());
        assertEquals(OrderService.CANCELLED, arrived.channel());
    }

    @Test
    void aPlacedOrderIsPublishedUnderItsOwnChannelName() {
        assertEquals("orders.placed", OrderEvent.placed(1).channel());
        assertEquals("OrderPlaced ORD-1", OrderEvent.placed(1).text());
    }

    @Test
    void theDirectVersionCallsEveryServiceItKnowsByName() {
        DirectOrderService direct = new DirectOrderService();
        direct.placeOrder(OrderEvent.placed(1));
        assertEquals(3, direct.servicesKnownByName());
        assertEquals(List.of("ORD-1"), direct.handledBy("inventory"));
        assertEquals(List.of("ORD-1"), direct.handledBy("email"));
        assertEquals(List.of("ORD-1"), direct.handledBy("analytics"));
    }

    @Test
    void theFifthActDescribesCountsThatDependOnTheMachineInWords() {
        assertEquals("none of them", RedisPubSubDemo.describe(0, 5000));
        assertEquals("some of them, not all", RedisPubSubDemo.describe(4000, 5000));
        assertEquals("all of them", RedisPubSubDemo.describe(5000, 5000));
        assertEquals("more than 10,000 orders", RedisPubSubDemo.describePublished(107_000));
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
        assertTrue(RedisServer.NO_RUNTIME_ADVICE.contains("container runtime"), RedisServer.NO_RUNTIME_ADVICE);
        assertTrue(RedisServer.NO_RUNTIME_ADVICE.contains("./gradlew run again"), RedisServer.NO_RUNTIME_ADVICE);
    }
}
