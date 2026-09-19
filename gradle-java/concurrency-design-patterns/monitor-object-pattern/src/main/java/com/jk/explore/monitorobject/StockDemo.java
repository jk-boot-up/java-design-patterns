package com.jk.explore.monitorobject;

import com.jk.explore.monitorobject.harness.Gate;
import com.jk.explore.monitorobject.harness.Rendezvous;
import com.jk.explore.monitorobject.naive.CallerLockedStock;
import com.jk.explore.monitorobject.naive.PlainStock;
import com.jk.explore.monitorobject.naive.VolatileStock;
import com.jk.explore.monitorobject.pattern.IfInsteadOfWhile;
import com.jk.explore.monitorobject.pattern.MonitorHazards;
import com.jk.explore.monitorobject.pattern.StockMonitor;

/**
 * Six acts. No act calls {@code Thread.sleep} to wait for another thread;
 * every race is forced with a rendezvous, a gate or a wait queue's own
 * length.
 */
public final class StockDemo {

    private static final int CHECKOUT_THREADS = 8;
    private static final int SALES_PER_THREAD = 25_000;

    public static void main(String[] args) throws InterruptedException {
        System.out.println("MONITOR OBJECT — the object that guards itself\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() throws InterruptedException {
        System.out.println("ONE. A plain count — the lost update.");
        Rendezvous bothRead = new Rendezvous("both-read", 2);
        PlainStock stock = new PlainStock(10, bothRead::meet);
        runTwo(stock::sellOne);
        System.out.println("  stock started at 10; two checkout threads each sold one");
        System.out.println("  stock now: " + stock.available() + " — two items sold, one gone from the count.\n");
    }

    private static void actTwo() throws InterruptedException {
        System.out.println("TWO. volatile — visible, but still not atomic.");
        Rendezvous bothRead = new Rendezvous("both-read", 2);
        VolatileStock stock = new VolatileStock(10, bothRead::meet);
        runTwo(stock::sellOne);
        System.out.println("  stock now: " + stock.available() + " — the same lost update, with volatile.");
        System.out.println("  volatile promises other threads see a write. It does not");
        System.out.println("  make read-subtract-write one step.\n");
    }

    private static void actThree() throws InterruptedException {
        System.out.println("THREE. The caller holds the lock — until one forgets.");
        Rendezvous bothRead = new Rendezvous("both-read", 2);
        CallerLockedStock stock = new CallerLockedStock(10, bothRead::meet);
        runTwo(() -> {
            stock.lock().lock();
            try {
                stock.sellOne();
            } finally {
                stock.lock().unlock();
            }
        }, stock::sellOne);
        System.out.println("  one caller took the lock; one forgot.");
        System.out.println("  stock now: " + stock.available() + " — the careful caller's lock protected nothing.\n");
    }

    private static void actFour() throws InterruptedException {
        System.out.println("FOUR. The pattern — the object owns its lock.");
        int total = CHECKOUT_THREADS * SALES_PER_THREAD;
        StockMonitor stock = new StockMonitor(total);
        Gate start = new Gate();
        Thread[] threads = new Thread[CHECKOUT_THREADS];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                start.awaitOpen();
                for (int n = 0; n < SALES_PER_THREAD; n++) {
                    stock.sellOne();
                }
            });
            threads[i].start();
        }
        long began = System.nanoTime();
        start.open();
        for (Thread t : threads) {
            t.join();
        }
        long millis = (System.nanoTime() - began) / 1_000_000;
        System.out.println("  " + CHECKOUT_THREADS + " threads x " + SALES_PER_THREAD + " sales from " + total + ": "
                + stock.available() + " left, in " + millis + "ms");
        System.out.println("  no caller could forget a lock; none was theirs to take.");

        Thread taker = new Thread(() -> {
            try {
                stock.take(3);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        taker.start();
        stock.add(3);
        taker.join();
        System.out.println("  a thread waited for 3 items, was signalled by the thread that added them,");
        System.out.println("  and took them: " + stock.available() + " left.");
        System.out.println("  the cost: one lock, so one thread at a time. That is the design.\n");
    }

    private static void actFive() throws InterruptedException {
        System.out.println("FIVE. wait() in an if, not a while.");
        int broken = IfInsteadOfWhile.twoTakersOneItem(new IfInsteadOfWhile.BrokenStock());
        System.out.println("  two takers waiting, one item added, both woken.");
        System.out.println("  with if:    stock ends at " + broken + " — a sale of an item that was never there.");

        StockMonitor stock = new StockMonitor(0);
        Thread a = new Thread(() -> take(stock));
        Thread b = new Thread(() -> take(stock));
        a.start();
        b.start();
        stock.add(1);
        a.join(200);
        b.join(200);
        int stillWaiting = (a.isAlive() ? 1 : 0) + (b.isAlive() ? 1 : 0);
        System.out.println("  with while: stock ends at " + stock.available() + ", and " + stillWaiting
                + " taker is still waiting, correctly.");
        stock.add(1);
        a.join();
        b.join();
        System.out.println("  the woken thread checked again and went back to waiting.\n");
    }

    private static void actSix() throws InterruptedException {
        System.out.println("SIX. When a correct monitor still deadlocks.");
        MonitorHazards.NestedOutcome nested = MonitorHazards.nestedMonitors();
        System.out.println("  two monitors locked in opposite orders:");
        System.out.println("  deadlock detected by the JVM: " + nested.deadlockDetected()
                + ", broken by interrupting both: " + nested.rescued());
        MonitorHazards.CalloutOutcome callout = MonitorHazards.calloutWhileHoldingLock(200);
        System.out.println("  unknown code called while holding the lock, asking another thread for the stock:");
        System.out.println("  timed out: " + callout.timedOut() + ", after " + callout.waitedMillis() + "ms");
        System.out.println("  never call out to code you do not own while holding your lock.");
    }

    private static void take(StockMonitor stock) {
        try {
            stock.take(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private static void runTwo(Runnable task) throws InterruptedException {
        runTwo(task, task);
    }

    private static void runTwo(Runnable first, Runnable second) throws InterruptedException {
        Thread t1 = new Thread(first, "checkout-1");
        Thread t2 = new Thread(second, "checkout-2");
        t1.start();
        t2.start();
        t1.join(5_000);
        t2.join(5_000);
    }
}
