package com.jk.explore.threadpoolspring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.core.task.TaskRejectedException;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Every wait is a latch or a gate. No test sleeps to wait for another thread. */
class AsyncPoolTest {

    @Test
    void springBootsDefaultExecutorHasEightCoreThreadsAndAnUnboundedQueue() {
        try (ConfigurableApplicationContext context = PackingApplication.start()) {
            ThreadPoolTaskExecutor pool = PackingApplication.pool(context);
            assertEquals(8, pool.getCorePoolSize());
            assertEquals(Integer.MAX_VALUE, pool.getMaxPoolSize());
            assertEquals(Integer.MAX_VALUE, pool.getThreadPoolExecutor().getQueue().remainingCapacity());
        }
    }

    @Test
    void anAsyncMethodRunsOnAPoolThreadNotTheCaller() throws Exception {
        try (ConfigurableApplicationContext context = PackingApplication.start()) {
            Gate gate = new Gate();
            gate.open();
            String worker = context.getBean(PackingService.class).pack(1, new CountDownLatch(1), gate).get(5, TimeUnit.SECONDS);
            assertNotEquals(Thread.currentThread().getName(), worker);
            assertTrue(worker.startsWith("task-"), worker);
        }
    }

    @Test
    void withEightWorkersBusyAThousandMoreOrdersQueueAndNoneIsRefused() throws Exception {
        try (ConfigurableApplicationContext context = PackingApplication.start()) {
            PackingService packing = context.getBean(PackingService.class);
            Gate gate = new Gate();
            CountDownLatch eightRunning = new CountDownLatch(8);
            List<CompletableFuture<String>> all = new ArrayList<>();
            for (int i = 0; i < 8; i++) {
                all.add(packing.pack(i, eightRunning, gate));
            }
            assertTrue(eightRunning.await(10, TimeUnit.SECONDS));
            for (int i = 0; i < 1_000; i++) {
                all.add(packing.pack(100 + i, new CountDownLatch(1), gate));
            }
            assertEquals(1_000, PackingApplication.pool(context).getThreadPoolExecutor().getQueue().size());
            gate.open();
            for (CompletableFuture<String> f : all) {
                f.get(10, TimeUnit.SECONDS);
            }
        }
    }

    @Test
    void aBoundedPoolRefusesTheSixthOrderWithATaskRejectedException() throws Exception {
        try (ConfigurableApplicationContext context = PackingApplication.start("spring.task.execution.pool.core-size=2",
                "spring.task.execution.pool.max-size=2", "spring.task.execution.pool.queue-capacity=3")) {
            PackingService packing = context.getBean(PackingService.class);
            Gate gate = new Gate();
            CountDownLatch twoRunning = new CountDownLatch(2);
            List<CompletableFuture<String>> accepted = new ArrayList<>();
            for (int i = 0; i < 2; i++) {
                accepted.add(packing.pack(i, twoRunning, gate));
            }
            assertTrue(twoRunning.await(10, TimeUnit.SECONDS));
            for (int i = 0; i < 3; i++) {
                accepted.add(packing.pack(10 + i, new CountDownLatch(1), gate));
            }
            assertThrows(TaskRejectedException.class, () -> packing.pack(99, new CountDownLatch(1), gate));
            gate.open();
            for (CompletableFuture<String> f : accepted) {
                f.get(10, TimeUnit.SECONDS);
            }
        }
    }

    @Test
    void aCallOnThisSkipsTheProxyAndRunsOnTheCallersThread() throws Exception {
        try (ConfigurableApplicationContext context = PackingApplication.start()) {
            String worker = context.getBean(PackingService.class).packThroughThis(1).get(5, TimeUnit.SECONDS);
            assertEquals(Thread.currentThread().getName(), worker);
        }
    }

    @Test
    void aTaskWaitingForAnotherOnItsOwnSingleThreadPoolStarves() throws Exception {
        try (ConfigurableApplicationContext context = PackingApplication.start("spring.task.execution.pool.core-size=1",
                "spring.task.execution.pool.max-size=1", "spring.task.execution.pool.queue-capacity=5")) {
            String outcome = context.getBean(PackingService.class).packAndWaitForALabel().get(10, TimeUnit.SECONDS);
            assertTrue(outcome.startsWith("starved"), outcome);
        }
    }

    @Test
    void withTwoThreadsTheSameNestedWaitSucceeds() throws Exception {
        try (ConfigurableApplicationContext context = PackingApplication.start("spring.task.execution.pool.core-size=2",
                "spring.task.execution.pool.max-size=2", "spring.task.execution.pool.queue-capacity=5")) {
            assertEquals("label printed", context.getBean(PackingService.class).packAndWaitForALabel().get(10, TimeUnit.SECONDS));
        }
    }
}
