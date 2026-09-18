package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The instrumented page load, and the same page load with one service missing.
 *
 * <p>The second half of this class is the important half, because it pins down a
 * failure that does not look like a failure. When recommendations forgets to open
 * a span, the trace does not come back with a hole in it. It comes back complete,
 * plausible, and wrong: the four hundred milliseconds lands on the parent, so the
 * page appears to be doing work it never did, and the ranking model appears to
 * hang directly off the page. Nothing errors and nothing warns. The tests below
 * are how that stays visible.
 */
class ProductPageTest {

    @Test
    @DisplayName("a page load records one span per unit of work")
    void recordsSevenSpans() {
        Trace trace = ProductPage.load("trace-4f2a");

        assertEquals(7, trace.spans().size());
    }

    @Test
    @DisplayName("the page is the sum of the services it waited on")
    void pageDurationIsTheSumOfItsParts() {
        assertEquals(900, ProductPage.PAGE_MS);
        assertEquals(ProductPage.PAGE_MS, ProductPage.load("trace-4f2a").totalMillis());
    }

    @Test
    @DisplayName("each service starts when the one before it finished")
    void servicesRunOneAfterAnother() {
        Trace trace = ProductPage.load("trace-4f2a");
        List<Span> children = trace.childrenOf(trace.root().orElseThrow().spanId());

        long expectedStart = 0;
        for (Span child : children) {
            assertEquals(expectedStart, child.startMillis(),
                    child.name() + " should start where the previous service finished");
            expectedStart = child.endMillis();
        }
    }

    @Test
    @DisplayName("the same trace id reaches every span")
    void oneTraceIdThroughout() {
        Trace trace = ProductPage.load("trace-4f2a");

        assertTrue(trace.spans().stream()
                .allMatch(span -> "trace-4f2a".equals(span.traceId())));
    }

    @Test
    @DisplayName("the run is identical every time, so the documents can quote it")
    void isDeterministic() {
        assertEquals(ProductPage.load("trace-4f2a").spans(),
                ProductPage.load("trace-4f2a").spans());
    }

    @Test
    @DisplayName("without instrumentation the page loses one span, not the time")
    void uninstrumentedServiceLosesOnlyItsOwnSpan() {
        Trace partial = ProductPage.loadWithUninstrumentedRecommendations("trace-7c19");

        assertEquals(6, partial.spans().size());
        assertFalse(partial.spans().stream().anyMatch(s -> "recommendations".equals(s.name())));
        assertEquals(900, partial.totalMillis());
    }

    @Test
    @DisplayName("the missing service's time is charged to its parent instead")
    void theTimeLandsOnTheParent() {
        Trace partial = ProductPage.loadWithUninstrumentedRecommendations("trace-7c19");

        // Sixty milliseconds of work the page never did. This is the wrong
        // answer that partial instrumentation produces, and the reason somebody
        // spends an afternoon reading the page renderer.
        assertEquals(60, partial.selfTime(partial.root().orElseThrow()));
        assertEquals(0, ProductPage.load("trace-4f2a")
                .selfTime(ProductPage.load("trace-4f2a").root().orElseThrow()));
    }

    @Test
    @DisplayName("the ranking model appears to hang off the page it never called")
    void nestingIsFlattenedByTheMissingSpan() {
        Trace partial = ProductPage.loadWithUninstrumentedRecommendations("trace-7c19");
        String pageSpan = partial.root().orElseThrow().spanId();

        assertEquals(List.of("catalog", "pricing", "inventory", "ranking-model", "render"),
                partial.childrenOf(pageSpan).stream().map(Span::name).toList());
    }

    @Test
    @DisplayName("a partial trace has no orphans, which is why nobody notices")
    void thePartialTraceLooksHealthy() {
        Trace partial = ProductPage.loadWithUninstrumentedRecommendations("trace-7c19");

        assertEquals(List.of(), partial.orphans());
        assertEquals(1, partial.roots().size());
    }
}
