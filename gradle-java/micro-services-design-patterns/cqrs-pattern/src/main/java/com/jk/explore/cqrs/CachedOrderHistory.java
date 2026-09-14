package com.jk.explore.cqrs;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The cache people reach for instead of a read model, and it very nearly works.
 *
 * A five-minute expiry over the composed page. The first view is slow, the next few
 * hundred are instant, and the code is fifteen lines. Every test in
 * {@code CachedOrderHistoryTest} passes.
 *
 * <p>The difference from a read model is not speed and it is not staleness — both are
 * stale. It is *why* each one is stale, and how long for.
 *
 * <p>A read model is out of date for as long as an event takes to be delivered, and it is
 * corrected by the event that made it wrong. A cache is out of date for however long its
 * timer says, whatever happens: the customer places an order, the cache knows nothing
 * about it, and it will keep serving the page from before the order for the rest of the
 * five minutes. It cannot know it is wrong, because nothing tells it. Lowering the expiry
 * to a second does not fix that, it just pays for the composition again every second.
 */
public final class CachedOrderHistory {

    public static final long EXPIRY_MILLIS = 5 * 60 * 1000L;

    private record CachedPage(List<OrderHistoryRow> rows, long storedAtMillis) {
    }

    private final ComposingOrderHistory composer;
    private final SimulatedClock clock;
    private final CallLog log;
    private final Map<String, CachedPage> pages = new LinkedHashMap<>();
    private int hits;
    private int misses;

    public CachedOrderHistory(ComposingOrderHistory composer, SimulatedClock clock,
                              CallLog log) {
        this.composer = composer;
        this.clock = clock;
        this.log = log;
    }

    public List<OrderHistoryRow> historyFor(String customerId) {
        CachedPage cached = pages.get(customerId);
        if (cached != null && clock.millis() - cached.storedAtMillis() < EXPIRY_MILLIS) {
            hits++;
            log.note("Cache", "HIT", "page from "
                    + (clock.millis() - cached.storedAtMillis()) + "ms ago");
            return cached.rows();
        }

        misses++;
        log.note("Cache", "MISS", "composing the page again");
        List<OrderHistoryRow> rows = composer.historyFor(customerId);
        pages.put(customerId, new CachedPage(rows, clock.millis()));
        return rows;
    }

    public int hits() {
        return hits;
    }

    public int misses() {
        return misses;
    }
}
