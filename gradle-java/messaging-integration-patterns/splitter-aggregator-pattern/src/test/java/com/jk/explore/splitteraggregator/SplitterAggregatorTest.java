package com.jk.explore.splitteraggregator;

import org.junit.jupiter.api.Test;

import java.util.List;

import static com.jk.explore.splitteraggregator.SplitterAggregatorDemo.LINES;
import static org.junit.jupiter.api.Assertions.*;

class SplitterAggregatorTest {

    private final Clock clock = new Clock();
    private final Aggregator agg = new Aggregator(clock, 30);

    @Test
    void theSplitterNumbersEveryPartAndCarriesTheOrderId() {
        List<Part> parts = Splitter.split("ORD-1", LINES);
        assertEquals(3, parts.size());
        for (int i = 0; i < 3; i++) {
            assertEquals(i + 1, parts.get(i).index());
            assertEquals(3, parts.get(i).total());
            assertEquals("ORD-1", parts.get(i).orderId());
            assertEquals(LINES.get(i), parts.get(i).content());
        }
    }

    @Test
    void partsArrivingInAnyOrderComeBackInLineOrder() {
        List<Part> parts = Splitter.split("A", LINES);
        assertTrue(agg.accept(parts.get(2)).isEmpty());
        assertTrue(agg.accept(parts.get(0)).isEmpty());
        var done = agg.accept(parts.get(1)).orElseThrow();
        assertEquals(LINES, done.contents());
        assertTrue(done.complete());
        assertEquals(0, agg.openOrders());
    }

    @Test
    void twoOrdersInterleavedDoNotMix() {
        List<Part> a = Splitter.split("A", List.of("a1", "a2"));
        List<Part> b = Splitter.split("B", List.of("b1", "b2"));
        agg.accept(a.get(0));
        agg.accept(b.get(0));
        assertEquals(List.of("b1", "b2"), agg.accept(b.get(1)).orElseThrow().contents());
        assertEquals(List.of("a1", "a2"), agg.accept(a.get(1)).orElseThrow().contents());
    }

    @Test
    void aDuplicatePartIsCountedOnce() {
        List<Part> p = Splitter.split("A", List.of("x", "y"));
        agg.accept(p.get(0));
        agg.accept(p.get(0));
        assertEquals(1, agg.duplicates());
        assertEquals(List.of("x", "y"), agg.accept(p.get(1)).orElseThrow().contents());
    }

    @Test
    void anIncompleteOrderIsEmittedPartialAtTheTimeoutAndNotBefore() {
        List<Part> p = Splitter.split("A", LINES);
        agg.accept(p.get(0));
        agg.accept(p.get(2));
        clock.advance(29);
        assertTrue(agg.expire().isEmpty());
        clock.advance(1);
        var partial = agg.expire().get(0);
        assertEquals(List.of(2), partial.missing());
        assertFalse(partial.complete());
        assertEquals(2, partial.contents().size());
        assertEquals(0, agg.openOrders());
    }

    @Test
    void everyOrderMissingAPartIsHeldUntilItExpires() {
        for (int i = 0; i < 100; i++) {
            List<Part> p = Splitter.split("O" + i, LINES);
            agg.accept(p.get(0));
        }
        assertEquals(100, agg.openOrders());
        clock.advance(30);
        assertEquals(100, agg.expire().size());
        assertEquals(0, agg.openOrders());
    }

    @Test
    void aSingleLineOrderCompletesAtOnce() {
        assertTrue(agg.accept(Splitter.split("A", List.of("only")).get(0)).orElseThrow().complete());
    }
}
