package com.jk.explore.monitorobject.pattern;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import com.jk.explore.monitorobject.harness.Rendezvous;

/**
 * <strong>Two ways a correctly written monitor still deadlocks.</strong>
 * Neither is a bug in the monitor's own methods. Both come from how the
 * monitor is used.
 */
public final class MonitorHazards {

    private MonitorHazards() {
    }

    public record NestedOutcome(boolean deadlockDetected, boolean rescued) {
    }

    /**
     * Two threads move stock in opposite directions between two monitors.
     * Each holds its own first monitor, then asks for the other's. A
     * rendezvous makes both hold before either asks, so the deadlock
     * happens every run. It is detected by the JVM, then broken by
     * interrupting both threads.
     */
    public static NestedOutcome nestedMonitors() throws InterruptedException {
        StockMonitor a = new StockMonitor(5);
        StockMonitor b = new StockMonitor(5);
        Rendezvous bothHoldFirst = new Rendezvous("both-hold-first", 2);

        Thread t1 = new Thread(() -> transfer(a, b, bothHoldFirst), "transfer-a-to-b");
        Thread t2 = new Thread(() -> transfer(b, a, bothHoldFirst), "transfer-b-to-a");
        t1.start();
        t2.start();

        ThreadMXBean mx = ManagementFactory.getThreadMXBean();
        boolean detected = false;
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(10);
        while (System.nanoTime() < deadline) {
            long[] ids = mx.findDeadlockedThreads();
            if (ids != null && ids.length >= 2) {
                detected = true;
                break;
            }
            Thread.onSpinWait();
        }

        t1.interrupt();
        t2.interrupt();
        t1.join(2_000);
        t2.join(2_000);
        return new NestedOutcome(detected, !t1.isAlive() && !t2.isAlive());
    }

    private static void transfer(StockMonitor from, StockMonitor to, Rendezvous bothHoldFirst) {
        try {
            from.transferOneTo(to, bothHoldFirst::meet);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public record CalloutOutcome(boolean timedOut, long waitedMillis) {
    }

    /**
     * The monitor calls a listener while holding its lock. The listener
     * asks another thread to read the stock, and waits for the answer. That
     * thread needs the lock the caller is holding, so neither can move. A
     * timeout rescues the demo.
     */
    public static CalloutOutcome calloutWhileHoldingLock(long timeoutMillis) throws InterruptedException {
        StockMonitor stock = new StockMonitor(5);
        ExecutorService other = Executors.newSingleThreadExecutor(r -> {
            Thread t = new Thread(r, "reporting-thread");
            t.setDaemon(true);
            return t;
        });
        boolean[] timedOut = {false};
        long[] waited = {0};
        try {
            stock.addAndNotify(1, () -> {
                long start = System.nanoTime();
                Future<Integer> reading = other.submit(stock::available);
                try {
                    reading.get(timeoutMillis, TimeUnit.MILLISECONDS);
                } catch (TimeoutException e) {
                    timedOut[0] = true;
                    reading.cancel(true);
                } catch (Exception e) {
                    throw new IllegalStateException(e);
                }
                waited[0] = TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - start);
            });
        } finally {
            other.shutdownNow();
        }
        return new CalloutOutcome(timedOut[0], waited[0]);
    }
}
