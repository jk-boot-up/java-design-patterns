package com.jk.explore.eventbusnats;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * Nothing here sleeps. Every wait is a bounded wait on a real condition, and it fails rather than hangs.
 *
 * <p>The hard one is proving that a subscriber missed an event, because that is proving a negative. It is
 * done by proving a positive instead: subscribe, publish, and check that the very first event received is
 * the second one. NATS delivers one name in the order it was published, so the first order cannot still be
 * on its way once the second has arrived.
 */
class EventBusNatsTest {

    private static NatsServer server;

    @BeforeAll
    static void startTheBus() {
        assumeTrue(NatsServer.containerRuntimeAvailable(), "needs a container runtime");
        server = new NatsServer();
        server.start();
    }

    @AfterAll
    static void stopTheBus() {
        if (server != null) {
            server.close();
        }
    }

    @Test
    void wiringEveryServiceToEveryOtherCostsTwentyWiresForFive() {
        DirectStore store = new DirectStore(5);
        assertEquals(20, store.wires());
        assertEquals(10, store.wiresForOneMoreService());
        assertEquals(5, store.wiresThroughABus());
    }

    @Test
    void everyListenerOnTheSameNameGetsTheSameEvent() throws Exception {
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus email = new StoreBus("email", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url())) {
            StoreSubscriber toEmail = email.subscribe("email", EventBusNatsDemo.ORDER_PLACED);
            StoreSubscriber toWarehouse = warehouse.subscribe("warehouse", EventBusNatsDemo.ORDER_PLACED);

            checkout.publish(EventBusNatsDemo.ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.settle();

            assertEquals("OrderPlaced ORD-1", toEmail.waitForNext());
            assertEquals("OrderPlaced ORD-1", toWarehouse.waitForNext());
        }
    }

    @Test
    void aStarMatchesOneWordAndAnArrowMatchesTheRest() throws Exception {
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus listeners = new StoreBus("listeners", server.url())) {
            StoreSubscriber placed = listeners.subscribe("email", EventBusNatsDemo.ORDER_PLACED);
            StoreSubscriber orderEvents = listeners.subscribe("warehouse", EventBusNatsDemo.ALL_ORDER_EVENTS);
            StoreSubscriber allOfIt = listeners.subscribe("analytics", EventBusNatsDemo.EVERYTHING);

            checkout.publish(EventBusNatsDemo.ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.publish(EventBusNatsDemo.ORDER_CANCELLED, "OrderCancelled ORD-1");
            checkout.publish(EventBusNatsDemo.PAYMENT_TAKEN, "PaymentTaken ORD-1");
            checkout.publish(EventBusNatsDemo.STOCK_LOW, "StockLow SKU-42");
            checkout.settle();

            placed.waitFor(1);
            orderEvents.waitFor(2);
            allOfIt.waitFor(4);

            assertEquals(List.of("OrderPlaced ORD-1"), placed.events());
            assertEquals(List.of("OrderPlaced ORD-1", "OrderCancelled ORD-1"), orderEvents.events());
            assertEquals(4, allOfIt.received());
        }
    }

    @Test
    void aSubscriberThatIsNotListeningYetMissesTheEventOutright() throws Exception {
        try (StoreBus checkout = new StoreBus("checkout", server.url());
             StoreBus warehouse = new StoreBus("warehouse", server.url())) {
            checkout.publish(EventBusNatsDemo.ORDER_PLACED, "OrderPlaced ORD-1");
            checkout.settle();

            StoreSubscriber late = warehouse.subscribe("warehouse", EventBusNatsDemo.ORDER_PLACED);
            checkout.publish(EventBusNatsDemo.ORDER_PLACED, "OrderPlaced ORD-2");
            checkout.settle();

            // The positive fact: the first event this listener ever receives is the second one published.
            // Delivery on one name is ordered, so the first order was never going to arrive.
            assertEquals("OrderPlaced ORD-2", late.waitForNext());
            assertEquals(1, late.received());
        }
    }

    @Test
    void askingOnANameNobodyIsListeningToFailsAtOnce() throws Exception {
        try (StoreBus checkout = new StoreBus("checkout", server.url())) {
            assertEquals("no responders", checkout.ask("store.orders.nobody.listens", "anyone there?"));
        }
    }

    @Test
    void onlyTheServerKnowsHowManyListenersThereAre() throws Exception {
        ServerView view = new ServerView(server.monitorUrl(), "store.");
        view.waitUntilStoreListeners(n -> n == 0);
        try (StoreBus email = new StoreBus("email", server.url());
             StoreBus analytics = new StoreBus("analytics", server.url())) {
            email.subscribe("email", EventBusNatsDemo.ORDER_PLACED);
            StoreSubscriber tally = analytics.subscribe("analytics", EventBusNatsDemo.EVERYTHING);
            assertEquals(2, view.waitUntilStoreListeners(n -> n == 2));

            tally.stopListening();
            analytics.settle();
            assertEquals(1, view.waitUntilStoreListeners(n -> n == 1));
        }
        assertEquals(0, view.waitUntilStoreListeners(n -> n == 0));
    }

    @Test
    void aListenerThatIsKeptWaitingFailsInsteadOfHanging() throws Exception {
        try (StoreBus warehouse = new StoreBus("warehouse", server.url())) {
            StoreSubscriber quiet = warehouse.subscribe("warehouse", "store.orders.never.published");
            // Nothing is ever published here, so the wait must end in a clear failure, not a hang.
            IllegalStateException failure = assertThrows(IllegalStateException.class,
                    () -> quiet.waitForNext(java.time.Duration.ofSeconds(2)));
            assertTrue(failure.getMessage().contains("nothing arrived"), failure.getMessage());
        }
    }
}
