package com.jk.explore.proxy;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * The real subject. Standing in for something genuinely expensive to create
 * -- pulling a multi-megabyte asset from the CDN and decoding it -- modelled
 * here as a counter rather than an actual delay, so the cost is still
 * observable without making the tests slow.
 */
public final class HighResolutionProductImage implements ProductImage {

    private static final AtomicInteger LOAD_COUNT = new AtomicInteger();

    private final String sku;

    public HighResolutionProductImage(String sku) {
        this.sku = sku;
        LOAD_COUNT.incrementAndGet();
    }

    public static int loadCount() {
        return LOAD_COUNT.get();
    }

    public static void resetLoadCount() {
        LOAD_COUNT.set(0);
    }

    @Override
    public String render() {
        return "Rendering " + sku + " hero image (1920x1080)";
    }

    @Override
    public String sku() {
        return sku;
    }
}
