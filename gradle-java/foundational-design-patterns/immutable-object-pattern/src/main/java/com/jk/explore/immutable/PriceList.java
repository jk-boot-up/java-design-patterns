package com.jk.explore.immutable;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The pattern: a price list that never changes once made. A sale builds a whole new list.
 *
 * <p>The constructor copies the map it is given, so whoever passed it in
 * cannot change this list afterwards, and {@link #prices()} hands out a
 * read-only view.
 */
public final class PriceList {

    private final Map<String, Long> pence;

    public PriceList(Map<String, Long> prices) {
        this.pence = Map.copyOf(prices);
    }

    /** A new list with every price reduced by {@code percent}; this one is untouched. */
    public PriceList withSale(int percent) {
        Map<String, Long> next = new LinkedHashMap<>();
        pence.forEach((item, p) -> next.put(item, p * (100 - percent) / 100));
        return new PriceList(next);
    }

    /** A new list with one price changed; every other entry is copied across. */
    public PriceList withPrice(String item, long price) {
        Map<String, Long> next = new LinkedHashMap<>(pence);
        next.put(item, price);
        return new PriceList(next);
    }

    public long total(List<String> basket) {
        return basket.stream().mapToLong(pence::get).sum();
    }

    public Map<String, Long> prices() {
        return pence;
    }

    public int size() {
        return pence.size();
    }
}
