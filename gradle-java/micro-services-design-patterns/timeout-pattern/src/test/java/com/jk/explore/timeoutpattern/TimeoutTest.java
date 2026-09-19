package com.jk.explore.timeoutpattern;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.*;

class TimeoutTest {

    private final ExecutorService pool = Executors.newCachedThreadPool();

    @AfterEach
    void stop() {
        pool.shutdownNow();
    }

    @Test
    void aCallWithNoLimitWaitsForeverOnAGate() throws Exception {
        Gate gate = new Gate();
        SupplierApi api = new SupplierApi(gate);
        Thread t = new Thread(() -> api.stockOf("A"));
        t.start();
        long until = System.nanoTime() + 5_000_000_000L;
        while (t.getState() != Thread.State.WAITING && System.nanoTime() < until) Thread.onSpinWait();
        assertEquals(Thread.State.WAITING, t.getState());
        gate.open();
        t.join();
        assertEquals(1, api.finished());
    }

    @Test
    void aLimitTurnsANeverEndingWaitIntoAnAnswer() {
        String shown = new Callers(pool).withTimeout(new SupplierApi(new Gate()), "A", 50);
        assertEquals("stock unknown, try again shortly", shown);
    }

    @Test
    void aFastCallWithinTheLimitReturnsItsAnswer() {
        Gate gate = new Gate();
        gate.open();
        assertEquals("42 of A", new Callers(pool).withTimeout(new SupplierApi(gate), "A", 5000));
    }

    @Test
    void givingUpDoesNotStopTheWorkAtTheSupplier() {
        Gate gate = new Gate();
        SupplierApi api = new SupplierApi(gate);
        new Callers(pool).withTimeout(api, "A", 50);
        assertEquals(1, api.started());
        assertEquals(0, api.finished());
        gate.open();
        long until = System.nanoTime() + 5_000_000_000L;
        while (api.finished() < 1 && System.nanoTime() < until) Thread.onSpinWait();
        assertEquals(1, api.finished());
    }

    @Test
    void theLimitDecidesHowManyHealthyCallsSucceed() {
        List<Integer> day = Latency.aTypicalHundred();
        assertEquals(100, day.size());
        assertEquals(54, Latency.succeedingWithin(day, 50));
        assertEquals(90, Latency.succeedingWithin(day, 100));
        assertEquals(98, Latency.succeedingWithin(day, 1000));
        assertEquals(100, Latency.succeedingWithin(day, 3000));
    }

    @Test
    void aSharedBudgetBoundsThePageAndSkipsWhatItCannotAfford() {
        var outcomes = Budget.spend(1000, 400, 700, 500);
        assertEquals("answered", outcomes.get(0).what());
        assertEquals("cut off", outcomes.get(1).what());
        assertEquals(600, outcomes.get(1).spentMillis());
        assertEquals("skipped", outcomes.get(2).what());
        assertEquals(1000, Budget.total(outcomes));
    }

    @Test
    void aBudgetNeverSpendsMoreThanItHas() {
        for (int budget = 0; budget <= 2000; budget += 100) {
            assertTrue(Budget.total(Budget.spend(budget, 300, 300, 300, 300)) <= budget);
        }
    }
}
