package com.jk.explore.tracing;

import java.util.ArrayList;
import java.util.List;

/**
 * Mints span ids, times the work, and collects the spans.
 *
 * <p>Usage is a try-with-resources block, which is how most real tracing
 * libraries read too:
 *
 * <pre>{@code
 * try (Tracer.Scope pricing = tracer.start(context, "pricing")) {
 *     clock.advance(180);
 * }
 * }</pre>
 *
 * <p>The closing brace is what records the span, because that is the moment the
 * duration is known. A span that is started and never closed is a span that
 * never appears, which is worth knowing: in a real system an exception thrown
 * past an un-closed span is how a trace ends up missing the very call that
 * failed. Try-with-resources is not tidiness here, it is correctness.
 *
 * <p>Ids are sequential rather than random. A real tracer uses random
 * hexadecimal so that two machines cannot collide, but random ids would make
 * this project's output different on every run, and every number in the video
 * and the documents comes from real output.
 */
public final class Tracer {

    private final String traceId;
    private final Clock clock;
    private final List<Span> spans = new ArrayList<>();
    private int nextSpanId = 1;

    public Tracer(String traceId, Clock clock) {
        this.traceId = traceId;
        this.clock = clock;
    }

    /** The trace every span from this tracer belongs to. */
    public String traceId() {
        return traceId;
    }

    /**
     * Open the root span — the one at the front door, with no parent.
     *
     * <p>Exactly one of these per customer request, and it is where the trace id
     * is minted in a real system.
     */
    public Scope startRoot(String name) {
        return new Scope(null, name);
    }

    /**
     * Open a child span of the work currently in progress.
     *
     * @param parent the context handed to this unit of work. Its span id becomes
     *               the new span's parent, which is what gives the trace its
     *               shape
     */
    public Scope start(TraceContext parent, String name) {
        return new Scope(parent.spanId(), name);
    }

    /** Everything recorded so far. */
    public Trace trace() {
        return new Trace(traceId, List.copyOf(spans));
    }

    /**
     * An open span. Closing it records the duration.
     *
     * <p>{@link #close()} declares no checked exception, so this can be used in
     * try-with-resources without forcing a catch on every call site.
     */
    public final class Scope implements AutoCloseable {

        private final String parentSpanId;
        private final String spanId;
        private final String name;
        private final long startMillis;
        private boolean closed;

        private Scope(String parentSpanId, String name) {
            this.parentSpanId = parentSpanId;
            this.spanId = "span-" + nextSpanId++;
            this.name = name;
            this.startMillis = clock.now();
        }

        /**
         * The context to hand to anything this unit of work calls.
         *
         * <p>Passing this on is the entire discipline the pattern asks of you.
         * Forget it once, in one service, and everything below that service
         * falls out of the trace.
         */
        public TraceContext context() {
            return new TraceContext(traceId, spanId);
        }

        @Override
        public void close() {
            if (closed) {
                return;
            }
            closed = true;
            spans.add(new Span(traceId, spanId, parentSpanId, name,
                    startMillis, clock.now() - startMillis));
        }
    }
}
