package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

/**
 * The failure that catches everybody: a thread-local that does not travel.
 *
 * <p>Both methods under test do the same work on another thread, and only one of
 * them keeps the trace. The difference is a single line — whether the context is
 * read on the thread that has it, or hoped for on the thread that does not. These
 * tests are the mechanical proof that the difference is real, because reading the
 * two methods side by side it is almost invisible.
 */
class AsyncHandoffTest {

    @Test
    @DisplayName("a thread-local context does not reach the worker thread")
    void threadLocalContextIsLost() {
        Trace broken = AsyncHandoff.withThreadLocalContext();

        assertEquals(List.of("product-page", "recommendations"),
                broken.roots().stream().map(Span::name).toList());
        assertNull(broken.spans().stream()
                .filter(span -> "recommendations".equals(span.name()))
                .findFirst().orElseThrow()
                .parentSpanId());
    }

    @Test
    @DisplayName("the broken trace has two roots, which is what broken looks like")
    void brokenTraceHasTwoRoots() {
        assertEquals(2, AsyncHandoff.withThreadLocalContext().roots().size());
    }

    @Test
    @DisplayName("passing the context as a value keeps the trace whole")
    void explicitContextSurvivesTheHandoff() {
        Trace fixed = AsyncHandoff.withExplicitContext();

        assertEquals(1, fixed.roots().size());
        assertEquals("product-page", fixed.root().orElseThrow().name());
        assertNotNull(fixed.spans().stream()
                .filter(span -> "recommendations".equals(span.name()))
                .findFirst().orElseThrow()
                .parentSpanId());
    }

    @Test
    @DisplayName("the strip hangs off the page once the context is passed by hand")
    void fixedTraceNestsCorrectly() {
        Trace fixed = AsyncHandoff.withExplicitContext();

        assertEquals(List.of("recommendations"),
                fixed.childrenOf(fixed.root().orElseThrow().spanId()).stream()
                        .map(Span::name).toList());
    }

    @Test
    @DisplayName("both versions record the same work and the same time")
    void onlyTheShapeDiffers() {
        Trace broken = AsyncHandoff.withThreadLocalContext();
        Trace fixed = AsyncHandoff.withExplicitContext();

        // This is the uncomfortable part. Same two spans, same four hundred
        // milliseconds, same absence of any error. The only thing the broken run
        // lost is the link, and the link is the only thing that was useful.
        assertEquals(2, broken.spans().size());
        assertEquals(2, fixed.spans().size());
        assertEquals(ProductPage.RECOMMENDATIONS_MS, broken.endMillis());
        assertEquals(ProductPage.RECOMMENDATIONS_MS, fixed.endMillis());
    }

    @Test
    @DisplayName("the lost context leaves the page looking like it did no work")
    void theBrokenPageCannotAccountForItsTime() {
        Trace broken = AsyncHandoff.withThreadLocalContext();
        Span page = broken.roots().get(0);

        assertEquals(ProductPage.RECOMMENDATIONS_MS, page.durationMillis());
        assertEquals(ProductPage.RECOMMENDATIONS_MS, broken.selfTime(page));
    }
}
