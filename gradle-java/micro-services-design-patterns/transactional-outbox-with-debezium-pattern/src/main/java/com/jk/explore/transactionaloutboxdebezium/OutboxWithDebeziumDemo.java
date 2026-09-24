package com.jk.explore.transactionaloutboxdebezium;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Six acts against a real Postgres database and a real Kafka broker, both started and
 * stopped by this program, with Debezium reading Postgres's log in between.
 *
 * <p>The Orders service saves each order in Postgres, and the rest of the shop has to hear
 * about it through Kafka. The acts show why doing both by hand goes wrong, how the outbox
 * and change data capture put it right, and what change data capture brings with it that a
 * simulation cannot show.
 */
public class OutboxWithDebeziumDemo {

    public static void main(String[] args) {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        try (OrdersDatabase database = new OrdersDatabase(); Broker broker = new Broker()) {
            try {
                database.start();
                broker.start();
            } catch (RuntimeException e) {
                System.out.println(Broker.WOULD_NOT_START_ADVICE);
                return;
            }
            one(database, broker);
            try (ChangeDataCapture cdc = new ChangeDataCapture(database, broker)) {
                two(database, broker, cdc);
                three(database, broker, cdc);
                four(database, broker, cdc);
                five(database, broker, cdc);
                six(database, broker, cdc);
            }
        }
    }

    /** Save then send, and send then save, each with a crash in between. */
    static void one(OrdersDatabase database, Broker broker) {
        System.out.println("ONE. Two writes, one crash.");
        database.empty();
        Map<Integer, Long> mark = broker.mark();
        System.out.println("  Postgres and Kafka are running in containers. no Debezium yet: the checkout talks to both itself.");
        try (DualWriteCheckout checkout = new DualWriteCheckout(database, broker)) {
            try {
                checkout.saveThenSend(Order.number(1), true);
            } catch (ProcessDied died) {
                // in real life nothing catches this; the process is gone
            }
            System.out.println("  save, then send. the process dies in between. ORD-1 in Postgres: " + yesNo(database.hasOrder("ORD-1"))
                    + ". events in Kafka: " + broker.countSince(mark) + ". the customer is charged and nobody is told.");
            try {
                checkout.sendThenSave(Order.number(2), true);
            } catch (ProcessDied died) {
                // in real life nothing catches this; the process is gone
            }
            System.out.println("  swap the lines: send, then save, and die in between. events in Kafka: " + broker.countSince(mark)
                    + ". ORD-2 in Postgres: " + yesNo(database.hasOrder("ORD-2")) + ". the shop announced an order that does not exist.");
        }
        System.out.println("  two systems, two steps, and no transaction that covers both.");
    }

    /** The outbox: one transaction, and Debezium does the sending. */
    static void two(OrdersDatabase database, Broker broker, ChangeDataCapture cdc) {
        System.out.println("TWO. One transaction, and Debezium sends.");
        database.empty();
        cdc.start();
        System.out.println("  Postgres runs with wal_level " + database.walLevel() + ". Debezium " + ChangeDataCapture.DEBEZIUM_VERSION
                + " runs inside this program and holds replication slot " + ChangeDataCapture.SLOT + ". slot active: " + yesNo(database.slotActive(ChangeDataCapture.SLOT)) + ".");
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        broker.waitFor(3, mark, "3 events from Debezium");
        System.out.println("  the checkout writes each order and an outbox row in one transaction, and has no Kafka code at all. orders: "
                + database.orders() + ", outbox rows: " + database.outboxRows() + ".");
        System.out.println("  Debezium reads the 3 commits from Postgres's log and sends them. events in Kafka: " + broker.countSince(mark) + ".");
        checkout.placeButCardDeclined(Order.number(4));
        checkout.place(Order.number(5));
        broker.waitFor(4, mark, "the event after the declined order");
        List<OrderEvent> events = broker.readSince(mark);
        long declined = events.stream().filter(e -> e.orderId().equals("ORD-4")).count();
        System.out.println("  ORD-4 writes both rows, the card is declined, and the transaction rolls back. then ORD-5 commits.");
        System.out.println("  events in Kafka: " + events.size() + ". events for ORD-4: " + declined
                + ". the log only hands over committed work, so the order and its event live or die together.");
    }

    /** Debezium reads the log, not the table, so the row can be deleted as soon as it is written. */
    static void three(OrdersDatabase database, Broker broker, ChangeDataCapture cdc) {
        System.out.println("THREE. The log, not the table.");
        database.empty();
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database, true);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        broker.waitFor(3, mark, "3 events from Debezium");
        System.out.println("  this time each transaction writes the outbox row and deletes it again before committing.");
        System.out.println("  orders: " + database.orders() + ". outbox rows: " + database.outboxRows() + ". events in Kafka: " + broker.countSince(mark) + ".");
        System.out.println("  a relay that reads the table would find nothing to send. Debezium read the insert from the log.");
    }

    /** The connector is down: checkout carries on, and the slot keeps the log. */
    static void four(OrdersDatabase database, Broker broker, ChangeDataCapture cdc) {
        System.out.println("FOUR. Debezium is down.");
        database.empty();
        cdc.stop();
        long heldBefore = database.logHeldForSlot(ChangeDataCapture.SLOT);
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        long heldAfter = database.logHeldForSlot(ChangeDataCapture.SLOT);
        System.out.println("  Debezium is stopped. slot active: " + yesNo(database.slotActive(ChangeDataCapture.SLOT))
                + ". the checkout still takes 3 orders. orders: " + database.orders() + ". events in Kafka: " + broker.countSince(mark) + ".");
        System.out.println("  the slot makes Postgres keep every part of the log Debezium has not confirmed. log kept for the slot: "
                + (heldAfter > heldBefore ? "grew while it was down" : "did not grow") + ". limit: " + database.slotLogLimit() + ", which means none.");
        cdc.start();
        broker.waitFor(3, mark, "Debezium to catch up");
        List<OrderEvent> events = broker.readSince(mark);
        System.out.println("  Debezium starts again, carries on from its slot, and sends " + events.size() + ": "
                + events.stream().map(OrderEvent::orderId).sorted().collect(Collectors.joining(", ")) + ". nothing was lost and nobody wrote a retry.");
    }

    /** A crash between sending and writing down the position: the same events go out again. */
    static void five(OrdersDatabase database, Broker broker, ChangeDataCapture cdc) {
        System.out.println("FIVE. Sent, but not written down.");
        database.empty();
        Map<Integer, Long> mark = broker.mark();
        cdc.crashAfterSending(2);
        OutboxCheckout checkout = new OutboxCheckout(database);
        checkout.place(Order.number(1));
        checkout.place(Order.number(2));
        cdc.awaitCrash();
        System.out.println("  Debezium sends ORD-1 and ORD-2 to Kafka, then dies before writing down how far it has read. events in Kafka: "
                + broker.countSince(mark) + ". slot active: " + yesNo(database.slotActive(ChangeDataCapture.SLOT)) + ".");
        cdc.start();
        broker.waitFor(4, mark, "Debezium to send again");
        List<OrderEvent> events = broker.readSince(mark);
        Map<String, Long> byId = new LinkedHashMap<>();
        events.forEach(e -> byId.merge(e.eventId(), 1L, Long::sum));
        System.out.println("  it starts again from the last place it wrote down, and sends both again. events in Kafka: " + events.size() + " for 2 orders.");
        System.out.println("  " + byId.entrySet().stream().map(e -> e.getKey() + " arrived " + e.getValue() + " times").collect(Collectors.joining(", "))
                + ", with the same event id each time. delivery is at least once.");
    }

    /** One key, one partition, one order. */
    static void six(OrdersDatabase database, Broker broker, ChangeDataCapture cdc) {
        System.out.println("SIX. Order per key, and the bill.");
        database.empty();
        Map<Integer, Long> mark = broker.mark();
        OutboxCheckout checkout = new OutboxCheckout(database);
        for (int i = 1; i <= 3; i++) {
            checkout.place(Order.number(i));
        }
        for (int i = 1; i <= 3; i++) {
            checkout.moveOn("ORD-" + i, "paid", "OrderPaid");
        }
        for (int i = 1; i <= 3; i++) {
            checkout.moveOn("ORD-" + i, "shipped", "OrderShipped");
        }
        broker.waitFor(9, mark, "9 events from Debezium");
        List<OrderEvent> events = broker.readSince(mark);
        System.out.println("  3 orders are placed, paid and shipped, each step its own transaction: 9 commits, the orders taking turns. "
                + Broker.TOPIC + " has " + Broker.PARTITIONS + " partitions.");
        for (int i = 1; i <= 3; i++) {
            String id = "ORD-" + i;
            List<OrderEvent> mine = events.stream().filter(e -> e.orderId().equals(id)).toList();
            System.out.println("  " + id + ": partition " + mine.stream().map(e -> Integer.toString(e.partition())).distinct().collect(Collectors.joining(" and "))
                    + ", " + mine.stream().map(OrderEvent::type).collect(Collectors.joining(", ")) + ".");
        }
        System.out.println("  " + describePartitions(events) + " the order id is the key, and the key picks the partition.");
        System.out.println("  each order's own events stay in the order they were committed. across orders, nothing is promised.");
        cdc.stop();
        System.out.println("  the bill: 2 containers, Postgres started with wal_level " + database.walLevel() + ", and 1 replication slot.");
        database.dropSlot(ChangeDataCapture.SLOT);
        System.out.println("  a slot whose reader has gone keeps log for ever: limit " + database.slotLogLimit()
                + ". retiring Debezium means dropping its slot. slot exists now: " + yesNo(database.slotExists(ChangeDataCapture.SLOT)) + ".");
        System.out.println("  and delivery is at least once, so every reader of " + Broker.TOPIC + " has to recognise an event id it has already seen.");
    }

    /** Says, in words, which partitions ended up holding which orders. */
    static String describePartitions(List<OrderEvent> events) {
        List<String> parts = new ArrayList<>();
        for (int p = 0; p < Broker.PARTITIONS; p++) {
            final int partition = p;
            List<String> orders = events.stream().filter(e -> e.partition() == partition).map(OrderEvent::orderId).distinct().toList();
            if (orders.isEmpty()) {
                parts.add("partition " + p + " holds none");
            } else if (orders.size() == 1) {
                parts.add("partition " + p + " holds only " + orders.get(0));
            } else {
                parts.add("partition " + p + " holds " + String.join(" and ", orders) + " taking turns");
            }
        }
        return String.join(", ", parts) + ".";
    }

    private static String yesNo(boolean b) {
        return b ? "yes" : "no";
    }
}
