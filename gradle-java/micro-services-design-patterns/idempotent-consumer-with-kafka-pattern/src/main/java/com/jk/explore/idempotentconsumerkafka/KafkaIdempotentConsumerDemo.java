package com.jk.explore.idempotentconsumerkafka;

import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;

/**
 * Six acts against a real Kafka broker and a real Postgres database, both started and stopped
 * by this program.
 *
 * <p>Checkout writes an OrderPlaced message to a Kafka topic for every order. The
 * notifications service reads the topic and queues one confirmation email per order, as a
 * row in its own database. Kafka promises to deliver each message at least once, and the
 * acts show what "at least" means, and what it takes to turn it into exactly one email.
 */
public class KafkaIdempotentConsumerDemo {

    static final String GROUP = "notifications";

    /** How long a copy may go without asking for more before Kafka decides it is stuck, in act five. */
    static final Duration SHORT_PATIENCE = Duration.ofSeconds(3);

    /** How long the cleanup job in act six keeps an id. */
    static final int KEEP_IDS_HOURS = 24;

    public static void main(String[] args) {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        try (Broker broker = new Broker(); Database database = new Database()) {
            try {
                broker.start();
                database.start();
            } catch (RuntimeException e) {
                System.out.println(Broker.WOULD_NOT_START_ADVICE);
                return;
            }
            one(broker, database);
            two(broker, database);
            three(broker, database);
            four(broker, database);
            five(broker, database);
            six(broker, database);
        }
    }

    /** No memory at all. A copy crashes before writing down its place, and the next copy is handed everything again. */
    static void one(Broker broker, Database database) {
        System.out.println("ONE. Kafka sends it again.");
        String topic = fresh(broker, database, "orders-one");
        List<Long> placed = placeOrders(broker, topic, 3);
        System.out.println("  a Kafka broker and a Postgres database are running in containers. checkout places 3 orders, at places " + places(placed) + ".");

        Notifications a = new Notifications("copy A", broker, GROUP, topic);
        int queuedByA = a.takeAndHandle(3, new JustSend(database));
        a.crash();
        System.out.println("  notifications copy A is handed " + a.placesHandedOver().size() + ", queues " + queuedByA + " confirmation emails, and crashes before writing down its place. place written down: " + written(broker, topic) + ".");

        try (Notifications b = new Notifications("copy B", broker, GROUP, topic)) {
            b.takeAndHandle(3, new JustSend(database));
            b.sayDone();
            System.out.println("  copy B joins the same group and is handed the same orders again, at places " + places(b.placesHandedOver()) + ". nothing on them says they are repeats.");
            int deliveries = a.placesHandedOver().size() + b.placesHandedOver().size();
            System.out.println("  deliveries: " + deliveries + " for 3 orders. confirmation emails queued: " + database.confirmations() + ".");
        }
    }

    /** A set of ids in memory. The set lives in copy A, and the redelivery goes to copy B. */
    static void two(Broker broker, Database database) {
        System.out.println("TWO. A list of ids in memory.");
        String topic = fresh(broker, database, "orders-two");
        placeOrders(broker, topic, 3);

        Notifications a = new Notifications("copy A", broker, GROUP, topic);
        RememberInMemory aMemory = new RememberInMemory(database);
        a.takeAndHandle(3, aMemory);
        a.crash();
        System.out.println("  copy A keeps a list of handled ids in memory. it handles 3 orders, remembers " + aMemory.remembered() + " ids, and crashes before writing down its place.");

        try (Notifications b = new Notifications("copy B", broker, GROUP, topic)) {
            RememberInMemory bMemory = new RememberInMemory(database);
            int rememberedAtStart = bMemory.remembered();
            b.takeAndHandle(3, bMemory);
            b.sayDone();
            System.out.println("  copy B is handed the same " + b.placesHandedOver().size() + ". its list starts with " + rememberedAtStart + " ids. confirmation emails queued: " + database.confirmations() + ".");
        }
        System.out.println("  the list died with copy A. a redelivery happens because a copy stopped, so it always lands on a list that is new.");
    }

    /** The pattern: the id and the email in one transaction, in a table that outlives every copy. */
    static void three(Broker broker, Database database) {
        System.out.println("THREE. A table of ids, in the same transaction.");
        String topic = fresh(broker, database, "orders-three");
        placeOrders(broker, topic, 3);

        Notifications a = new Notifications("copy A", broker, GROUP, topic);
        a.takeAndHandle(3, new RecordIdInSameTransaction(database));
        a.crash();
        System.out.println("  copy A writes each order's id and its email in one database transaction. it handles 3 and crashes before writing down its place.");

        try (Notifications b = new Notifications("copy B", broker, GROUP, topic)) {
            int queuedByB = b.takeAndHandle(3, new RecordIdInSameTransaction(database));
            b.sayDone();
            int skipped = b.placesHandedOver().size() - queuedByB;
            System.out.println("  copy B is handed the same " + b.placesHandedOver().size() + ". the table already holds their ids, so B skips " + skipped + " and queues " + queuedByB + ".");
            int deliveries = a.placesHandedOver().size() + b.placesHandedOver().size();
            System.out.println("  deliveries: " + deliveries + ". confirmation emails queued: " + database.confirmations() + ". ids stored: " + database.handledIds() + ". the table outlived the copy that wrote it.");
        }
    }

    /** The same crash in two places: between two transactions, and inside one. */
    static void four(Broker broker, Database database) {
        System.out.println("FOUR. Where the crash lands.");
        String topic = fresh(broker, database, "orders-four-afterwards");
        placeOrders(broker, topic, 1);
        Notifications a = new Notifications("copy A", broker, GROUP, topic);
        try {
            a.takeAndHandle(1, new RecordIdAfterwards(database, true));
        } catch (ProcessDied died) {
            a.crash();
        }
        System.out.println("  id written after the email, as a second step. copy A queues ORD-1's email and dies before writing the id. emails: " + database.confirmations() + ", ids: " + database.handledIds() + ".");
        try (Notifications b = new Notifications("copy B", broker, GROUP, topic)) {
            b.takeAndHandle(1, new RecordIdAfterwards(database, false));
            b.sayDone();
        }
        System.out.println("  copy B is handed ORD-1, finds no id, and queues it again. emails for ORD-1: " + database.confirmationsFor("ORD-1") + ".");

        topic = fresh(broker, database, "orders-four-together");
        placeOrders(broker, topic, 1);
        RecordIdInSameTransaction pattern = new RecordIdInSameTransaction(database);
        Notifications c = new Notifications("copy A", broker, GROUP, topic);
        OrderPlaced order = c.take(1).get(0);
        pattern.begin(order).die();
        c.crash();
        System.out.println("  id and email in one transaction. copy A dies before the commit, and Postgres throws both away. emails: " + database.confirmations() + ", ids: " + database.handledIds() + ".");
        try (Notifications d = new Notifications("copy B", broker, GROUP, topic)) {
            d.takeAndHandle(1, pattern);
            d.sayDone();
        }
        System.out.println("  copy B is handed ORD-1 and handles it properly. emails: " + database.confirmations() + ", ids: " + database.handledIds() + ". exactly once, from a broker that promises at least once.");
    }

    /**
     * A slow copy loses its orders while it is still working on one, and a second copy is
     * handed the same order at the same time. The database decides which one wins.
     */
    static void five(Broker broker, Database database) {
        System.out.println("FIVE. Two copies at once.");
        String topic = fresh(broker, database, "orders-five");
        placeOrders(broker, topic, 1);
        RecordIdInSameTransaction pattern = new RecordIdInSameTransaction(database);

        Notifications a = new Notifications("copy A", broker, GROUP, topic, SHORT_PATIENCE);
        OrderPlaced order = a.take(1).get(0);
        RecordIdInSameTransaction.Open aWork = pattern.begin(order);

        // Copy B runs as its own program would: its own thread, its own Kafka connection, its own database connection.
        AtomicBoolean bHanded = new AtomicBoolean();
        AtomicReference<Boolean> bQueued = new AtomicReference<>();
        AtomicReference<RuntimeException> bFailed = new AtomicReference<>();
        Thread copyB = new Thread(() -> {
            try (Notifications b = new Notifications("copy B", broker, GROUP, topic, SHORT_PATIENCE)) {
                OrderPlaced same = b.take(1).get(0);
                bHanded.set(true);
                bQueued.set(pattern.handle(same));
                b.sayDone();
            } catch (RuntimeException e) {
                bFailed.set(e);
            }
        });
        copyB.start();
        Poll.until("Kafka to hand ORD-1 to copy B", () -> bHanded.get() || bFailed.get() != null);
        System.out.println("  copy A is handed " + order.orderId() + " and is slow. after " + SHORT_PATIENCE.toSeconds() + " seconds without asking for more, Kafka decides A is stuck and hands the order to copy B.");
        Poll.until("copy B to be stopped by the database", () -> database.waitingOnALock() == 1 || bFailed.get() != null);
        System.out.println("  both copies are working on " + order.orderId() + ". A has written the id and not committed. B writes the same id, and Postgres makes it wait. sessions waiting on a lock: " + database.waitingOnALock() + ".");

        aWork.commit();
        Poll.until("copy B to finish", () -> !copyB.isAlive());
        if (bFailed.get() != null) {
            throw bFailed.get();
        }
        System.out.println("  A commits. B is told the id is taken, and skips it: queued by B: " + (bQueued.get() ? 1 : 0) + ". emails for " + order.orderId() + ": " + database.confirmationsFor(order.orderId()) + ".");

        String refusal;
        try {
            a.sayDone();
            refusal = "it was accepted, which it should not have been";
        } catch (RuntimeException e) {
            refusal = "Kafka refuses with " + e.getClass().getSimpleName();
        } finally {
            a.close();
        }
        System.out.println("  A finishes and asks for its place to be written down. " + refusal + ": A no longer owns those orders.");
    }

    /** The table cannot keep every id for ever, and Kafka decides how long is long enough. */
    static void six(Broker broker, Database database) {
        System.out.println("SIX. The bill.");
        String topic = fresh(broker, database, "orders-six");
        Instant twoDaysAgo = Instant.now().minus(2, ChronoUnit.DAYS);
        try (Checkout checkout = new Checkout(broker, topic)) {
            for (int i = 1; i <= 3; i++) {
                checkout.placeAsOf(OrderPlaced.of(i), twoDaysAgo);
            }
        }
        RecordIdInSameTransaction pattern = new RecordIdInSameTransaction(database);
        try (Notifications a = new Notifications("copy A", broker, GROUP, topic)) {
            a.takeAndHandle(3, pattern);
            a.sayDone();
        }
        int stored = database.handledIds();
        int forgotten = database.forgetIdsOlderThanHours(KEEP_IDS_HOURS);
        System.out.println("  3 orders placed two days ago are handled. ids stored: " + stored + ". a cleanup job keeps ids for " + KEEP_IDS_HOURS + " hours, and deletes " + forgotten + ".");

        long keeps = broker.hoursTheTopicKeepsOrders(topic);
        broker.moveGroupBackToTheStart(GROUP, topic);
        try (Notifications b = new Notifications("copy B", broker, GROUP, topic)) {
            b.takeAndHandle(3, pattern);
            b.sayDone();
            System.out.println("  this topic keeps orders for " + keeps + " hours. an operator replays the group from the start. handed again: " + b.placesHandedOver().size() + ". emails queued: " + database.confirmations() + ".");
        }
        System.out.println("  keep the ids at least as long as Kafka keeps the orders.");
        System.out.println("  and every message needs an id that stays the same when it is sent again, and every copy needs a transaction to put it in.");
        System.out.println("  and there are two more systems to run: this demo needed 2 containers, a broker and a database, for 1 email per order.");
    }

    /** A new topic, and empty tables, so each act starts from nothing. */
    private static String fresh(Broker broker, Database database, String topic) {
        broker.createTopic(topic);
        database.empty();
        return topic;
    }

    private static List<Long> placeOrders(Broker broker, String topic, int count) {
        List<Long> places = new ArrayList<>();
        try (Checkout checkout = new Checkout(broker, topic)) {
            for (int i = 1; i <= count; i++) {
                places.add(checkout.place(OrderPlaced.of(i)));
            }
        }
        return places;
    }

    private static String written(Broker broker, String topic) {
        long place = broker.placeWrittenDown(GROUP, topic);
        return place < 0 ? "none" : Long.toString(place);
    }

    static String places(List<Long> places) {
        return places.stream().map(String::valueOf).collect(Collectors.joining(", "));
    }
}
