package com.jk.explore.idempotentconsumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** Dedupe by id, recorded in the same transaction as the effect. */
class IdempotentConsumerTest {

    private SimulatedClock clock;
    private CallLog log;
    private NotificationsDatabase database;
    private MessageBroker broker;
    private IdempotentNotificationConsumer consumer;

    @BeforeEach
    void setUp() {
        clock = new SimulatedClock();
        log = new CallLog(clock);
        database = new NotificationsDatabase(clock, log);
        broker = new MessageBroker(clock, log);
        consumer = new IdempotentNotificationConsumer(database, log);
    }

    private static Message orderPlaced(String messageId, String orderId) {
        return new Message(messageId, "OrderPlaced", orderId, Money.pence(7095));
    }

    @Test
    @DisplayName("one delivery queues one confirmation")
    void theFirstDeliveryIsHandled() {
        broker.deliver(orderPlaced("msg-1", "ord-1"), consumer);

        assertEquals(1, database.confirmationsQueued());
        assertTrue(database.hasHandled("msg-1"));
    }

    @Test
    @DisplayName("the same message twice queues one confirmation")
    void theDuplicateIsIgnored() {
        broker.deliverTwice(orderPlaced("msg-1", "ord-2"), consumer);

        assertEquals(1, database.confirmationsQueued());
        assertEquals(1, database.handledCount());
    }

    @Test
    @DisplayName("two different messages are two different orders, not duplicates")
    void differentIdsAreBothHandled() {
        broker.deliver(orderPlaced("msg-1", "ord-3"), consumer);
        broker.deliver(orderPlaced("msg-2", "ord-4"), consumer);

        assertEquals(2, database.confirmationsQueued());
    }

    @Test
    @DisplayName("a restart does not lose the memory, because it was never in memory")
    void theStoreOutlivesTheProcess() {
        Message message = orderPlaced("msg-1", "ord-5");
        broker.deliver(message, consumer);

        consumer.restart();
        broker.deliver(message, consumer);

        assertEquals(1, database.confirmationsQueued());
    }

    @Test
    @DisplayName("a crash before the commit writes neither the effect nor the id")
    void bothOrNeither() {
        consumer.dieBeforeCommitting();

        assertThrows(ProcessDiedException.class,
                () -> broker.deliver(orderPlaced("msg-1", "ord-6"), consumer));

        assertEquals(0, database.confirmationsQueued());
        assertFalse(database.hasHandled("msg-1"));
    }

    @Test
    @DisplayName("after that crash the redelivery handles it exactly once")
    void exactlyOnceOutOfAtLeastOnce() {
        Message message = orderPlaced("msg-1", "ord-7");
        consumer.dieBeforeCommitting();
        assertThrows(ProcessDiedException.class, () -> broker.deliver(message, consumer));

        consumer.restart();
        broker.deliver(message, consumer);
        broker.deliver(message, consumer);

        assertEquals(1, database.confirmationsQueued());
    }

    @Test
    @DisplayName("the ignored delivery costs nothing but the trip")
    void ignoringIsCheap() {
        Message message = orderPlaced("msg-1", "ord-8");
        broker.deliver(message, consumer);
        long commitsAfterOne = log.countFor("NotifDb");

        broker.deliver(message, consumer);

        assertEquals(commitsAfterOne, log.countFor("NotifDb"));
        assertTrue(log.timeline().contains("IGNORED"), log.timeline());
    }

    @Test
    @DisplayName("the effect and the id land in one commit")
    void oneCommitCoversBoth() {
        broker.deliver(orderPlaced("msg-1", "ord-9"), consumer);

        assertEquals(1, log.countFor("NotifDb"));
        assertTrue(log.timeline().contains("1 confirmation(s) and 1 handled id(s) together"),
                log.timeline());
    }

    @Test
    @DisplayName("the honest cost: a duplicate that arrives after the id expires is handled again")
    void theWindowIsAGuess() {
        Message message = orderPlaced("msg-1", "ord-10");
        broker.deliver(message, consumer);

        clock.advance(60_000);
        database.forgetHandledOlderThan(30_000);

        assertFalse(database.hasHandled("msg-1"));
        broker.deliver(message, consumer);
        assertEquals(2, database.confirmationsQueued());
    }

    @Test
    @DisplayName("expiry keeps the ids that are still inside the window")
    void expiryOnlyForgetsOldIds() {
        broker.deliver(orderPlaced("msg-1", "ord-11"), consumer);
        clock.advance(60_000);
        broker.deliver(orderPlaced("msg-2", "ord-12"), consumer);

        database.forgetHandledOlderThan(30_000);

        assertFalse(database.hasHandled("msg-1"));
        assertTrue(database.hasHandled("msg-2"));
    }

    @Test
    @DisplayName("nothing a transaction holds is visible before it commits")
    void writesAreHeldUntilTheCommit() {
        NotificationsDatabase.Transaction transaction = database.begin();
        transaction.queueConfirmation("hello");
        transaction.recordHandled("msg-99");

        assertEquals(0, database.confirmationsQueued());
        assertFalse(database.hasHandled("msg-99"));

        transaction.commit();

        assertEquals(1, database.confirmationsQueued());
        assertTrue(database.hasHandled("msg-99"));
    }

    @Test
    @DisplayName("a naturally idempotent handler needs no store at all")
    void settingAStatusTwiceSetsTheSameStatus() {
        ShipmentStatusConsumer shipping = new ShipmentStatusConsumer(log);

        broker.deliverTwice(new Message("msg-3", "OrderShipped", "ord-13",
                Money.pence(7095)), shipping);

        assertEquals("SHIPPED", shipping.statusOf("ord-13"));
        assertEquals(1, shipping.ordersKnown());
    }

    @Test
    @DisplayName("adding to a total is not naturally idempotent")
    void addingTwiceDoublesIt() {
        LoyaltyPointsConsumer loyalty = new LoyaltyPointsConsumer(log);
        Message message = orderPlaced("msg-4", "ord-14");

        broker.deliverTwice(message, loyalty);

        assertEquals(140, loyalty.runningTotal());
    }

    @Test
    @DisplayName("rewriting it as a per-order assignment makes it idempotent with no store")
    void theRewriteBeatsTheStore() {
        LoyaltyPointsConsumer loyalty = new LoyaltyPointsConsumer(log);
        Message message = orderPlaced("msg-4", "ord-15");

        loyalty.awardForOrder(message);
        loyalty.awardForOrder(message);

        assertEquals(70, loyalty.pointsAwarded());
    }
}
