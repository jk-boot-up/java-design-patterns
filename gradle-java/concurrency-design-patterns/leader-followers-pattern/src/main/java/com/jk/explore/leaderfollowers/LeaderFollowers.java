package com.jk.explore.leaderfollowers;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

/**
 * The pattern: a pool of threads takes turns. One leader waits for the next message; the rest are followers, waiting to lead.
 *
 * <p>When the leader receives a message it hands leadership to a follower
 * (by releasing the lock) and then handles the message itself. No second
 * queue, no hand-off between threads: the thread that received a message is
 * the one that handles it.
 */
public final class LeaderFollowers {

    private final BlockingQueue<Message> source;
    private final ReentrantLock leadership = new ReentrantLock();
    private final List<Thread> threads = new ArrayList<>();
    private final Record record = new Record();
    private final AtomicInteger waitingOnSource = new AtomicInteger();
    private final AtomicInteger mostWaitingAtOnce = new AtomicInteger();
    private final AtomicInteger promotions = new AtomicInteger();

    public LeaderFollowers(BlockingQueue<Message> source, int size) {
        this.source = source;
        for (int i = 1; i <= size; i++) {
            threads.add(new Thread(this::takeTurns, "pool-" + i));
        }
    }

    private void takeTurns() {
        while (true) {
            Message m;
            leadership.lock();                 // become the leader (followers wait here)
            try {
                mostWaitingAtOnce.accumulateAndGet(waitingOnSource.incrementAndGet(), Math::max);
                m = source.take();             // only the leader waits for a message
                waitingOnSource.decrementAndGet();
                if (m == Message.STOP) {
                    source.put(Message.STOP);  // pass the stop on to the next leader
                    return;
                }
                promotions.incrementAndGet();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            } finally {
                leadership.unlock();           // promote a follower to leader
            }
            record.handled(m, Thread.currentThread().getName()); // then handle it here
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

    public int mostWaitingAtOnce() {
        return mostWaitingAtOnce.get();
    }

    public int promotions() {
        return promotions.get();
    }

    public int threadCount() {
        return threads.size();
    }
}
