package com.jk.explore.threadpool;

import com.jk.explore.threadpool.domain.Order;
import com.jk.explore.threadpool.harness.Gate;
import com.jk.explore.threadpool.naive.ThreadPerOrderPacking;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ThreadPerOrderPackingTest {

    @Test
    void everySubmittedOrderGetsItsOwnLiveThread() throws InterruptedException {
        Gate packingHold = new Gate();
        ThreadPerOrderPacking packing = new ThreadPerOrderPacking(order -> packingHold.awaitOpen());

        // submit() increments liveThreads on the calling thread before it ever
        // starts the new one, so the count below is exact, not a race.
        packing.submit(new Order("ord-1", "BNS-220"));
        packing.submit(new Order("ord-2", "BNS-220"));
        packing.submit(new Order("ord-3", "BNS-220"));
        assertEquals(3, packing.liveThreads());

        // Opening the gate lets all three finish packing and decrement; this
        // spin-wait cannot hang, because nothing after the gate opens blocks
        // again -- it only waits out the last few instructions of each thread.
        packingHold.open();
        while (packing.liveThreads() > 0) {
            Thread.onSpinWait();
        }
        assertEquals(0, packing.liveThreads());
    }

    @Test
    void floodSafelyCreatesExactlyTheRequestedThreads() {
        Gate hold = new Gate();
        ThreadPerOrderPacking.FloodResult result = ThreadPerOrderPacking.floodSafely(50, hold);

        assertEquals(50, result.threadsCreated());
        assertTrue(result.totalCreateNanos() > 0);
        assertTrue(hold.isOpen(), "floodSafely must release the gate itself before returning");
    }
}
