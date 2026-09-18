package com.jk.explore.eventsourcing;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Where saved balances live. Small class, large bill.
 *
 * <p>Snapshots are not optional once a stream is long. Folding a hundred thousand
 * events to answer a page load is not a design, and every event-sourced system of
 * any age has something like this in it. So this is not a shortcut a purist would
 * avoid — it is the second half of the pattern.
 *
 * <p>What it costs is worth stating before you need it. The balance now lives in
 * two places, and the derived copy can be wrong while the log is right: a
 * snapshot written by code that had a bug stays wrong forever, and a snapshot
 * whose position is off double-counts events. Neither failure is visible from the
 * outside, because a wrong balance looks exactly like a right one.
 *
 * <p>The rule that follows is the useful one: <strong>the log is the truth and a
 * snapshot is a cache.</strong> Anything you can rebuild you are allowed to
 * throw away, and when in doubt, {@link #discardAll} and fold again.
 */
public final class SnapshotStore {

    private final Map<String, Snapshot> byCustomer = new LinkedHashMap<>();

    public void save(Snapshot snapshot) {
        byCustomer.put(snapshot.customerId(), snapshot);
    }

    /** The saved balance for a customer, or {@code null} if there is none. */
    public Snapshot forCustomer(String customerId) {
        return byCustomer.get(customerId);
    }

    public int size() {
        return byCustomer.size();
    }

    /**
     * Throws every snapshot away.
     *
     * <p>This is the recovery move, and being able to make it without fear is the
     * whole reward for keeping the log. Every snapshot in the shop can be deleted
     * on a Tuesday afternoon and the only consequence is that the next few reads
     * are slow.
     */
    public void discardAll() {
        byCustomer.clear();
    }
}
