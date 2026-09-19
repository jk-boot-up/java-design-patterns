package com.jk.explore.scattergather;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.junit.jupiter.api.Assertions.*;

class ScatterGatherTest {

    private final ExecutorService pool = Executors.newCachedThreadPool();

    @AfterEach
    void stop() {
        pool.shutdownNow();
    }

    @Test
    void sequentialIsTheSumAndParallelIsTheMax() {
        assertEquals(1300, Latencies.sequentialTotal(Latencies.FOUR));
        assertEquals(900, Latencies.parallelTotal(Latencies.FOUR));
        assertEquals(500, Latencies.withDeadline(Latencies.FOUR, 500));
        assertEquals(900, Latencies.withDeadline(Latencies.FOUR, 5000));
    }

    @RepeatedTest(3)
    void allFourAreAskedAtTheSameMoment() {
        assertEquals(4, ScatterGatherDemo.askedAtOnce(pool));
    }

    @Test
    void allAnswersAreGatheredWhenAllAreQuick() {
        var r = new ScatterGather(pool).ask(List.of(Supplier.fixed("A", 300), Supplier.fixed("B", 200)), "x", 2000);
        assertEquals(2, r.quotes().size());
        assertTrue(r.missing().isEmpty());
        assertEquals("B", r.best().supplier());
    }

    @Test
    void aSlowSupplierIsLeftOutAtTheDeadlineAndNamed() {
        Gate never = new Gate();
        var r = new ScatterGather(pool).ask(List.of(Supplier.fixed("A", 300), Supplier.held("Slow", 100, never)), "x", 300);
        assertEquals(1, r.quotes().size());
        assertEquals(List.of("Slow (too slow)"), r.missing());
        assertEquals("A", r.best().supplier());
        never.open();
    }

    @Test
    void aFailingSupplierIsLeftOutAndTheOthersStillAnswer() {
        var r = new ScatterGather(pool).ask(List.of(Supplier.fixed("A", 300), Supplier.failing("B")), "x", 2000);
        assertEquals(1, r.quotes().size());
        assertEquals(List.of("B (B is down)"), r.missing());
    }

    @Test
    void nobodyAnsweringGivesNoBestPriceRatherThanAnError() {
        var r = new ScatterGather(pool).ask(List.of(Supplier.failing("A"), Supplier.failing("B")), "x", 2000);
        assertNull(r.best());
        assertEquals(2, r.missing().size());
    }

    @Test
    void theMoreYouWaitForTheLessOftenTheyAreAllQuick() {
        assertEquals(99.0, Latencies.chanceAllFast(1), 0.01);
        assertEquals(96.06, Latencies.chanceAllFast(4), 0.01);
        assertTrue(Latencies.chanceAllFast(10) < Latencies.chanceAllFast(4));
    }
}
