package com.jk.explore.producerconsumer;

import com.jk.explore.producerconsumer.harness.Gate;
import com.jk.explore.producerconsumer.harness.Rendezvous;
import com.jk.explore.producerconsumer.harness.StepExecutor;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Phase 0's exit requirement: each of the three harness pieces, proven
 * against a real, known race — not merely exercised. Every test here uses
 * no {@code Thread.sleep} anywhere; a thread that has not reached the point
 * being tested is parked, not guessed at.
 */
class HarnessSelfTest {

    // ---------------------------------------------------------- Gate

    @RepeatedTest(20)
    void gateHoldsAThreadUntilOpened() throws InterruptedException {
        Gate gate = new Gate();
        AtomicBoolean proceeded = new AtomicBoolean(false);
        Thread waiter = new Thread(() -> {
            gate.awaitOpen();
            proceeded.set(true);
        });
        waiter.start();

        // The waiter thread exists and may be scheduled, but it cannot have
        // set the flag: the gate is provably still closed.
        assertFalse(gate.isOpen());
        assertFalse(proceeded.get());

        gate.open();
        waiter.join(2_000);

        assertTrue(proceeded.get(), "the waiter must have proceeded once the gate opened");
    }

    // ---------------------------------------------------------- Rendezvous

    /**
     * The known race: two threads read the same shared value, meet at a
     * rendezvous, then both write back a value derived from what they read.
     * Without the rendezvous this is "sometimes wrong". With it, it is
     * wrong every single time — which is the proof the harness works.
     */
    @RepeatedTest(20)
    void rendezvousForcesTheLostUpdateEveryRun() throws InterruptedException {
        int[] sharedStock = {10};
        Rendezvous bothHaveRead = new Rendezvous("both-have-read", 2);

        Runnable decrement = () -> {
            int seen = sharedStock[0];
            bothHaveRead.meet();
            sharedStock[0] = seen - 1;
        };

        Thread t1 = new Thread(decrement);
        Thread t2 = new Thread(decrement);
        t1.start();
        t2.start();
        t1.join(2_000);
        t2.join(2_000);

        // Two decrements should leave 8. The rendezvous forces both threads
        // to read 10 before either writes, so exactly one decrement is lost
        // and the result is 9 -- every run.
        assertEquals(9, sharedStock[0],
                "the rendezvous must force the same lost update on every run");
    }

    // ---------------------------------------------------------- StepExecutor

    @Test
    void stepExecutorRunsNothingUntilStepped() {
        StepExecutor executor = new StepExecutor();
        AtomicInteger order = new AtomicInteger();
        int[] firstRan = {-1};
        int[] secondRan = {-1};

        executor.execute(() -> firstRan[0] = order.incrementAndGet());
        executor.execute(() -> secondRan[0] = order.incrementAndGet());

        assertEquals(2, executor.pending());
        assertEquals(-1, firstRan[0], "nothing should have run yet");

        assertTrue(executor.runNext());
        assertEquals(1, firstRan[0]);
        assertEquals(-1, secondRan[0], "the second task must still be untouched");
        assertEquals(1, executor.pending());

        assertTrue(executor.runNext());
        assertEquals(2, secondRan[0]);
        assertEquals(0, executor.pending());

        assertFalse(executor.runNext(), "nothing left to run");
    }
}
