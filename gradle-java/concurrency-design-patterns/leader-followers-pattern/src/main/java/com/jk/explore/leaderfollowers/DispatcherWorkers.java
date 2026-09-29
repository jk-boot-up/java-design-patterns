package com.jk.explore.leaderfollowers;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * Without the pattern: one dispatcher thread receives every message and hands it to a worker through a second queue.
 *
 * <p>Every message changes threads once, and the dispatcher does no order
 * work itself.
 */
public final class DispatcherWorkers {

    private final BlockingQueue<Message> source;
    private final BlockingQueue<Object[]> handOff = new LinkedBlockingQueue<>();
    private final Record record = new Record();
    private final List<Thread> threads = new ArrayList<>();
    private int handOffs;

    public DispatcherWorkers(BlockingQueue<Message> source, int workers) {
        this.source = source;
        threads.add(new Thread(this::dispatch, "dispatcher"));
        for (int i = 1; i <= workers; i++) {
            threads.add(new Thread(this::work, "worker-" + i));
        }
    }

    private void dispatch() {
        try {
            while (true) {
                Message m = source.take();
                if (m == Message.STOP) {
                    for (int i = 1; i < threads.size(); i++) {
                        handOff.put(new Object[] {Message.STOP, null});
                    }
                    return;
                }
                handOffs++;
                handOff.put(new Object[] {m, Thread.currentThread().getName()});
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void work() {
        try {
            while (true) {
                Object[] item = handOff.take();
                if (item[0] == Message.STOP) {
                    return;
                }
                record.handled((Message) item[0], (String) item[1]);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public void runUntilStopped() throws InterruptedException {
        threads.forEach(Thread::start);
        for (Thread t : threads) {
            t.join();
        }
    }

    public Record record() {
        return record;
    }

    public int handOffs() {
        return handOffs;
    }

    public int threadCount() {
        return threads.size();
    }
}
