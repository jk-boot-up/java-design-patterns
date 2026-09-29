package com.jk.explore.pollingconsumer;

import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * The pattern: the consumer decides when to take messages. Each time it is ready, it asks the queue for as many as it can handle.
 *
 * <p>Messages wait safely in the queue until the consumer polls, so a burst
 * cannot overwhelm it, and pausing is simply not polling.
 */
public final class PollingConsumer {

    private final Deque<String> queue;
    private final LabelPrinter printer;
    private boolean paused;
    private int polls;
    private int emptyPolls;

    public PollingConsumer(Deque<String> queue, LabelPrinter printer) {
        this.queue = queue;
        this.printer = printer;
    }

    /** One tick: if not paused, take up to what the printer can do this tick, and print it. */
    public int tick() {
        if (paused) {
            return 0;
        }
        polls++;
        List<String> batch = new ArrayList<>();
        while (batch.size() < LabelPrinter.PER_TICK && !queue.isEmpty()) {
            batch.add(queue.poll());
        }
        if (batch.isEmpty()) {
            emptyPolls++;
        }
        printer.print(batch);
        return batch.size();
    }

    public void pause() {
        paused = true;
    }

    public void resume() {
        paused = false;
    }

    public int polls() {
        return polls;
    }

    public int emptyPolls() {
        return emptyPolls;
    }
}
