package com.jk.explore.aggregate.naive;

import java.util.concurrent.atomic.AtomicInteger;

/** A customer read from storage. Reading one is counted, because it is the expensive part. */
public record CustomerRecord(String id, String name) {

    public static final AtomicInteger LOADS = new AtomicInteger();

    public static CustomerRecord load(String id) {
        LOADS.incrementAndGet();
        return new CustomerRecord(id, "Ada");
    }
}
