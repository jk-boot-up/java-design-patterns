package com.jk.explore.singleton;

import java.util.concurrent.atomic.AtomicLong;

/**
 * The order-number sequencer used everywhere in the checkout flow.
 *
 * <p>Every part of the system that issues an order number must issue it
 * from the same counter, or two different code paths can hand out the same
 * number to two different customers. That is a correctness requirement,
 * not a style preference, which is exactly the situation the singleton
 * pattern exists for: guarantee, in code, that a class has exactly one
 * instance, and hand out one well-known way to reach it.
 *
 * <p>This is an enum with a single constant, which <i>Effective Java</i>
 * Item 3 recommends as the best way to implement a singleton in Java. The
 * language itself enforces the "exactly one instance" guarantee here: the
 * JVM creates enum constants exactly once, reflection is barred from
 * calling an enum's constructor, and enum serialization is defined in
 * terms of the constant's name rather than its fields, so a
 * deserialized enum singleton is the same instance, not a copy.
 */
public enum OrderSequenceGenerator {

    INSTANCE;

    private final AtomicLong counter = new AtomicLong();

    public String nextOrderNumber() {
        return String.format("ORD-%06d", counter.incrementAndGet());
    }
}
