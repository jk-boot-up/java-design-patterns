package com.jk.explore.tracingjaeger;

import io.opentelemetry.sdk.trace.IdGenerator;
import java.util.SplittableRandom;

/**
 * Trace ids and span ids from a seeded random sequence, so that two runs print the same ids.
 *
 * <p>A real service uses {@link IdGenerator#random()}, and so does everything this project
 * teaches: the ids still look random, still differ between every trace in a run, and are still
 * what the sampler looks at when it decides what to keep. The only difference is that the
 * sequence starts from a fixed seed, so the headers the documents quote are the headers the
 * program prints.
 */
final class SeededIds implements IdGenerator {

    private final SplittableRandom random;

    SeededIds(long seed) {
        this.random = new SplittableRandom(seed);
    }

    @Override
    public synchronized String generateSpanId() {
        long id;
        do {
            id = random.nextLong();
        } while (id == 0);
        return String.format("%016x", id);
    }

    @Override
    public synchronized String generateTraceId() {
        long high = random.nextLong();
        long low;
        do {
            low = random.nextLong();
        } while (low == 0);
        return String.format("%016x%016x", high, low);
    }
}
