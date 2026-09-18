package com.jk.explore.tracing;

/**
 * One unit of work, timed, and told who asked for it.
 *
 * <p>A span is the whole of tracing's data model, and it is four things. A
 * <strong>name</strong>, so you know what the work was. A <strong>start</strong>
 * and a <strong>duration</strong>, so you know when it happened and how long it
 * took. And a <strong>parent</strong> — the span that caused this one — which is
 * the field that turns a pile of timings into a shape.
 *
 * <p>That last field is worth sitting with, because it is the one people leave
 * out when they build this themselves. Timestamps in a log tell you when things
 * happened. They do not tell you that the pricing call happened
 * <em>because of</em> the product page request, and without that you cannot add
 * anything up, because you cannot tell which of the four hundred requests in
 * flight this line belongs to.
 *
 * @param traceId      shared by every span in one customer's request
 * @param spanId       unique to this span
 * @param parentSpanId the span that caused this one, or {@code null} for the
 *                     root span at the front door
 * @param name         what the work was, e.g. {@code "pricing"}
 * @param startMillis  when it started, measured from the start of the request
 * @param durationMillis how long it took
 */
public record Span(String traceId,
                   String spanId,
                   String parentSpanId,
                   String name,
                   long startMillis,
                   long durationMillis) {

    public Span {
        if (traceId == null || traceId.isBlank()) {
            throw new IllegalArgumentException("a span must belong to a trace");
        }
        if (spanId == null || spanId.isBlank()) {
            throw new IllegalArgumentException("a span must have an id");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("a span must say what the work was");
        }
        if (durationMillis < 0) {
            throw new IllegalArgumentException("a span cannot last negative time");
        }
    }

    /** When the work finished. */
    public long endMillis() {
        return startMillis + durationMillis;
    }

    /** True for the span created at the front door, which has no parent. */
    public boolean isRoot() {
        return parentSpanId == null;
    }
}
