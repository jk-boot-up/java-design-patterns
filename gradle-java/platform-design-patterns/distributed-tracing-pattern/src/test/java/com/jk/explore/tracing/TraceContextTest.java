package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * The two values that have to survive the journey.
 */
class TraceContextTest {

    @Test
    @DisplayName("a child keeps the trace and takes a new parent")
    void childKeepsTheTraceAndChangesTheSpan() {
        TraceContext page = new TraceContext("trace-4f2a", "span-1");

        TraceContext pricing = page.childWith("span-3");

        assertEquals("trace-4f2a", pricing.traceId());
        assertEquals("span-3", pricing.spanId());
    }

    @Test
    @DisplayName("the parent is unchanged by making a child of it")
    void makingAChildDoesNotMutateTheParent() {
        TraceContext page = new TraceContext("trace-4f2a", "span-1");

        page.childWith("span-3");

        assertEquals("span-1", page.spanId());
    }

    @Test
    @DisplayName("a context without a trace id is not a context")
    void rejectsAMissingTraceId() {
        assertThrows(IllegalArgumentException.class, () -> new TraceContext(null, "span-1"));
    }

    @Test
    @DisplayName("a context without a span id cannot be anybody's parent")
    void rejectsAMissingSpanId() {
        assertThrows(IllegalArgumentException.class, () -> new TraceContext("trace-1", "  "));
    }
}
