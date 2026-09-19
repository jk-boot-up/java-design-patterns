package com.jk.explore.deadletter;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.*;

class DeadLetterTest {

    @Test
    void withoutADeadLetterChannelAPoisonMessageBlocksEverythingBehindIt() {
        Worker w = DeadLetterDemo.loaded(DeadLetterDemo.fussy(), 10);
        w.runAll(false);
        assertEquals(List.of("ORD-1"), w.handled());
        assertEquals(3, w.waiting());
        assertEquals(11, w.totalAttempts());
    }

    @Test
    void withOneItIsMovedAsideAfterTheAttemptLimitAndTheRestGoThrough() {
        Worker w = DeadLetterDemo.loaded(DeadLetterDemo.fussy(), 3);
        w.runAll(true);
        assertEquals(List.of("ORD-1", "ORD-3", "ORD-4"), w.handled());
        assertEquals(0, w.waiting());
        assertEquals(1, w.deadLetters().size());
    }

    @Test
    void aDeadLetterKeepsTheMessageTheAttemptsAndTheReason() {
        Worker w = DeadLetterDemo.loaded(DeadLetterDemo.fussy(), 3);
        w.runAll(true);
        DeadLetter d = w.deadLetters().get(0);
        assertEquals(new Message("ORD-2", "### garbled ###"), d.message());
        assertEquals(3, d.attempts());
        assertEquals("cannot read the body of ORD-2", d.lastError());
    }

    @Test
    void aTransientFailureThatRecoversIsNotDeadLettered() {
        Map<String, Integer> seen = new HashMap<>();
        Consumer<Message> flaky = m -> {
            int n = seen.merge(m.id(), 1, Integer::sum);
            if (m.id().equals("ORD-3") && n < 2) throw new IllegalStateException("timeout");
        };
        Worker w = new Worker(flaky, 3);
        w.send(new Message("ORD-3", "x"));
        w.runAll(true);
        assertEquals(List.of("ORD-3"), w.handled());
        assertTrue(w.deadLetters().isEmpty());
        assertEquals(2, w.totalAttempts());
    }

    @Test
    void replayingAfterAFixHandlesTheMessageButNotInItsOriginalPlace() {
        boolean[] fixed = {false};
        Worker w = DeadLetterDemo.loaded(m -> { if (!fixed[0] && m.body().contains("###")) throw new IllegalArgumentException("bad"); }, 3);
        w.runAll(true);
        fixed[0] = true;
        assertEquals(1, w.replayDeadLetters());
        w.runAll(true);
        assertEquals(List.of("ORD-1", "ORD-3", "ORD-4", "ORD-2"), w.handled());
        assertTrue(w.deadLetters().isEmpty());
    }

    @Test
    void replayingBeforeTheFixSendsItStraightBack() {
        Worker w = DeadLetterDemo.loaded(DeadLetterDemo.fussy(), 3);
        w.runAll(true);
        w.replayDeadLetters();
        w.runAll(true);
        assertEquals(1, w.deadLetters().size());
    }

    @Test
    void theMainChannelLooksHealthyWhileTheLossPilesUpInTheDeadLetters() {
        Worker w = new Worker(DeadLetterDemo.fussy(), 3);
        for (int i = 1; i <= 40; i++) w.send(new Message("ORD-" + i, i % 2 == 0 ? "###" : "ok"));
        w.runAll(true);
        assertEquals(0, w.waiting());
        assertEquals(20, w.deadLetters().size());
    }
}
