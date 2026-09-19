package com.jk.explore.singletonspring;

import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

/**
 * The order-number sequencer from the hand-built singleton project, now a Spring bean.
 * Nothing here is private or static: Spring keeps one instance per container, and the
 * plain public constructor is what lets anyone else make another.
 */
@Component
public class OrderSequenceGenerator {

    /** How many instances have ever been built, so the demo can show when. */
    static final AtomicInteger BUILT = new AtomicInteger();

    private final AtomicLong counter = new AtomicLong();

    public OrderSequenceGenerator() {
        BUILT.incrementAndGet();
    }

    public String nextOrderNumber() {
        return String.format("ORD-%06d", counter.incrementAndGet());
    }
}
