package com.jk.explore.splitteraggregatorcamel;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * Where finished answers land. A finished answer can appear on the thread that sent the last shipment, or on
 * the background thread that watches the clock, so waiting for one is a bounded wait on a real event: it
 * either arrives or the wait fails loudly. Nothing here ever sleeps for a fixed length of time.
 */
public class Results {

    private static final long PATIENCE_SECONDS = 20;

    private final BlockingQueue<Gathered> arrived = new LinkedBlockingQueue<>();

    public void add(Gathered gathered) {
        arrived.add(gathered);
    }

    public int size() {
        return arrived.size();
    }

    /** Waits for the next finished answer, and fails with a readable sentence rather than hanging. */
    public Gathered next() {
        try {
            Gathered g = arrived.poll(PATIENCE_SECONDS, TimeUnit.SECONDS);
            if (g == null) {
                throw new IllegalStateException(
                        "No order came out of the aggregator within " + PATIENCE_SECONDS + " seconds.");
            }
            return g;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    public List<Gathered> takeAll() {
        List<Gathered> all = new ArrayList<>();
        arrived.drainTo(all);
        return all;
    }

    public void clear() {
        arrived.clear();
    }
}
