package com.jk.explore.splitteraggregator;

import java.util.ArrayList;
import java.util.List;

/** Breaks an order into one message per line, each carrying the order's id and its own place: line 2 of 3. */
public final class Splitter {

    private Splitter() {
    }

    public static List<Part> split(String orderId, List<String> lines) {
        List<Part> parts = new ArrayList<>();
        for (int i = 0; i < lines.size(); i++) {
            parts.add(new Part(orderId, i + 1, lines.size(), lines.get(i)));
        }
        return parts;
    }
}
