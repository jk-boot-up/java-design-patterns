package com.jk.explore.immutable;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Without the pattern: one price list shared by everyone, changed one price at a time, in place.
 */
public final class MutablePriceList {

    private final Map<String, Long> pence = new LinkedHashMap<>();

    public MutablePriceList(Map<String, Long> start) {
        pence.putAll(start);
    }

    public void set(String item, long price) {
        pence.put(item, price);
    }

    public long total(List<String> basket) {
        return basket.stream().mapToLong(pence::get).sum();
    }

    public Map<String, Long> prices() {
        return pence;
    }
}
