package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The data model, and the rules it refuses to bend on.
 *
 * <p>A span with no trace id, no name or a negative duration is not a slightly
 * imperfect span — it is a span that will quietly corrupt every total computed
 * from the trace it lands in. These tests exist to keep that failure at the point
 * of construction, where it names itself, rather than in a percentage three
 * classes away.
 */
class SpanTest {

    @Test
    @DisplayName("a span ends at its start plus its duration")
    void endsWhenTheWorkFinished() {
        Span pricing = new Span("trace-1", "span-3", "span-1", "pricing", 120, 180);

        assertEquals(300, pricing.endMillis());
    }

    @Test
    @DisplayName("only the span at the front door has no parent")
    void rootIsTheSpanWithoutAParent() {
        Span page = new Span("trace-1", "span-1", null, "product-page", 0, 900);
        Span pricing = new Span("trace-1", "span-3", "span-1", "pricing", 120, 180);

        assertTrue(page.isRoot());
        assertFalse(pricing.isRoot());
    }

    @Test
    @DisplayName("a span must belong to a trace, or it can never be added up")
    void rejectsAMissingTraceId() {
        IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class,
                () -> new Span(" ", "span-1", null, "product-page", 0, 900));

        assertTrue(thrown.getMessage().contains("belong to a trace"));
    }

    @Test
    @DisplayName("a span must say what the work was")
    void rejectsAMissingName() {
        assertThrows(IllegalArgumentException.class,
                () -> new Span("trace-1", "span-1", null, "", 0, 900));
    }

    @Test
    @DisplayName("a span must have an id, or nothing can be its child")
    void rejectsAMissingSpanId() {
        assertThrows(IllegalArgumentException.class,
                () -> new Span("trace-1", null, null, "product-page", 0, 900));
    }

    @Test
    @DisplayName("work cannot take negative time")
    void rejectsANegativeDuration() {
        assertThrows(IllegalArgumentException.class,
                () -> new Span("trace-1", "span-1", null, "product-page", 0, -1));
    }

    @Test
    @DisplayName("a zero-length span is legal, because instant work still happened")
    void allowsAZeroDuration() {
        Span cached = new Span("trace-1", "span-2", "span-1", "catalog", 0, 0);

        assertEquals(0, cached.durationMillis());
        assertEquals(0, cached.endMillis());
    }
}
