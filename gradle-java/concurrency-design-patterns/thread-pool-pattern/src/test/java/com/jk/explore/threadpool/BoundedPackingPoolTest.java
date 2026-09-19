package com.jk.explore.threadpool;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.harness.Gate;
import com.jk.explore.threadpool.pattern.BoundedPackingPool;
import org.junit.jupiter.api.RepeatedTest;

import java.util.concurrent.CountDownLatch;

import static org.junit.jupiter.api.Assertions.assertEquals;

class BoundedPackingPoolTest {

    @RepeatedTest(20)
    void theQueueReachesItsStatedCapacityAndThenRejectsOnTheSpot() throws InterruptedException {
        BoundedPackingPool pool = new BoundedPackingPool(1, 3);
        Gate workerHold = new Gate();
        CountDownLatch workerStarted = new CountDownLatch(1);
        pool.submitRaw(() -> {
            workerStarted.countDown();
            workerHold.awaitOpen();
        });
        // The one worker is provably busy on the held task before any real
        // order is submitted, so the queue can only ever fill, never drain,
        // until the gate below is opened.
        workerStarted.await();

        for (int i = 1; i <= 3; i++) {
            pool.submit(new Order("ord-" + i, "BNS-220"), order -> { });
        }
        assertEquals(3, pool.queueDepth());
        assertEquals(0, pool.rejectedCount());

        pool.submit(new Order("ord-overflow", "BNS-220"), order -> { });
        assertEquals(1, pool.rejectedCount(),
                "the worker is busy and the queue is full: this submission has nowhere to go");

        workerHold.open();
        pool.close();
    }
}
