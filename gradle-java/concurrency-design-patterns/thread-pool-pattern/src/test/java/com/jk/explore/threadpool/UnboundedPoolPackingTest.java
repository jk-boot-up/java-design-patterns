package com.jk.explore.threadpool;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.harness.Gate;
import com.jk.explore.threadpool.naive.UnboundedPoolPacking;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;

class UnboundedPoolPackingTest {

    @RepeatedTest(20)
    void submissionNeverBlocksOrRejectsNoMatterHowFarBehindTheWorkersAre() throws InterruptedException {
        UnboundedPoolPacking pool = new UnboundedPoolPacking(2);
        Gate workerHold = new Gate();
        CountDownLatch workersStarted = new CountDownLatch(2);
        for (int i = 0; i < 2; i++) {
            pool.raw().execute(() -> {
                workersStarted.countDown();
                try {
                    workerHold.awaitOpen();
                } catch (IllegalStateException e) {
                    // interrupted by this test's own shutdownNow() below — expected
                }
            });
        }
        // Both workers are provably parked before a single real order is
        // submitted, so every one of the 40 submissions below is guaranteed
        // to still be sitting in the queue when backlog() is read.
        workersStarted.await();

        int burst = 40;
        for (int i = 1; i <= burst; i++) {
            pool.submit(new Order("ord-" + i, "BNS-220"), order -> { });
        }

        assertEquals(burst, pool.backlog(),
                "an unbounded queue must accept every submission with nobody home to take any of them");

        pool.raw().shutdownNow();
        pool.raw().awaitTermination(2, TimeUnit.SECONDS);
    }
}
