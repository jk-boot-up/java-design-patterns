package com.jk.explore.contentenricher;

import java.util.List;

/**
 * The thin message checkout sends: which order, which customer id, and the items.
 */
public record OrderPlaced(String orderId, String customerId, List<String> items) {

    /** Roughly how big the message is on the wire, in characters. */
    public int size() {
        return toString().length();
    }
}
