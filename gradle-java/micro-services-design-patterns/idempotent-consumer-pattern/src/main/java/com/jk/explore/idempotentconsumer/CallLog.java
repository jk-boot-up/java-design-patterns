package com.jk.explore.idempotentconsumer;

import java.util.ArrayList;
import java.util.List;

/**
 * The timeline of every remote call made, in the order they happened.
 *
 * This is the point of the whole project. A product page can be assembled two
 * ways that return exactly the same page, and the only way to see which one is
 * better is to look at how many calls each made, over which network, and how
 * long the caller waited. So the demo does not print the page. It prints this.
 */
public final class CallLog {

    /** One line of the timeline. */
    public record Entry(long startedAt, long finishedAt, String service,
                        String outcome, String note) {

        public long durationMillis() {
            return finishedAt - startedAt;
        }
    }

    private final SimulatedClock clock;
    private final List<Entry> entries = new ArrayList<>();

    public CallLog(SimulatedClock clock) {
        this.clock = clock;
    }

    /** Records a call that took time. The harness calls this. */
    public void record(long startedAt, long finishedAt, String service,
                       String outcome, String note) {
        entries.add(new Entry(startedAt, finishedAt, service, outcome, note));
    }

    /**
     * Records a decision rather than a call — something a pattern chose to do,
     * which took no time because no network was involved.
     */
    public void note(String service, String outcome, String note) {
        long now = clock.millis();
        entries.add(new Entry(now, now, service, outcome, note));
    }

    public List<Entry> entries() {
        return List.copyOf(entries);
    }

    /**
     * The services called, earliest first. The shape of the timeline.
     *
     * A call that contains other calls finishes after them, so it is written
     * into the log last even though it began first. Ordering by start time puts
     * it back where a reader expects it.
     */
    public List<String> services() {
        return inOrder().stream().map(Entry::service).toList();
    }

    /** How long the whole sequence took, first call started to last call ended. */
    public long elapsedMillis() {
        if (entries.isEmpty()) {
            return 0;
        }
        long start = entries.stream().mapToLong(Entry::startedAt).min().orElse(0);
        long end = entries.stream().mapToLong(Entry::finishedAt).max().orElse(0);
        return end - start;
    }

    private List<Entry> inOrder() {
        return entries.stream()
                .sorted((a, b) -> Long.compare(a.startedAt(), b.startedAt()))
                .toList();
    }

    /** How many entries a given service has. */
    public long countFor(String service) {
        return entries.stream().filter(e -> service.equals(e.service())).count();
    }

    public int size() {
        return entries.size();
    }

    public void clear() {
        entries.clear();
    }

    /** The timeline, one line per entry, ready to print. */
    public String timeline() {
        StringBuilder out = new StringBuilder();
        for (Entry e : inOrder()) {
            out.append(String.format("  %5dms -> %5dms  %-16s %-9s %s%n",
                    e.startedAt(), e.finishedAt(), e.service(), e.outcome(), e.note()));
        }
        return out.toString();
    }
}
