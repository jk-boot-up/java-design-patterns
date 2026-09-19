package com.jk.explore.doublechecked;

import java.util.concurrent.atomic.AtomicInteger;

/** Something expensive to build that the whole shop shares: it is created lazily, and every build is counted. */
public class PriceList {

    public static final AtomicInteger BUILT = new AtomicInteger();

    public PriceList() {
        BUILT.incrementAndGet();
    }

    public int priceOf(String sku) {
        return sku.startsWith("ESP") ? 30000 : 800;
    }
}
