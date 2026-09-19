package com.jk.explore.loadleveling;

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.function.IntUnaryOperator;

/**
 * A model of orders arriving and a worker that can process a fixed number each tick. One tick is one step.
 * With no queue, an order that arrives when the worker is full is refused. With a queue, it waits its turn.
 * Everything is integer arithmetic, so a run gives the same answer every time.
 */
public final class Sim {

    private Sim() {
    }

    /** No queue: the worker handles up to {@code capacity} orders a tick and refuses the rest. */
    public static Result direct(IntUnaryOperator arrivalsAtTick, int capacity, int ticks) {
        int arrived = 0;
        int processed = 0;
        int rejected = 0;
        for (int t = 0; t < ticks; t++) {
            int now = arrivalsAtTick.applyAsInt(t);
            arrived += now;
            int served = Math.min(now, capacity);
            processed += served;
            rejected += now - served;
        }
        return new Result(arrived, processed, rejected, 0, 0, 0, 0, 0);
    }

    /**
     * A queue between arrivals and the worker. {@code queueLimit} of 0 or less means the queue has no limit.
     * If {@code crashAtTick} is not negative, the queue is in memory and everything waiting at that tick is lost.
     */
    public static Result queued(IntUnaryOperator arrivalsAtTick, int capacity, int queueLimit, int ticks, int crashAtTick) {
        Queue<Integer> waiting = new ArrayDeque<>();
        int arrived = 0;
        int processed = 0;
        int rejected = 0;
        int lost = 0;
        int maxDepth = 0;
        int maxWait = 0;
        long totalWait = 0;
        for (int t = 0; t < ticks; t++) {
            int now = arrivalsAtTick.applyAsInt(t);
            arrived += now;
            for (int i = 0; i < now; i++) {
                if (queueLimit > 0 && waiting.size() >= queueLimit) {
                    rejected++;
                } else {
                    waiting.add(t);
                }
            }
            maxDepth = Math.max(maxDepth, waiting.size());
            if (t == crashAtTick) {
                lost += waiting.size();
                waiting.clear();
            }
            for (int i = 0; i < capacity && !waiting.isEmpty(); i++) {
                int waited = t - waiting.poll();
                processed++;
                maxWait = Math.max(maxWait, waited);
                totalWait += waited;
            }
        }
        return new Result(arrived, processed, rejected, lost, maxDepth, maxWait, processed == 0 ? 0 : (double) totalWait / processed, waiting.size());
    }

    /** All the orders arrive at tick zero. */
    public static IntUnaryOperator burst(int orders) {
        return t -> t == 0 ? orders : 0;
    }

    /** The same number of orders every tick. */
    public static IntUnaryOperator steady(int perTick) {
        return t -> perTick;
    }
}
