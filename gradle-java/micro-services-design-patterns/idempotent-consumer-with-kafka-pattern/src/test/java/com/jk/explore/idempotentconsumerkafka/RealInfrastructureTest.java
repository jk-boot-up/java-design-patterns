package com.jk.explore.idempotentconsumerkafka;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import org.apache.kafka.clients.consumer.CommitFailedException;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What the real broker and the real database do, asked of them directly.
 *
 * <p>One broker and one database are started for the whole class, because starting them is
 * the slow part, and both are removed at the end. Each test uses its own topic and its own
 * group, and empties the tables first. Every wait is a bounded poll on something Kafka or
 * Postgres can actually be asked about; there is no sleep anywhere in this file.
 */
class RealInfrastructureTest {

    private static Broker broker;
    private static Database database;

    @BeforeAll
    static void startBoth() {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        broker = new Broker();
        database = new Database();
        broker.start();
        database.start();
    }

    @AfterAll
    static void stopBoth() {
        if (broker != null) {
            broker.close();
        }
        if (database != null) {
            database.close();
        }
    }

    private static String fresh(String topic) {
        return fresh(topic, 3);
    }

    private static String fresh(String topic, int orders) {
        broker.createTopic(topic);
        database.empty();
        try (Checkout checkout = new Checkout(broker, topic)) {
            for (int i = 1; i <= orders; i++) {
                assertEquals(i - 1, checkout.place(OrderPlaced.of(i)), "a new topic numbers its orders from 0");
            }
        }
        return topic;
    }

    @Test
    void aCopyThatStopsBeforeWritingDownItsPlaceIsFollowedByTheSameOrders() {
        String topic = fresh("redelivered");
        Notifications a = new Notifications("copy A", broker, "g-redelivered", topic);
        a.takeAndHandle(3, new JustSend(database));
        a.crash();
        assertEquals(-1, broker.placeWrittenDown("g-redelivered", topic));
        try (Notifications b = new Notifications("copy B", broker, "g-redelivered", topic)) {
            b.takeAndHandle(3, new JustSend(database));
            b.sayDone();
            assertEquals(List.of(0L, 1L, 2L), b.placesHandedOver());
        }
        assertEquals(3, broker.placeWrittenDown("g-redelivered", topic));
        assertEquals(6, database.confirmations());
    }

    @Test
    void aCopyThatWritesDownItsPlaceIsNotHandedTheOrdersAgain() {
        String topic = fresh("not-redelivered");
        try (Notifications a = new Notifications("copy A", broker, "g-not-redelivered", topic)) {
            a.takeAndHandle(3, new JustSend(database));
            a.sayDone();
        }
        assertEquals(3, broker.placeWrittenDown("g-not-redelivered", topic));
    }

    @Test
    void aSetOfIdsInMemoryStartsEmptyInTheNextCopy() {
        String topic = fresh("in-memory");
        Notifications a = new Notifications("copy A", broker, "g-in-memory", topic);
        RememberInMemory aMemory = new RememberInMemory(database);
        a.takeAndHandle(3, aMemory);
        a.crash();
        try (Notifications b = new Notifications("copy B", broker, "g-in-memory", topic)) {
            RememberInMemory bMemory = new RememberInMemory(database);
            assertEquals(0, bMemory.remembered());
            b.takeAndHandle(3, bMemory);
        }
        assertEquals(3, aMemory.remembered());
        assertEquals(6, database.confirmations());
    }

    @Test
    void theTableOfIdsTurnsSixDeliveriesIntoThreeEmails() {
        String topic = fresh("table");
        Notifications a = new Notifications("copy A", broker, "g-table", topic);
        assertEquals(3, a.takeAndHandle(3, new RecordIdInSameTransaction(database)));
        a.crash();
        try (Notifications b = new Notifications("copy B", broker, "g-table", topic)) {
            assertEquals(0, b.takeAndHandle(3, new RecordIdInSameTransaction(database)));
            assertEquals(3, b.placesHandedOver().size());
        }
        assertEquals(3, database.confirmations());
        assertEquals(3, database.handledIds());
    }

    @Test
    void aCrashBetweenTheEmailAndTheIdSendsTheEmailTwice() {
        String topic = fresh("afterwards", 1);
        Notifications a = new Notifications("copy A", broker, "g-afterwards", topic);
        assertThrows(ProcessDied.class, () -> a.takeAndHandle(1, new RecordIdAfterwards(database, true)));
        a.crash();
        assertEquals(1, database.confirmations());
        assertEquals(0, database.handledIds());
        try (Notifications b = new Notifications("copy B", broker, "g-afterwards", topic)) {
            b.takeAndHandle(1, new RecordIdAfterwards(database, false));
        }
        assertEquals(2, database.confirmationsFor("ORD-1"));
    }

    @Test
    void aCrashBeforeTheCommitWritesNeitherAndTheRedeliveryWritesBothOnce() {
        String topic = fresh("together", 1);
        RecordIdInSameTransaction pattern = new RecordIdInSameTransaction(database);
        Notifications a = new Notifications("copy A", broker, "g-together", topic);
        pattern.begin(a.take(1).get(0)).die();
        a.crash();
        assertEquals(0, database.confirmations());
        assertEquals(0, database.handledIds());
        try (Notifications b = new Notifications("copy B", broker, "g-together", topic)) {
            assertEquals(1, b.takeAndHandle(1, pattern));
        }
        assertEquals(1, database.confirmationsFor("ORD-1"));
        assertEquals(1, database.handledIds());
    }

    /**
     * Two copies at once. A takes the order and holds its transaction open; Kafka gives up
     * on A and hands the order to B; B's insert of the same id is made to wait by Postgres
     * until A commits, and then writes nothing. A's request to write down its place is refused.
     */
    @Test
    void whenTwoCopiesHoldTheSameOrderTheDatabaseLetsOnlyOneQueueTheEmail() throws Exception {
        String topic = fresh("race", 1);
        Duration patience = KafkaIdempotentConsumerDemo.SHORT_PATIENCE;
        RecordIdInSameTransaction pattern = new RecordIdInSameTransaction(database);
        Notifications a = new Notifications("copy A", broker, "g-race", topic, patience);
        RecordIdInSameTransaction.Open aWork = pattern.begin(a.take(1).get(0));
        assertTrue(aWork.queued());

        AtomicBoolean bHanded = new AtomicBoolean();
        AtomicReference<Boolean> bQueued = new AtomicReference<>();
        Thread copyB = new Thread(() -> {
            try (Notifications b = new Notifications("copy B", broker, "g-race", topic, patience)) {
                OrderPlaced same = b.take(1).get(0);
                bHanded.set(true);
                bQueued.set(pattern.handle(same));
                b.sayDone();
            }
        });
        copyB.start();
        Poll.until("Kafka to hand the order to copy B", () -> bHanded.get());
        Poll.until("Postgres to make copy B wait", () -> database.waitingOnALock() == 1);
        aWork.commit();
        Poll.until("copy B to finish", () -> !copyB.isAlive());

        assertFalse(bQueued.get());
        assertEquals(1, database.confirmationsFor("ORD-1"));
        assertThrows(CommitFailedException.class, a::sayDone);
        a.close();
    }

    @Test
    void aReplayAfterTheIdsWereCleanedUpSendsEveryEmailAgain() {
        String topic = fresh("replay");
        RecordIdInSameTransaction pattern = new RecordIdInSameTransaction(database);
        try (Notifications a = new Notifications("copy A", broker, "g-replay", topic)) {
            a.takeAndHandle(3, pattern);
            a.sayDone();
        }
        assertEquals(168, broker.hoursTheTopicKeepsOrders(topic), "Kafka's default is seven days");
        broker.moveGroupBackToTheStart("g-replay", topic);
        try (Notifications b = new Notifications("copy B", broker, "g-replay", topic)) {
            assertEquals(0, b.takeAndHandle(3, pattern), "with the ids kept, a replay queues nothing");
        }
        database.forgetIdsOlderThanHours(-1);
        broker.moveGroupBackToTheStart("g-replay", topic);
        try (Notifications c = new Notifications("copy C", broker, "g-replay", topic)) {
            assertEquals(3, c.takeAndHandle(3, pattern), "with the ids gone, a replay queues all of them");
        }
        assertEquals(6, database.confirmations());
    }
}
