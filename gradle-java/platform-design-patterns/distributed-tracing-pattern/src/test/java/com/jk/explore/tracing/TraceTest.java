package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The arithmetic that turns a pile of spans into an answer.
 *
 * <p>The test that matters most here is the self-time one. Total time always
 * names the root span, which is always the request itself and is therefore always
 * useless. Subtracting the time a span spent waiting on its children is the step
 * that turns "the page took nine hundred milliseconds" into "the ranking model
 * took three hundred and forty of them", and it is the whole reason a trace beats
 * a stopwatch.
 */
class TraceTest {

    private static final Trace PAGE = ProductPage.load("trace-4f2a");

    @Test
    @DisplayName("the root is the span at the front door")
    void findsTheRoot() {
        assertEquals("product-page", PAGE.root().orElseThrow().name());
    }

    @Test
    @DisplayName("a healthy trace has exactly one root")
    void healthyTraceHasOneRoot() {
        assertEquals(1, PAGE.roots().size());
    }

    @Test
    @DisplayName("children come back in the order the work happened")
    void childrenAreOrderedByStart() {
        String pageSpan = PAGE.root().orElseThrow().spanId();

        assertEquals(List.of("catalog", "pricing", "inventory", "recommendations", "render"),
                PAGE.childrenOf(pageSpan).stream().map(Span::name).toList());
    }

    @Test
    @DisplayName("the ranking model hangs off recommendations, not off the page")
    void nestingIsPreserved() {
        Span recommendations = PAGE.spans().stream()
                .filter(span -> "recommendations".equals(span.name()))
                .findFirst().orElseThrow();

        assertEquals(List.of("ranking-model"),
                PAGE.childrenOf(recommendations.spanId()).stream().map(Span::name).toList());
    }

    @Test
    @DisplayName("a healthy trace has no orphans")
    void healthyTraceHasNoOrphans() {
        assertEquals(List.of(), PAGE.orphans());
    }

    @Test
    @DisplayName("a span whose parent is not in the trace is an orphan")
    void spotsAnOrphan() {
        Trace broken = new Trace("trace-1", List.of(
                new Span("trace-1", "span-1", null, "product-page", 0, 900),
                new Span("trace-1", "span-9", "span-nobody-has", "pricing", 120, 180)));

        assertEquals(List.of("pricing"),
                broken.orphans().stream().map(Span::name).toList());
    }

    @Test
    @DisplayName("self time excludes what a span was waiting on")
    void selfTimeExcludesChildren() {
        Span page = PAGE.root().orElseThrow();

        // The page span lasted the whole request but did none of the work
        // itself, which is exactly why total time never names a culprit.
        assertEquals(900, page.durationMillis());
        assertEquals(0, PAGE.selfTime(page));
    }

    @Test
    @DisplayName("recommendations is charged only for the part the model did not do")
    void selfTimeSplitsAParentFromItsChild() {
        Span recommendations = PAGE.spans().stream()
                .filter(span -> "recommendations".equals(span.name()))
                .findFirst().orElseThrow();

        assertEquals(400, recommendations.durationMillis());
        assertEquals(60, PAGE.selfTime(recommendations));
    }

    @Test
    @DisplayName("the ranking model is named as the slowest single piece of work")
    void rankingIsLargestFirst() {
        Map<String, Long> byName = PAGE.selfTimeByName();

        assertEquals("ranking-model", byName.keySet().iterator().next());
        assertEquals(340L, byName.get("ranking-model"));
    }

    @Test
    @DisplayName("every millisecond of the request is accounted for by exactly one span")
    void selfTimesSumToTheWholeRequest() {
        long accounted = PAGE.selfTimeByName().values().stream().mapToLong(Long::longValue).sum();

        assertEquals(ProductPage.PAGE_MS, accounted);
        assertEquals(900, accounted);
    }

    @Test
    @DisplayName("total time is the root's duration")
    void totalIsTheRootDuration() {
        assertEquals(900, PAGE.totalMillis());
    }

    @Test
    @DisplayName("elapsed time is the moment the last span closed")
    void endMillisIsTheLastFinish() {
        assertEquals(900, PAGE.endMillis());
    }

    @Test
    @DisplayName("a broken trace reports both of its roots, the real one first")
    void brokenTraceReportsRootsOldestFirst() {
        Trace broken = AsyncHandoff.withThreadLocalContext();

        assertEquals(List.of("product-page", "recommendations"),
                broken.roots().stream().map(Span::name).toList());
    }

    @Test
    @DisplayName("an empty trace has no root and no time, rather than throwing")
    void emptyTraceIsAnswerable() {
        Trace empty = new Trace("trace-1", List.of());

        assertTrue(empty.root().isEmpty());
        assertEquals(0, empty.totalMillis());
        assertEquals(0, empty.endMillis());
    }

    @Test
    @DisplayName("the span list cannot be changed after the trace is made")
    void spansAreCopied() {
        List<Span> mutable = new java.util.ArrayList<>(PAGE.spans());
        Trace trace = new Trace("trace-1", mutable);
        mutable.clear();

        assertEquals(7, trace.spans().size());
        assertThrows(UnsupportedOperationException.class, () -> trace.spans().clear());
    }
}
