package com.jk.explore.observer;

import java.util.EnumMap;
import java.util.Map;
import java.util.Objects;
import java.util.function.Consumer;

/**
 * Counts every transition, so the funnel can be reported on later.
 *
 * <p>This is the listener that shows why the pattern is worth the indirection.
 * Analytics wants every event, including ones nobody has invented yet, and it
 * wants them without the order service knowing the word "funnel". It gets
 * exactly that: a subscription, and no edit anywhere else.
 */
public final class AnalyticsListener implements OrderListener {

    private final Consumer<String> sink;
    private final Map<OrderStatus, Integer> counts = new EnumMap<>(OrderStatus.class);

    public AnalyticsListener(Consumer<String> sink) {
        this.sink = Objects.requireNonNull(sink, "sink");
    }

    @Override
    public String name() {
        return "analytics";
    }

    @Override
    public void onStatusChanged(OrderEvent event) {
        counts.merge(event.to(), 1, Integer::sum);
        sink.accept("  [analytics] recorded " + event.describe());
    }

    /** How many events have been seen for a status. */
    public int countFor(OrderStatus status) {
        return counts.getOrDefault(status, 0);
    }

    public int total() {
        return counts.values().stream().mapToInt(Integer::intValue).sum();
    }
}
