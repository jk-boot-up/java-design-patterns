package com.jk.explore.contentenricher;

import java.util.List;

/**
 * The same order with the customer's details added, so no receiver has to look them up.
 */
public record EnrichedOrder(String orderId, String customerId, List<String> items,
                            String name, String address, String tier) {

    public int size() {
        return toString().length();
    }
}
