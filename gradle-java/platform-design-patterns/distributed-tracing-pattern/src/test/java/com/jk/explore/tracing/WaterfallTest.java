package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The drawing, which is the payoff.
 *
 * <p>These tests check the properties that make the picture trustworthy rather
 * than the exact characters, because the exact characters will change if the bar
 * width is ever adjusted. What must not change is that a child is indented under
 * its parent, that a bar starts where the work started, that a span too short to
 * draw is still drawn, and that a broken trace looks broken.
 */
class WaterfallTest {

    private static final String DRAWN = Waterfall.render(ProductPage.load("trace-4f2a"));

    @Test
    @DisplayName("the header names the trace and how long it took")
    void headerCarriesTheTraceId() {
        assertTrue(DRAWN.lines().findFirst().orElseThrow().contains("trace-4f2a"));
        assertTrue(DRAWN.lines().findFirst().orElseThrow().contains("900ms"));
    }

    @Test
    @DisplayName("one line per span, plus the header")
    void everySpanIsDrawn() {
        assertEquals(8, DRAWN.lines().count());
    }

    @Test
    @DisplayName("children are indented under whatever called them")
    void nestingShowsAsIndentation() {
        List<String> lines = DRAWN.lines().toList();

        assertTrue(lines.get(1).startsWith("  product-page"));
        assertTrue(lines.get(2).startsWith("    catalog"));
        assertTrue(lines.get(6).startsWith("      ranking-model"),
                "the ranking model sits inside recommendations, two levels deep");
    }

    @Test
    @DisplayName("spans are drawn in the order the work happened")
    void readsLeftToRightInTimeOrder() {
        List<String> names = DRAWN.lines().skip(1)
                .map(line -> line.trim().split("\\s+")[0])
                .toList();

        assertEquals(List.of("product-page", "catalog", "pricing", "inventory",
                "recommendations", "ranking-model", "render"), names);
    }

    @Test
    @DisplayName("a bar starts further right the later the work began")
    void barOffsetGrowsWithStartTime() {
        List<String> lines = DRAWN.lines().toList();

        assertTrue(barStart(lines.get(2)) < barStart(lines.get(3)),
                "pricing starts after catalog, so its bar starts further right");
        assertTrue(barStart(lines.get(3)) < barStart(lines.get(4)),
                "inventory starts after pricing");
        assertTrue(barStart(lines.get(7)) > barStart(lines.get(5)),
                "render is the last thing to happen");
    }

    @Test
    @DisplayName("the root's bar fills the whole width")
    void theRootSpansTheTimeline() {
        String root = DRAWN.lines().skip(1).findFirst().orElseThrow();

        assertEquals(44, root.chars().filter(c -> c == '=').count());
    }

    @Test
    @DisplayName("a span that did work of its own says how much")
    void selfTimeIsCalledOut() {
        assertTrue(DRAWN.contains("60ms of it its own"),
                "recommendations did sixty milliseconds the model did not");
    }

    @Test
    @DisplayName("a span too short to draw is still drawn")
    void tinySpansDoNotVanish() {
        Trace trace = new Trace("trace-1", List.of(
                new Span("trace-1", "span-1", null, "product-page", 0, 900),
                new Span("trace-1", "span-2", "span-1", "cache-hit", 400, 1)));

        // One millisecond in nine hundred rounds to zero characters of bar. A
        // span drawn as nothing would look like a span that never happened,
        // which is the one thing this drawing must never suggest.
        String drawn = Waterfall.render(trace);
        String cacheLine = drawn.lines().filter(l -> l.contains("cache-hit"))
                .findFirst().orElseThrow();

        assertEquals(1, cacheLine.chars().filter(c -> c == '=').count());
    }

    @Test
    @DisplayName("a broken trace draws every root and says so")
    void brokenTraceIsDrawnHonestly() {
        String drawn = Waterfall.render(AsyncHandoff.withThreadLocalContext());

        assertTrue(drawn.contains("2 separate roots — this trace is broken"));
        assertTrue(drawn.contains("product-page"));
        assertTrue(drawn.contains("recommendations"),
                "the orphaned work must still appear, or the drawing hides the failure");
    }

    @Test
    @DisplayName("a healthy trace says nothing about roots")
    void healthyTraceIsNotAccused() {
        assertTrue(!DRAWN.contains("separate roots"));
    }

    @Test
    @DisplayName("orphans are listed under their own heading")
    void orphansAreCalledOut() {
        Trace broken = new Trace("trace-1", List.of(
                new Span("trace-1", "span-1", null, "product-page", 0, 900),
                new Span("trace-1", "span-9", "span-nobody-has", "pricing", 120, 180)));

        String drawn = Waterfall.render(broken);

        assertTrue(drawn.contains("1 span whose parent is missing"));
    }

    @Test
    @DisplayName("a trace with no root explains itself rather than drawing nothing")
    void rootlessTraceExplainsItself() {
        Trace rootless = new Trace("trace-1", List.of(
                new Span("trace-1", "span-9", "span-nobody-has", "pricing", 120, 180)));

        assertTrue(Waterfall.render(rootless).contains("no root span"));
    }

    /** Where the bar's first {@code =} sits, as a column. */
    private static int barStart(String line) {
        return line.indexOf('=');
    }
}
