package com.jk.explore.monitorobject.pattern;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * <strong>The classic wait mistake: {@code if} where {@code while} belongs.</strong>
 * A woken thread has been told stock <em>may</em> be there, not that it
 * <em>is</em>. Another woken thread can get in first. The only safe habit
 * is to check again after every wake-up, which is what a loop does.
 */
public final class IfInsteadOfWhile {

    private IfInsteadOfWhile() {
    }

    /** A stock whose {@code take} checks once. */
    public static final class BrokenStock {
        private final ReentrantLock lock = new ReentrantLock();
        private final Condition stockAdded = lock.newCondition();
        private int count;

        public void take(int wanted) throws InterruptedException {
            lock.lockInterruptibly();
            try {
                if (count < wanted) {
                    stockAdded.await();
                }
                count -= wanted;
            } finally {
                lock.unlock();
            }
        }

        public void add(int amount) {
            lock.lock();
            try {
                count += amount;
                stockAdded.signalAll();
            } finally {
                lock.unlock();
            }
        }

        public int available() {
            lock.lock();
            try {
                return count;
            } finally {
                lock.unlock();
            }
        }

        public boolean hasWaiters() {
            lock.lock();
            try {
                return lock.hasWaiters(stockAdded);
            } finally {
                lock.unlock();
            }
        }

        public int waiterCount() {
            lock.lock();
            try {
                return lock.getWaitQueueLength(stockAdded);
            } finally {
                lock.unlock();
            }
        }
    }

    /**
     * Two takers wait for one item each; one item is added. Returns the
     * final count: -1 for the broken stock, 0 for a correct one.
     */
    public static int twoTakersOneItem(BrokenStock stock) throws InterruptedException {
        Thread a = new Thread(() -> take(stock));
        Thread b = new Thread(() -> take(stock));
        a.start();
        b.start();
        while (stock.waiterCount() < 2) {
            Thread.onSpinWait();
        }
        stock.add(1);
        a.join(2_000);
        b.join(2_000);
        return stock.available();
    }

    private static void take(BrokenStock stock) {
        try {
            stock.take(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
