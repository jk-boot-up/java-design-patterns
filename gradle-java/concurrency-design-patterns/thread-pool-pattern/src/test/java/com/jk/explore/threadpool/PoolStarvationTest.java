package com.jk.explore.threadpool;

import com.jk.explore.threadpool.pattern.PoolStarvation;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PoolStarvationTest {

    @RepeatedTest(20)
    void aTaskThatSubmitsAndWaitsOnAnotherTaskInAOnePoolAlwaysStarves() throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(1);
        try {
            PoolStarvation.Outcome outcome = PoolStarvation.attemptNestedSubmit(pool, 100);

            assertTrue(outcome.starved(),
                    "the pool has exactly one worker, and that worker is the one waiting: "
                            + "the inner task can never be scheduled");
            assertTrue(outcome.waitedMillis() >= 100,
                    "the rescue timeout is the only thing that ends the wait");
        } finally {
            pool.shutdownNow();
            pool.awaitTermination(2, TimeUnit.SECONDS);
        }
    }

    @RepeatedTest(20)
    void aPoolWithTwoWorkersDoesNotStarveOnOneNestedSubmit() throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        try {
            PoolStarvation.Outcome outcome = PoolStarvation.attemptNestedSubmit(pool, 500);

            assertEquals(false, outcome.starved(),
                    "a second worker is free to run the inner task, so the outer wait resolves");
        } finally {
            pool.shutdownNow();
            pool.awaitTermination(2, TimeUnit.SECONDS);
        }
    }
}
