package com.jk.explore.proactor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class ProactorQuotesTest {

    @Test
    void collectsEveryAnswer() throws Exception {
        try (Supplier a = new Supplier(100); Supplier b = new Supplier(200)) {
            ProactorQuotes q = new ProactorQuotes(2);
            q.start(List.of(a.port(), b.port()));
            assertTrue(q.await(5000));
            assertEquals("100", q.results().get(a.port()));
            assertEquals("200", q.results().get(b.port()));
        }
    }

    @Test
    void waitsOverlap() throws Exception {
        try (Supplier a = new Supplier(1); Supplier b = new Supplier(2); Supplier c = new Supplier(3)) {
            ProactorQuotes q = new ProactorQuotes(3);
            long t0 = System.nanoTime();
            q.start(List.of(a.port(), b.port(), c.port()));
            q.await(5000);
            assertTrue((System.nanoTime() - t0) / 1_000_000 < 3 * Supplier.MS_TO_ANSWER);
        }
    }

    @Test
    void downSupplierCallsFailed() throws Exception {
        int dead = Supplier.deadPort();
        ProactorQuotes q = new ProactorQuotes(1);
        q.start(List.of(dead));
        assertTrue(q.await(5000));
        assertTrue(q.results().get(dead).startsWith("failed"));
    }

    @Test
    void blockingGetsTheSamePrices() throws Exception {
        try (Supplier a = new Supplier(100)) {
            assertEquals(100, BlockingQuotes.ask(List.of(a.port())).get(a.port()));
        }
    }
}
