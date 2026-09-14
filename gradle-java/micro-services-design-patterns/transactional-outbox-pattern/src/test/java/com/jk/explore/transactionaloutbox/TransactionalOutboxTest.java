package com.jk.explore.transactionaloutbox;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The out-tray: what it guarantees, and what it charges for the guarantee. */
class TransactionalOutboxTest {

    private CallLog log;
    private OrderDatabase database;
    private MessageBroker broker;
    private NotificationService notifications;
    private OrderService orders;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        log = new CallLog(clock);
        database = new OrderDatabase(log);
        broker = new MessageBroker(clock, log);
        notifications = new NotificationService(log);
        broker.subscribe(notifications::on);
        orders = new OrderService(database, log);
    }

    private OutboxRelay relay() {
        return new OutboxRelay(database, broker, log);
    }

    private static Order order(String orderId) {
        return new Order(orderId, "cust-7", Money.pence(7095));
    }

    @Test
    @DisplayName("placing an order writes the order and the message, and calls nobody")
    void theServiceNeverTalksToTheBroker() {
        orders.placeOrder(order("ord-1"));

        assertEquals(1, database.orderCount());
        assertEquals(1, database.unsent().size());
        assertEquals(0, broker.deliveredCount());
        assertEquals(0, log.countFor("Broker"));
    }

    @Test
    @DisplayName("the relay publishes what is waiting and marks it sent")
    void theSweepDeliversIt() {
        orders.placeOrder(order("ord-2"));

        assertEquals(1, relay().sweep());
        assertEquals(1, broker.deliveredCount());
        assertEquals(0, database.unsent().size());
        assertEquals(1, notifications.emailsSent());
    }

    @Test
    @DisplayName("a second sweep with an empty out-tray sends nothing")
    void aSweepIsNotAResend() {
        orders.placeOrder(order("ord-3"));
        relay().sweep();

        assertEquals(0, relay().sweep());
        assertEquals(1, broker.deliveredCount());
    }

    @Test
    @DisplayName("a crash before the commit leaves no order and no message")
    void bothOrNeither() {
        orders.dieBeforeCommitting();

        assertThrows(ProcessDiedException.class, () -> orders.placeOrder(order("ord-4")));

        assertEquals(0, database.orderCount());
        assertEquals(0, database.outboxSize());
        assertNull(database.find("ord-4"));
    }

    @Test
    @DisplayName("a crash after the commit still leaves the message to be found")
    void theMessageOutlivesTheProcess() {
        orders.placeOrder(order("ord-5"));
        // The process now dies. Nothing is running. A new one starts and sweeps.

        assertEquals(1, relay().sweep());
        assertEquals(1, notifications.emailsSent());
    }

    @Test
    @DisplayName("checkout works while the broker is down")
    void checkoutDoesNotDependOnTheBroker() {
        broker.failNext(5);

        orders.placeOrder(order("ord-6"));
        orders.placeOrder(order("ord-7"));

        assertEquals(2, database.orderCount());
        assertEquals(2, database.unsent().size());
    }

    @Test
    @DisplayName("a message the broker refused stays in the out-tray and goes out later")
    void nothingIsLostWhenTheBrokerIsDown() {
        orders.placeOrder(order("ord-8"));
        broker.failNext(1);

        assertEquals(0, relay().sweep());
        assertEquals(1, database.unsent().size());

        // Broker back. Nobody wrote any retry logic; the next sweep simply finds it again.
        assertEquals(1, relay().sweep());
        assertEquals(1, notifications.emailsSent());
    }

    @Test
    @DisplayName("two orders, two messages, both delivered on one sweep")
    void theTrayIsCollectedInOrder() {
        orders.placeOrder(order("ord-9"));
        orders.placeOrder(order("ord-10"));

        assertEquals(2, relay().sweep());
        assertEquals("ord-9", broker.delivered().get(0).orderId());
        assertEquals("ord-10", broker.delivered().get(1).orderId());
    }

    @Test
    @DisplayName("the honest cost: a crash after publishing sends the message twice")
    void deliveryIsAtLeastOnce() {
        orders.placeOrder(order("ord-11"));
        OutboxRelay relay = relay();
        relay.dieAfterPublishing();

        assertThrows(ProcessDiedException.class, relay::sweep);
        assertEquals(1, broker.deliveredCount());
        // As far as the table is concerned the message never went.
        assertEquals(1, database.unsent().size());

        relay.restart();
        relay.sweep();

        assertEquals(2, broker.timesDelivered("msg-1"));
        assertEquals(2, notifications.emailsSent());
    }

    @Test
    @DisplayName("a duplicate carries the same message id both times")
    void theDuplicateIsRecognisable() {
        orders.placeOrder(order("ord-12"));
        OutboxRelay relay = relay();
        relay.dieAfterPublishing();
        relay.sweepAndSurvive();
        relay.restart();
        relay.sweep();

        assertEquals(2, broker.deliveredCount());
        assertEquals(broker.delivered().get(0).messageId(),
                broker.delivered().get(1).messageId());
    }

    @Test
    @DisplayName("a committed transaction cannot be committed again")
    void oneCommitOnly() {
        OrderDatabase.Transaction transaction = database.begin();
        transaction.save(order("ord-13"));
        transaction.commit();

        assertThrows(IllegalStateException.class, transaction::commit);
    }

    @Test
    @DisplayName("nothing a transaction holds is visible before it commits")
    void writesAreHeldUntilTheCommit() {
        OrderDatabase.Transaction transaction = database.begin();
        transaction.save(order("ord-14"));
        transaction.save(new OutboxMessage("msg-99", "OrderPlaced", "ord-14",
                Money.pence(100)));

        assertEquals(0, database.orderCount());
        assertEquals(0, database.outboxSize());

        transaction.commit();

        assertEquals(1, database.orderCount());
        assertEquals(1, database.outboxSize());
    }

    @Test
    @DisplayName("the commit is one line in the timeline, covering both rows")
    void theTimelineShowsOneCommit() {
        orders.placeOrder(order("ord-15"));

        assertEquals(1, log.countFor("OrderDb"));
        assertTrue(log.timeline().contains("1 order(s) and 1 outbox message(s) together"),
                log.timeline());
    }
}
