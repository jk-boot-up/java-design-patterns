package com.jk.explore.resequencercamel;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The customer's order-tracking page: it shows each status update as it is applied.
 */
public final class OrderPage {

    private final List<String> shown = new CopyOnWriteArrayList<>();

    public void apply(String line) {
        shown.add(line);
    }

    public List<String> shown() {
        return shown;
    }

    public String latest() {
        return shown.isEmpty() ? "(nothing yet)" : shown.get(shown.size() - 1);
    }

    /** Waits, up to a limit, until {@code count} updates are shown. Never a fixed sleep. */
    public boolean await(int count, long timeoutMillis) throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        while (shown.size() < count && System.currentTimeMillis() < deadline) {
            Thread.sleep(5);
        }
        return shown.size() >= count;
    }
}
