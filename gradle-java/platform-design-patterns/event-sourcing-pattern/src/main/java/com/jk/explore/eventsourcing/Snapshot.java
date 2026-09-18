package com.jk.explore.eventsourcing;

/**
 * A balance that was true at one point in the log, saved so nobody has to fold
 * from the beginning again.
 *
 * <p>{@code upToPosition} is the part people get wrong. A snapshot without a
 * position is useless, because there is no way to tell which events it already
 * includes — so you either double-count them or you throw the snapshot away.
 * "The balance was 140 as at event 4,000" is a usable fact; "the balance was 140"
 * is not.
 *
 * <p>{@code computedBy} is not something a real snapshot usually carries, and
 * this project gives it one deliberately. A snapshot is a conclusion, and a
 * conclusion is only as good as the code that reached it. When that code turns
 * out to have had a bug, every snapshot it wrote is wrong, and the only way to
 * know which ones is to have recorded who did the arithmetic.
 */
public record Snapshot(String customerId, int balance, int upToPosition,
                       String computedBy) {

    @Override
    public String toString() {
        return customerId + " = " + balance + " points, as at event " + upToPosition
                + ", computed by " + computedBy;
    }
}
