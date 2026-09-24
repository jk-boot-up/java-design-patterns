package com.jk.explore.pubsubredis;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What the real Redis server does, asked of it directly.
 *
 * <p>One server is started for the whole class, because starting it is the slow part. Every
 * wait here is a bounded poll on something that can actually be asked; there is no sleep
 * anywhere in this file.
 */
class RealRedisTest {

    private static RedisServer server;

    @BeforeAll
    static void startRedis() {
        assumeTrue(RedisServer.containerRuntimeAvailable(), "needs a container runtime");
        server = new RedisServer();
        server.start();
    }

    @AfterAll
    static void stopRedis() {
        if (server != null) {
            server.close();
        }
    }

    @Test
    void publishingAnswersWithHowManyListenersWereHandedTheMessage() {
        try (OrderService orders = new OrderService(server);
             Subscriber inventory = Subscriber.listen(server, "inventory", OrderService.PLACED);
             Subscriber email = Subscriber.listen(server, "email", OrderService.PLACED)) {
            assertEquals(2, server.listenersOn(OrderService.PLACED));
            assertEquals(2, orders.publish(OrderEvent.placed(1)));
            Poll.until("both to hear it", () -> inventory.count() == 1 && email.count() == 1);
            assertEquals(List.of("OrderPlaced ORD-1"), inventory.received());
            assertEquals(List.of("OrderPlaced ORD-1"), email.received());
        }
    }

    @Test
    void aMessageNobodyIsListeningForIsGoneForGood() {
        try (OrderService orders = new OrderService(server)) {
            assertEquals(0, orders.publish(OrderEvent.placed(1)));
            try (Subscriber late = Subscriber.listen(server, "late", OrderService.PLACED)) {
                assertEquals(1, orders.publish(OrderEvent.placed(2)));
                Poll.until("the late subscriber to hear ORD-2", () -> late.count() == 1);
                assertEquals(List.of("ORD-2"), late.orders());
            }
            assertEquals(0, server.keysStored());
        }
    }

    @Test
    void aStarInTheNameMatchesEveryChannelThatFits() {
        try (OrderService orders = new OrderService(server);
             Subscriber analytics = Subscriber.listenToPattern(server, "analytics", "orders.*")) {
            assertEquals(1, orders.publish(OrderEvent.placed(1)));
            assertEquals(1, orders.publish(OrderEvent.cancelled(1)));
            Poll.until("analytics to hear both", () -> analytics.count() == 2);
            assertEquals(List.of("OrderPlaced ORD-1", "OrderCancelled ORD-1"), analytics.received());
        }
    }

    @Test
    void aSubscriberInAnotherProcessIsHandedTheSameMessage() {
        try (OrderService orders = new OrderService(server);
             SeparateProcess loyalty = new SeparateProcess(server, 1)) {
            assertTrue(loyalty.isSeparate(), "loyalty runs in its own process");
            assertEquals(1, orders.publish(OrderEvent.placed(9)));
            assertEquals(0, loyalty.awaitExit());
            assertEquals(List.of("ORD-9"), loyalty.ordersReceived());
        }
    }

    /**
     * The headline. A listener that stops reading is not waited for; once its pile of unsent
     * messages passes the limit, Redis closes its connection. How many orders that takes
     * depends on how much the network between here and the container holds, so it is a range.
     */
    @Test
    void aListenerThatFallsTooFarBehindIsCutOffAndLosesWhatWasWaiting() {
        server.limitEachListenerTo("1mb");
        server.resetCounts();
        try (OrderService orders = new OrderService(server);
             Subscriber fast = Subscriber.listen(server, "fast", OrderService.PLACED);
             Subscriber stalled = Subscriber.listen(server, "stalled", OrderService.PLACED)) {
            stalled.stopReading();
            List<Long> reached = new ArrayList<>();
            int rounds = 0;
            while (server.listenersCutOff() == 0 && rounds++ < RedisPubSubDemo.MAX_ROUNDS) {
                reached.addAll(orders.publishPlaced(reached.size() + 1, RedisPubSubDemo.ROUND));
            }
            assertEquals(1, server.listenersCutOff());
            assertEquals(2, reached.get(0));
            assertEquals(1, reached.get(reached.size() - 1));
            assertTrue(reached.size() > 10_000, "1mb of orders is well over 10,000 of them");

            int published = reached.size();
            Poll.until("the fast listener to hear every order", () -> fast.count() == published);
            assertTrue(!fast.wasCutOff());

            stalled.startReading();
            Poll.until("the stalled listener to reach the end of what it was sent", stalled::finished);
            assertTrue(stalled.wasCutOff(), "Redis closed the connection from its side");
            assertTrue(stalled.count() < published, "some orders were thrown away with the connection");
            assertEquals(1, server.listenersOn(OrderService.PLACED), "only the fast listener is left");
        }
    }
}
