package com.jk.explore.observer;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.function.Consumer;

/**
 * Appends a line to the feed the warehouse polls, for the two statuses the
 * warehouse acts on.
 *
 * <p>It keeps the lines it wrote so a test can read them back without a file
 * system, and so the demo can show that a listener may hold state of its own.
 */
public final class WarehouseFeedListener implements OrderListener {

    private final Consumer<String> sink;
    private final List<String> feed = new ArrayList<>();

    public WarehouseFeedListener(Consumer<String> sink) {
        this.sink = Objects.requireNonNull(sink, "sink");
    }

    @Override
    public String name() {
        return "warehouse-feed";
    }

    @Override
    public void onStatusChanged(OrderEvent event) {
        if (event.to() != OrderStatus.PAID && event.to() != OrderStatus.SHIPPED) {
            return;
        }
        String line = event.orderId() + "," + event.to().name();
        feed.add(line);
        sink.accept("  [warehouse-feed] wrote \"" + line + "\"");
    }

    /** The lines written so far, oldest first. */
    public List<String> feed() {
        return List.copyOf(feed);
    }
}
