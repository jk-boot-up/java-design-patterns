package com.jk.explore.threadpool;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.domain.Packing;
import com.jk.explore.threadpool.harness.Gate;
import com.jk.explore.threadpool.naive.ThreadPerOrderPacking;
import com.jk.explore.threadpool.naive.UnboundedPoolPacking;
import com.jk.explore.threadpool.pattern.BoundedPackingPool;
import com.jk.explore.threadpool.pattern.PoolStarvation;
import com.jk.explore.threadpool.pattern.VirtualThreadFlood;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Six acts. The only deliberate delay anywhere in this class is
 * {@link #PACK_MILLIS} — the same named, measured subject §46 introduced —
 * plus the demonstration timeout in act five, which is the rescue from a
 * genuine deadlock, not a wait for anything to finish.
 */
public final class PackingTeamDemo {

    /** How long packing one order takes. Named and printed, never hidden. */
    private static final long PACK_MILLIS = 40;

    private static final Packing REAL_PACKING = order -> {
        try {
            Thread.sleep(PACK_MILLIS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    };

    public static void main(String[] args) throws InterruptedException {
        System.out.println("THREAD POOL — a packing team, sized on purpose\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() throws InterruptedException {
        System.out.println("ONE. A thread per order — the same cost §46 measured, from the team's side.");
        Gate hold = new Gate();
        int sample = 2_000;
        ThreadPerOrderPacking.FloodResult result = ThreadPerOrderPacking.floodSafely(sample, hold);
        System.out.printf("  created %,d real threads in %.1fms (%.1f microseconds each)%n",
                result.threadsCreated(), result.totalCreateNanos() / 1_000_000.0,
                result.avgCreateMicros());
        System.out.println("  every thread is live and holding a stack until its order is packed —");
        System.out.println("  nothing here caps how many pile up if orders outpace packing.");
        System.out.println();
    }

    private static void actTwo() throws InterruptedException {
        System.out.println("TWO. A fixed pool with the queue nobody chose — the default trap.");
        UnboundedPoolPacking pool = new UnboundedPoolPacking(2);
        Gate workerHold = new Gate();
        CountDownLatch workersStarted = new CountDownLatch(2);
        for (int i = 0; i < 2; i++) {
            pool.raw().execute(() -> {
                workersStarted.countDown();
                try {
                    workerHold.awaitOpen();
                } catch (IllegalStateException e) {
                    // interrupted by this act's own cleanup below — expected, this act
                    // never opens the gate, it only proves the backlog number.
                }
            });
        }
        workersStarted.await();

        int burst = 500;
        for (int i = 1; i <= burst; i++) {
            pool.submit(new Order("ord-" + i, "BNS-220"), REAL_PACKING);
        }
        System.out.println("  2 workers, both provably busy; " + burst + " more orders submitted");
        System.out.println("  Executors.newFixedThreadPool never blocked and never rejected once");
        System.out.println("  backlog waiting behind the 2 busy workers: " + pool.backlog());
        System.out.println("  nothing anywhere would have told you that number until you asked.");

        pool.raw().shutdownNow();
        pool.raw().awaitTermination(2, TimeUnit.SECONDS);
        System.out.println();
    }

    private static void actThree() throws InterruptedException {
        System.out.println("THREE. The pattern — a bound on workers, and a bound on the queue.");
        BoundedPackingPool pool = new BoundedPackingPool(1, 3);
        Gate workerHold = new Gate();
        CountDownLatch workerStarted = new CountDownLatch(1);
        pool.submitRaw(() -> {
            workerStarted.countDown();
            workerHold.awaitOpen();
        });
        workerStarted.await();

        for (int i = 1; i <= 3; i++) {
            pool.submit(new Order("ord-" + i, "BNS-220"), REAL_PACKING);
        }
        System.out.println("  1 worker busy, queue filled to capacity 3: " + pool.queueDepth());

        pool.submit(new Order("ord-overflow", "BNS-220"), REAL_PACKING);
        System.out.println("  one more order, submitted with the worker busy and the queue full: "
                + (pool.rejectedCount() > 0 ? "REJECTED on the spot — no patience window, no room" : "accepted"));

        workerHold.open();
        pool.close();
        System.out.println();
    }

    private static void actFour() {
        System.out.println("FOUR. Sizing the pool is a real decision, both directions.");
        System.out.println("  too few workers: the queue in act two grew by 500 before anyone asked why.");
        System.out.println("  too many workers: each one is a stack, same cost as act one, just capped.");
        System.out.println("  there is no size that is free; there is only a size chosen on purpose.");
        System.out.println();
    }

    private static void actFive() throws InterruptedException {
        System.out.println("FIVE. Pool starvation — a task waiting on a task in its own pool.");
        ExecutorService pool = Executors.newFixedThreadPool(1);
        PoolStarvation.Outcome outcome = PoolStarvation.attemptNestedSubmit(pool, 200);
        System.out.println("  a fixed pool of 1: the running task submits a second task to that");
        System.out.println("  same pool and waits for its result — no free worker will ever run it.");
        System.out.println("  starved: " + outcome.starved() + ", rescued after "
                + outcome.waitedMillis() + "ms by a demonstration timeout; left alone, this never resolves.");
        pool.shutdownNow();
        pool.awaitTermination(2, TimeUnit.SECONDS);
        System.out.println();
    }

    private static void actSix() throws InterruptedException {
        System.out.println("SIX. Java's answer — virtual threads change the creation cost, not the bound.");
        Gate hold = new Gate();
        int sample = 2_000;
        VirtualThreadFlood.FloodResult result = VirtualThreadFlood.floodSafely(sample, hold);
        System.out.printf("  created %,d virtual threads in %.1fms (%.2f microseconds each)%n",
                result.threadsCreated(), result.totalCreateNanos() / 1_000_000.0,
                result.avgCreateMicros());
        System.out.println("  compare act one: same count, real platform threads, measured the same way.");
        System.out.println("  cheap thread-per-task is viable again for blocking I/O — but a pool still");
        System.out.println("  bounds a resource, not a thread count; a downstream limit of ten stays ten");
        System.out.println("  connections wide no matter how many virtual threads ask for one.");
    }
}
