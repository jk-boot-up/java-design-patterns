package com.jk.explore.proxyspring;

import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * The expensive real subject: every construction is counted. Both this class and the
 * injection point say {@code @Lazy}: one alone would still build it at startup.
 */
@Lazy
@Component
public class HighResolutionImage {

    static final AtomicInteger LOADS = new AtomicInteger();

    public HighResolutionImage() {
        LOADS.incrementAndGet();
    }

    public String pixels(String sku) {
        return "full-resolution pixels of " + sku;
    }
}
