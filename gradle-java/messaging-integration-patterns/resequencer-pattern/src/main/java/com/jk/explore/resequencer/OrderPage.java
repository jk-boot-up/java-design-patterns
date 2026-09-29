package com.jk.explore.resequencer;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The customer's order page: shows the latest status it was given, and remembers what it showed.
 */
public final class OrderPage {

    private final Map<String, String> status = new HashMap<>();
    private final List<String> shown = new ArrayList<>();

    public void apply(StatusUpdate u) {
        status.put(u.orderId(), u.status());
        shown.add(u.orderId() + " " + u.status());
    }

    public String status(String orderId) {
        return status.get(orderId);
    }

    public List<String> shown() {
        return shown;
    }
}
