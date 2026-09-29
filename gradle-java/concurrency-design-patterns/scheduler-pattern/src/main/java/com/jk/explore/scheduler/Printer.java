package com.jk.explore.scheduler;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.locks.ReentrantLock;

/**
 * The warehouse's one label printer, and packing stations that each send it one job, a little apart.
 */
public final class Printer {

    /** Something that decides whose turn it is: a fair lock, or the scheduler. */
    public interface Gate {
        void enter(PrintJob job) throws InterruptedException;

        void done();
    }

    /** Without the pattern: a fair lock serves jobs strictly in the order they arrived. */
    public static Gate fairLock() {
        ReentrantLock lock = new ReentrantLock(true);
        return new Gate() {
            public void enter(PrintJob job) {
                lock.lock();
            }

            public void done() {
                lock.unlock();
            }
        };
    }

    public static Gate scheduler(Scheduler s) {
        return new Gate() {
            public void enter(PrintJob job) throws InterruptedException {
                s.enter(job);
            }

            public void done() {
                s.done();
            }
        };
    }

    /**
     * The printer is busy with a bulk job while the other stations send theirs, 20 ms apart.
     * Returns the order the waiting jobs were printed in.
     */
    public static List<String> run(Gate gate, List<Object[]> jobs) throws InterruptedException {
        List<String> printed = new CopyOnWriteArrayList<>();
        List<Thread> stations = new ArrayList<>();
        PrintJob bulk = new PrintJob("BULK-0", false, 50, 0);
        Thread first = new Thread(() -> use(gate, bulk, 300, null));
        first.start();
        Thread.sleep(30);
        long t = 1;
        for (Object[] spec : jobs) {
            PrintJob job = new PrintJob((String) spec[0], (Boolean) spec[1], (Integer) spec[2], t++);
            Thread s = new Thread(() -> use(gate, job, 10, printed));
            stations.add(s);
            s.start();
            Thread.sleep(20);
        }
        first.join();
        for (Thread s : stations) {
            s.join();
        }
        return printed;
    }

    private static void use(Gate gate, PrintJob job, long ms, List<String> printed) {
        try {
            gate.enter(job);
            try {
                if (printed != null) {
                    printed.add(job.id());
                }
                Thread.sleep(ms);
            } finally {
                gate.done();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private Printer() {
    }
}
