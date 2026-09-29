package com.jk.explore.halfsync;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class HalfSyncHalfAsyncTest {

    @Test
    void everyOrderIsProcessed() throws Exception {
        HalfSyncHalfAsync h = new HalfSyncHalfAsync(3, 50);
        h.startWorkers();
        h.burst(9);
        h.awaitDone(9, 5000);
        h.stop();
        assertEquals(9, h.done());
    }

    @Test
    void acceptingIsFastEvenWhenWorkIsSlow() throws Exception {
        HalfSyncHalfAsync h = new HalfSyncHalfAsync(1, 50);
        h.startWorkers();
        h.burst(10);
        assertTrue(h.worstAcceptMs() < 100);
        h.stop();
    }

    @Test
    void fullQueueTurnsOrdersAway() throws Exception {
        HalfSyncHalfAsync h = new HalfSyncHalfAsync(1, 5);
        h.burst(8);
        assertEquals(3, h.turnedAway());
    }

    @Test
    void eventThreadOnlyMakesLaterOrdersWait() throws Exception {
        EventThreadOnly e = new EventThreadOnly();
        e.burst(5);
        assertTrue(e.worstAcceptMs() >= 350);
        assertEquals(5, e.done());
    }
}
