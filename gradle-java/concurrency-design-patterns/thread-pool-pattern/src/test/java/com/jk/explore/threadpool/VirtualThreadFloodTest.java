package com.jk.explore.threadpool;

import com.jk.explore.threadpool.harness.Gate;
import com.jk.explore.threadpool.pattern.VirtualThreadFlood;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class VirtualThreadFloodTest {

    @Test
    void floodSafelyCreatesExactlyTheRequestedVirtualThreads() {
        Gate hold = new Gate();
        VirtualThreadFlood.FloodResult result = VirtualThreadFlood.floodSafely(200, hold);

        assertEquals(200, result.threadsCreated());
        assertTrue(result.totalCreateNanos() > 0);
        assertTrue(hold.isOpen(), "floodSafely must release the gate itself before returning");
    }
}
