package com.jk.explore.spacebased;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Keeps the units' copies in step: every change is queued, then copied to every other unit and handed to the database writer.
 *
 * <p>Replication is not instant: until {@link #flush} runs, other units have
 * not heard about a sale. That gap is what the pattern trades for speed.
 */
public final class DataGrid {

    private record Change(ProcessingUnit from, int sold) {
    }

    private final List<ProcessingUnit> units = new ArrayList<>();
    private final ConcurrentLinkedQueue<Change> pending = new ConcurrentLinkedQueue<>();
    private final DataWriter writer;

    public DataGrid(DataWriter writer) {
        this.writer = writer;
    }

    public void join(ProcessingUnit unit) {
        units.add(unit);
    }

    void sold(ProcessingUnit from, int sold) {
        pending.add(new Change(from, sold));
    }

    /** Copies every waiting change to the other units and to the database writer. */
    public synchronized void flush() {
        Change c;
        while ((c = pending.poll()) != null) {
            for (ProcessingUnit u : units) {
                if (u != c.from()) {
                    u.applyFromOthers(c.sold());
                }
            }
            writer.record(c.sold());
        }
        writer.flush();
    }
}
