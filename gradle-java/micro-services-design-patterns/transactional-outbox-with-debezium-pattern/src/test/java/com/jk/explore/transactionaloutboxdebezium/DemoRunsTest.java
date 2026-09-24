package com.jk.explore.transactionaloutboxdebezium;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every number quoted in the README, in the slides and in the
 * narration is asserted here, so a change to the code that changes a figure fails the build
 * instead of quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstRealInfrastructureAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        String[] figures = {
            "save, then send. the process dies in between. ORD-1 in Postgres: yes. events in Kafka: 0.",
            "send, then save, and die in between. events in Kafka: 1. ORD-2 in Postgres: no.",
            "Postgres runs with wal_level logical. Debezium 3.6.3.Final runs inside this program and holds replication slot orders_outbox. slot active: yes.",
            "has no Kafka code at all. orders: 3, outbox rows: 3.",
            "Debezium reads the 3 commits from Postgres's log and sends them. events in Kafka: 3.",
            "events in Kafka: 4. events for ORD-4: 0.",
            "orders: 3. outbox rows: 0. events in Kafka: 3.",
            "Debezium is stopped. slot active: no. the checkout still takes 3 orders. orders: 3. events in Kafka: 0.",
            "log kept for the slot: grew while it was down. limit: -1, which means none.",
            "sends 3: ORD-1, ORD-2, ORD-3.",
            "dies before writing down how far it has read. events in Kafka: 2. slot active: no.",
            "sends both again. events in Kafka: 4 for 2 orders.",
            "ORD-1/OrderPlaced arrived 2 times, ORD-2/OrderPlaced arrived 2 times, with the same event id each time.",
            "9 commits, the orders taking turns. order-events has 3 partitions.",
            "ORD-1: partition 1, OrderPlaced, OrderPaid, OrderShipped.",
            "ORD-2: partition 2, OrderPlaced, OrderPaid, OrderShipped.",
            "ORD-3: partition 2, OrderPlaced, OrderPaid, OrderShipped.",
            "partition 0 holds none, partition 1 holds only ORD-1, partition 2 holds ORD-2 and ORD-3 taking turns.",
            "the bill: 2 containers, Postgres started with wal_level logical, and 1 replication slot.",
            "keeps log for ever: limit -1. retiring Debezium means dropping its slot. slot exists now: no.",
        };
        for (String figure : figures) {
            assertTrue(out.contains(figure), "missing: " + figure + "\n" + out);
        }
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            OutboxWithDebeziumDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
