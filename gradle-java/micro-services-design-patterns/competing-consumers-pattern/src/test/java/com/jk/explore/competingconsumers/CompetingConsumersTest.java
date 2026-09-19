package com.jk.explore.competingconsumers;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import static org.junit.jupiter.api.Assertions.*;

class CompetingConsumersTest {

    @RepeatedTest(3)
    void moreConsumersMeanMoreInProgress() {
        assertArrayEquals(new int[]{1, 5}, CompetingConsumersDemo.heldJobs(1));
        assertArrayEquals(new int[]{3, 3}, CompetingConsumersDemo.heldJobs(3));
        assertArrayEquals(new int[]{6, 0}, CompetingConsumersDemo.heldJobs(6));
    }

    @RepeatedTest(3)
    void everyMessageIsHandledExactlyOnceByExactlyOneConsumer() {
        Broker broker = new Broker();
        Set<Integer> seen = ConcurrentHashMap.newKeySet();
        List<Integer> all = Collections.synchronizedList(new ArrayList<>());
        for (int i = 1; i <= 500; i++) broker.publish(i, "m" + i);
        try (ConsumerPool pool = new ConsumerPool(broker, 4, (who, d) -> { seen.add(d.id()); all.add(d.id()); })) {
            assertTrue(ConsumerPool.until(() -> broker.acknowledged() == 500));
        }
        assertEquals(500, all.size());
        assertEquals(500, seen.size());
    }

    @RepeatedTest(3)
    void aSlowFirstMessageFinishesLast() {
        Broker broker = new Broker();
        Gate first = new Gate();
        List<Integer> finished = Collections.synchronizedList(new ArrayList<>());
        for (int i = 1; i <= 3; i++) broker.publish(i, "m" + i);
        try (ConsumerPool pool = new ConsumerPool(broker, 2, (who, d) -> {
            if (d.id() == 1) first.await();
            finished.add(d.id());
        })) {
            ConsumerPool.until(() -> finished.size() == 2);
            first.open();
            assertTrue(ConsumerPool.until(() -> broker.acknowledged() == 3));
        }
        assertEquals(List.of(2, 3, 1), finished);
    }

    @Test
    void aFailedMessageIsGivenBackAndHandledAgain() {
        Broker broker = new Broker();
        List<Integer> attempts = Collections.synchronizedList(new ArrayList<>());
        broker.publish(1, "m");
        try (ConsumerPool pool = new ConsumerPool(broker, 2, (who, d) -> {
            attempts.add(d.attempt());
            if (d.attempt() < 3) throw new IllegalStateException("boom");
        })) {
            assertTrue(ConsumerPool.until(() -> broker.acknowledged() == 1));
        }
        assertEquals(List.of(1, 2, 3), attempts);
    }

    @Test
    void aCrashAfterTheEffectCausesADuplicateUnlessTheConsumerRemembers() {
        List<String> plain = Collections.synchronizedList(new ArrayList<>());
        Broker b1 = new Broker();
        b1.publish(1, "charge");
        try (ConsumerPool pool = new ConsumerPool(b1, 2, (who, d) -> { plain.add(d.body()); if (d.attempt() == 1) throw new IllegalStateException(); })) {
            assertTrue(ConsumerPool.until(() -> b1.acknowledged() == 1));
        }
        assertEquals(2, plain.size());
        List<String> safe = Collections.synchronizedList(new ArrayList<>());
        Set<Integer> done = ConcurrentHashMap.newKeySet();
        Broker b2 = new Broker();
        b2.publish(1, "charge");
        try (ConsumerPool pool = new ConsumerPool(b2, 2, (who, d) -> { if (done.add(d.id())) safe.add(d.body()); if (d.attempt() == 1) throw new IllegalStateException(); })) {
            assertTrue(ConsumerPool.until(() -> b2.acknowledged() == 1));
        }
        assertEquals(1, safe.size());
    }

    @RepeatedTest(3)
    void aSharedDownstreamCapsUsefulWork() {
        assertArrayEquals(new int[]{2, 4}, CompetingConsumersDemo.sharedDatabase());
    }
}
