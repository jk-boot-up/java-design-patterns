package com.jk.explore.bulkhead;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * A timeline of what happened, in a form that is safe to write to from many threads.
 *
 * Every other project in this category uses a simulated clock, because time there is
 * something the test controls. This one cannot: it is about threads genuinely
 * waiting for each other, so the clock has to be the real one. That is also why this
 * log is a {@link CopyOnWriteArrayList} rather than a plain list — several worker
 * threads write to it at once, and a plain {@code ArrayList} would quietly lose
 * entries or corrupt itself.
 */
public final class JobLog {

    /** One thing that happened, at a real number of milliseconds since the run began. */
    public record Entry(long atMillis, String pool, String job, String what) {
    }

    private final List<Entry> entries = new CopyOnWriteArrayList<>();
    private final long startedAt = System.currentTimeMillis();

    public void note(String pool, String job, String what) {
        entries.add(new Entry(System.currentTimeMillis() - startedAt, pool, job, what));
    }

    public List<Entry> entries() {
        return List.copyOf(entries);
    }

    /** How many entries this pool wrote. */
    public long countFor(String pool) {
        return entries.stream().filter(e -> e.pool().equals(pool)).count();
    }

    public boolean contains(String what) {
        return entries.stream().anyMatch(e -> e.what().contains(what));
    }

    /**
     * The timeline, ordered by when things happened.
     *
     * Real timestamps wobble by a millisecond or two between runs, so the demo prints
     * them rounded to the nearest ten. The shape is the lesson, not the digits.
     */
    public String timeline() {
        StringBuilder out = new StringBuilder();
        entries.stream()
                .sorted((a, b) -> Long.compare(a.atMillis(), b.atMillis()))
                .forEach(e -> out.append(String.format("  ~%4dms  %-10s %-14s %s%n",
                        Math.round(e.atMillis() / 10.0) * 10, e.pool(), e.job(), e.what())));
        return out.toString();
    }
}
