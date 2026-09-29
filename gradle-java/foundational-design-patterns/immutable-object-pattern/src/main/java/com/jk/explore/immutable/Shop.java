package com.jk.explore.immutable;

import java.util.concurrent.atomic.AtomicReference;

/**
 * Holds the current immutable price list. Publishing a new one is a single swap, so a reader sees all old or all new.
 */
public final class Shop {

    private final AtomicReference<PriceList> current;

    public Shop(PriceList start) {
        current = new AtomicReference<>(start);
    }

    public PriceList prices() {
        return current.get();
    }

    public void publish(PriceList next) {
        current.set(next);
    }
}
