package com.jk.explore.backpressure;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class BackpressureTest {

    @Test
    void unboundedBufferGrows() {
        FeedSimulation.Result r = FeedSimulation.run(10_000, 0, 5);
        assertEquals(4500, r.finalWaiting());
    }

    @Test
    void boundedBufferNeverExceedsCapacity() {
        FeedSimulation.Result r = FeedSimulation.run(10_000, 300, 1000);
        assertTrue(r.maxWaiting() <= 300);
        assertEquals(10_000, r.indexed());
    }

    @Test
    void subscriberGetsOnlyWhatItAsksFor() {
        PullPublisher feed = new PullPublisher(95);
        Indexer indexer = new Indexer(7);
        feed.subscribe(indexer);
        assertEquals(95, indexer.indexed());
        assertTrue(indexer.done());
        assertTrue(feed.maxOutstanding() <= 7);
    }

    @Test
    void conflatorKeepsLatest() {
        Conflator c = new Conflator();
        c.offer("A", 5);
        c.offer("A", 3);
        c.offer("B", 9);
        assertEquals(2, c.drain().size());
        assertEquals(3, c.received());
    }
}
