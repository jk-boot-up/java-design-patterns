package com.jk.explore.tracing;

/**
 * The third item on the bill: you cannot afford to keep every trace.
 *
 * <p>A shop serving a thousand requests a second, each producing six spans, is
 * asking a tracing backend to store six thousand spans a second — around half a
 * billion a day. Nobody pays for that. So you sample: keep one trace in a
 * hundred, throw the rest away before they are ever sent.
 *
 * <p>The arithmetic that follows is the uncomfortable part, and it is the reason
 * this class exists rather than a sentence in a document. Sampling is decided
 * per <em>trace</em>, at the front door, before anybody knows whether the request
 * is going to be interesting. So the one request a customer complained about has
 * a ninety-nine per cent chance of having been discarded, and it was discarded
 * for exactly the same reason as every other request: nothing about it stood out
 * yet.
 *
 * <p>You are not left with nothing — a one per cent sample is plenty for
 * "recommendations is slow on average", which is what tracing is genuinely best
 * at. What you are left without is the specific trace for the specific
 * complaint, which is what you were asked for.
 *
 * <p>The way out is <strong>tail sampling</strong>: hold the spans briefly, and
 * decide to keep the trace once you know it was slow or it failed. That costs
 * more and needs a collector that can buffer, and it is what you should reach
 * for when "we sample at one per cent" first fails you.
 */
public final class Sampler {

    /** Keep one trace in this many. */
    private final int oneIn;

    /** Deterministic, so the demo prints the same figures every run. */
    private long seen;

    public Sampler(int oneIn) {
        if (oneIn < 1) {
            throw new IllegalArgumentException("cannot keep one trace in " + oneIn);
        }
        this.oneIn = oneIn;
    }

    /**
     * Decide, at the front door, whether this trace will be recorded.
     *
     * <p>Deliberately deterministic rather than random. A real sampler hashes
     * the trace id so that every service independently reaches the same verdict
     * without talking to the others — which matters, because a request sampled
     * in by one service and out by the next produces a trace with holes in it.
     */
    public boolean keep() {
        return seen++ % oneIn == 0;
    }

    /** How many traces have been offered so far. */
    public long seen() {
        return seen;
    }

    /** How many of those were kept. */
    public long kept() {
        return (seen + oneIn - 1) / oneIn;
    }

    /** How many were thrown away, and can never be looked at again. */
    public long discarded() {
        return seen - kept();
    }

    /**
     * Whether the one trace somebody has asked about survived.
     *
     * @param traceNumber which request it was, counting from one
     */
    public boolean wouldHaveKept(long traceNumber) {
        return (traceNumber - 1) % oneIn == 0;
    }
}
