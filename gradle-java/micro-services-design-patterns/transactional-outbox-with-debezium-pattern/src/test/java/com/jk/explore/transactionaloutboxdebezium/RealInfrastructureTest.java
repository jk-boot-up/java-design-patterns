package com.jk.explore.transactionaloutboxdebezium;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * What Postgres, Debezium and Kafka do, asked of them directly.
 *
 * <p>One database, one broker and one Debezium engine are started for the whole class,
 * because starting them is the slow part, and all of it is removed at the end. Each test
 * empties the tables and reads Kafka only from a mark taken at its start. Every wait is a
 * bounded poll on something the tools can be asked about; there is no sleep in this file.
 */
class RealInfrastructureTest {

    private static OrdersDatabase database;
    private static Broker broker;
    private static ChangeDataCapture cdc;

    @BeforeAll
    static void startAll() {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        database = new OrdersDatabase();
        broker = new Broker();
        database.start();
        broker.start();
        cdc = new ChangeDataCapture(database, broker);
        cdc.start();
    }

    @AfterAll
    static void stopAll() {
        if (cdc != null) {
            cdc.close();
        }
        if (broker != null) {
            broker.close();
        }
        if (database != null) {
            database.close();
        }
    }

    @BeforeEach
    void clean() {
        if (!cdc.running()) {
            cdc.start();
        }
        database.empty();
    }

    @Test
    void postgresRunsWithLogicalDecodingAndDebeziumHoldsItsSlot() {
        assertEquals("logical", database.walLevel());
        assertTrue(database.slotActive(ChangeDataCapture.SLOT));
    }

    @Test
    void aDualWriteThatDiesAfterTheSaveLeavesAnOrderAndNoEvent() {
        Map<Integer, Long> mark = broker.mark();
        try (DualWriteCheckout checkout = new DualWriteCheckout(database, broker)) {
            assertThrows(ProcessDied.class, () -> checkout.saveThenSend(Order.number(1), true));
        }
        assertTrue(database.hasOrder("ORD-1"));
        assertEquals(0, broker.countSince(mark));
    }

    @Test
    void aDualWriteThatDiesAfterTheSendLeavesAnEventAndNoOrder() {
        Map<Integer, Long> mark = broker.mark();
        try (DualWriteCheckout checkout = new DualWriteCheckout(database, broker)) {
            assertThrows(ProcessDied.class, () -> checkout.sendThenSave(Order.number(2), true));
        }
        assertFalse(database.hasOrder("ORD-2"));
        assertEquals(1, broker.countSince(mark));
    }

    @Test
    void debeziumPublishesEveryCommittedOutboxRowKeyedByTheOrder() {
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        broker.waitFor(3, mark, "3 events");
        List<OrderEvent> events = broker.readSince(mark);
        assertEquals(3, events.size());
        assertEquals(List.of("ORD-1", "ORD-2", "ORD-3"), events.stream().map(OrderEvent::orderId).sorted().toList());
        assertTrue(events.stream().allMatch(e -> e.type().equals("OrderPlaced")));
        assertTrue(events.stream().allMatch(e -> e.eventId().equals(e.orderId() + "/OrderPlaced")));
    }

    @Test
    void aRolledBackCheckoutPublishesNothing() {
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        checkout.placeButCardDeclined(Order.number(4));
        // The log is read in commit order, so once a later commit has arrived, an earlier one would have too.
        checkout.place(Order.number(5));
        broker.waitFor(1, mark, "the event after the declined order");
        List<OrderEvent> events = broker.readSince(mark);
        assertEquals(List.of("ORD-5"), events.stream().map(OrderEvent::orderId).toList());
        assertFalse(database.hasOrder("ORD-4"));
    }

    @Test
    void aRowDeletedInTheSameTransactionIsStillPublished() {
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database, true);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        broker.waitFor(3, mark, "3 events from rows that no longer exist");
        assertEquals(0, database.outboxRows());
        assertEquals(3, database.orders());
        assertEquals(3, broker.readSince(mark).size());
    }

    @Test
    void whileDebeziumIsDownTheSlotKeepsTheLogAndNothingIsLost() {
        cdc.stop();
        assertFalse(database.slotActive(ChangeDataCapture.SLOT));
        long before = database.logHeldForSlot(ChangeDataCapture.SLOT);
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        assertEquals(3, database.orders());
        assertEquals(0, broker.countSince(mark));
        assertTrue(database.logHeldForSlot(ChangeDataCapture.SLOT) > before);
        assertEquals("-1", database.slotLogLimit());
        cdc.start();
        broker.waitFor(3, mark, "Debezium to catch up");
        assertEquals(3, broker.readSince(mark).size());
    }

    @Test
    void aCrashAfterSendingAndBeforeWritingDownSendsTheSameEventsAgain() {
        Map<Integer, Long> mark = broker.mark();
        cdc.crashAfterSending(2);
        OutboxCheckout checkout = new OutboxCheckout(database);
        checkout.place(Order.number(1));
        checkout.place(Order.number(2));
        cdc.awaitCrash();
        assertEquals(2, broker.countSince(mark));
        cdc.start();
        broker.waitFor(4, mark, "the same events again");
        List<OrderEvent> events = broker.readSince(mark);
        assertEquals(4, events.size());
        assertEquals(2, events.stream().filter(e -> e.eventId().equals("ORD-1/OrderPlaced")).count());
        assertEquals(2, events.stream().filter(e -> e.eventId().equals("ORD-2/OrderPlaced")).count());
    }

    @Test
    void anOrdersEventsShareOnePartitionAndKeepTheirCommitOrder() {
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        for (String[] step : new String[][]{{"paid", "OrderPaid"}, {"shipped", "OrderShipped"}}) {
            for (int i = 1; i <= 3; i++) {
                checkout.moveOn("ORD-" + i, step[0], step[1]);
            }
        }
        broker.waitFor(9, mark, "9 events");
        List<OrderEvent> events = broker.readSince(mark);
        for (int i = 1; i <= 3; i++) {
            String id = "ORD-" + i;
            List<OrderEvent> mine = events.stream().filter(e -> e.orderId().equals(id)).toList();
            assertEquals(1, mine.stream().map(OrderEvent::partition).distinct().count(), id + " is on one partition");
            assertEquals(List.of("OrderPlaced", "OrderPaid", "OrderShipped"), mine.stream().map(OrderEvent::type).toList());
        }
    }
}
