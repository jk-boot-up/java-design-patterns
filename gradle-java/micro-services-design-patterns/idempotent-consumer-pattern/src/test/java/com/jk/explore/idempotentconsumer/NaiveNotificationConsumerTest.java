package com.jk.explore.idempotentconsumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The {@code HashSet} of seen ids, and every test here passes.
 *
 * The first test is the one everybody writes, and it is green. The last two are green as well,
 * and they describe a customer receiving two confirmation emails for one order. Nothing threw;
 * the suite is simply asserting what the code does.
 */
class NaiveNotificationConsumerTest {

    private CallLog log;
    private NotificationsDatabase database;
    private MessageBroker broker;
    private NaiveNotificationConsumer consumer;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        log = new CallLog(clock);
        database = new NotificationsDatabase(clock, log);
        broker = new MessageBroker(clock, log);
        consumer = new NaiveNotificationConsumer(database, log);
    }

    private static Message orderPlaced(String messageId, String orderId) {
        return new Message(messageId, "OrderPlaced", orderId, Money.pence(7095));
    }

    @Test
    @DisplayName("the duplicate is caught, which is the test everybody writes")
    void theObviousTestPasses() {
        broker.deliverTwice(orderPlaced("msg-1", "ord-1"), consumer);

        assertEquals(1, database.confirmationsQueued());
    }

    @Test
    @DisplayName("two different messages are both handled")
    void differentIdsAreBothHandled() {
        broker.deliver(orderPlaced("msg-1", "ord-2"), consumer);
        broker.deliver(orderPlaced("msg-2", "ord-3"), consumer);

        assertEquals(2, database.confirmationsQueued());
    }

    @Test
    @DisplayName("a restart empties the memory and the duplicate is handled again")
    void theMemoryLivesInTheProcess() {
        Message message = orderPlaced("msg-1", "ord-4");
        broker.deliver(message, consumer);

        consumer.restart();
        broker.deliver(message, consumer);

        // Two confirmation emails for one order, and nothing anywhere reported a problem.
        assertEquals(2, database.confirmationsQueued());
        assertEquals(0, database.handledCount());
    }

    @Test
    @DisplayName("a crash between the work and the record loses the id and keeps the effect")
    void theGapIsTheProblem() {
        Message message = orderPlaced("msg-1", "ord-5");
        consumer.dieAfterQueueing();

        assertThrows(ProcessDiedException.class, () -> broker.deliver(message, consumer));
        assertEquals(1, database.confirmationsQueued());

        consumer.restart();
        broker.deliver(message, consumer);

        assertEquals(2, database.confirmationsQueued());
    }
}
