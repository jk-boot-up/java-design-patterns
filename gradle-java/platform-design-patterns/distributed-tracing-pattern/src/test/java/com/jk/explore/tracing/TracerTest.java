package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The three habits the pattern asks of you, checked one at a time.
 *
 * <p>Open a span, pass the context to whatever you call, close the span. These
 * tests pin down what each of those actually does, including the one that catches
 * people out: a span is recorded at the moment it is <em>closed</em>, so a span
 * that is never closed never appears in the trace at all.
 */
class TracerTest {

    @Test
    @DisplayName("the root span has no parent")
    void rootHasNoParent() {
        Tracer tracer = new Tracer("trace-1", new Clock.Scripted());

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            assertEquals("span-1", page.context().spanId());
        }

        Span root = tracer.trace().spans().get(0);
        assertNull(root.parentSpanId());
        assertTrue(root.isRoot());
    }

    @Test
    @DisplayName("a child span records the caller as its parent")
    void childRecordsItsCaller() {
        Tracer tracer = new Tracer("trace-1", new Clock.Scripted());

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            try (Tracer.Scope pricing = tracer.start(page.context(), "pricing")) {
                // nothing to do; the shape is the point
            }
        }

        List<Span> spans = tracer.trace().spans();
        assertEquals("pricing", spans.get(0).name());
        assertEquals("span-1", spans.get(0).parentSpanId());
    }

    @Test
    @DisplayName("closing the span is what records the duration")
    void durationIsTakenAtClose() {
        Clock.Scripted clock = new Clock.Scripted();
        Tracer tracer = new Tracer("trace-1", clock);

        try (Tracer.Scope pricing = tracer.startRoot("pricing")) {
            clock.advance(180);
        }

        assertEquals(180, tracer.trace().spans().get(0).durationMillis());
    }

    @Test
    @DisplayName("a span that is never closed never appears")
    void anUnclosedSpanIsInvisible() {
        Clock.Scripted clock = new Clock.Scripted();
        Tracer tracer = new Tracer("trace-1", clock);

        Tracer.Scope leaked = tracer.startRoot("pricing");
        clock.advance(180);

        // This is not a quirk of this class. It is why real instrumentation uses
        // try-with-resources: an exception thrown past an un-closed span deletes
        // the record of the very call that failed.
        assertEquals(List.of(), tracer.trace().spans());

        leaked.close();
        assertEquals(1, tracer.trace().spans().size());
    }

    @Test
    @DisplayName("closing twice does not record the span twice")
    void closeIsIdempotent() {
        Tracer tracer = new Tracer("trace-1", new Clock.Scripted());

        Tracer.Scope page = tracer.startRoot("product-page");
        page.close();
        page.close();

        assertEquals(1, tracer.trace().spans().size());
    }

    @Test
    @DisplayName("every span from one tracer carries the same trace id")
    void allSpansShareTheTraceId() {
        Tracer tracer = new Tracer("trace-4f2a", new Clock.Scripted());

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            try (Tracer.Scope catalog = tracer.start(page.context(), "catalog")) {
                // nothing to do
            }
        }

        assertTrue(tracer.trace().spans().stream()
                .allMatch(span -> "trace-4f2a".equals(span.traceId())));
    }

    @Test
    @DisplayName("spans arrive in the order they were closed, innermost first")
    void spansArriveInCloseOrder() {
        Tracer tracer = new Tracer("trace-1", new Clock.Scripted());

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            try (Tracer.Scope recs = tracer.start(page.context(), "recommendations")) {
                try (Tracer.Scope model = tracer.start(recs.context(), "ranking-model")) {
                    // nothing to do
                }
            }
        }

        assertEquals(List.of("ranking-model", "recommendations", "product-page"),
                tracer.trace().spans().stream().map(Span::name).toList());
    }
}
