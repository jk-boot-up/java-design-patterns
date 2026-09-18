package com.jk.explore.tracing;

/**
 * The two identifiers that have to travel with the work.
 *
 * <p>This is the smallest and most important type in the project. Everything
 * else — the spans, the waterfall, the percentages — is bookkeeping that follows
 * automatically once these two values reach the place the work is done. If they
 * do not reach it, there is no trace, and no amount of instrumentation
 * downstream will recover it.
 *
 * <p>Notice that it is passed as an ordinary method argument throughout this
 * project. Real tracing libraries hide it in a thread-local so that your method
 * signatures stay clean, and that convenience is exactly where context gets
 * lost: a thread-local is attached to a thread, so the moment work moves to
 * another thread the context does not go with it. {@link AsyncHandoff}
 * demonstrates that, and it is the most common way a real trace breaks.
 *
 * @param traceId the customer's request, shared by every span in it
 * @param spanId  the span currently doing the work, which becomes the parent of
 *                anything it calls
 */
public record TraceContext(String traceId, String spanId) {

    public TraceContext {
        if (traceId == null || traceId.isBlank()) {
            throw new IllegalArgumentException("a context must carry a trace id");
        }
        if (spanId == null || spanId.isBlank()) {
            throw new IllegalArgumentException("a context must carry a span id");
        }
    }

    /**
     * The context a callee should receive.
     *
     * <p>Same trace, new parent: the span doing the calling becomes the parent
     * of the span being called. Getting this one line wrong is how a trace ends
     * up flat — every span a sibling of every other, with the shape that told
     * you where the time went thrown away.
     */
    public TraceContext childWith(String childSpanId) {
        return new TraceContext(traceId, childSpanId);
    }
}
