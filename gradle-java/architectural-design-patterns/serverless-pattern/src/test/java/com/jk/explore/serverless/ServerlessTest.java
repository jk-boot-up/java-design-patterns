package com.jk.explore.serverless;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class ServerlessTest {

    private Platform platform() {
        return new Platform(5, 10, 15);
    }

    @Test
    void serverIsPaidForIdleTime() {
        assertEquals(200, new AlwaysOnServer(2).bill(100));
    }

    @Test
    void functionsArePaidPerCallOnly() {
        Platform p = platform();
        p.invoke(1);
        p.advance(50);
        p.invoke(1);
        assertEquals(2, p.bill(1));
    }

    @Test
    void concurrentCallsNeedSeparateInstancesAndScaleToZero() {
        Platform p = platform();
        p.invoke(5);
        assertEquals(5, p.instances());
        assertEquals(5, p.coldStarts());
        p.advance(10);
        assertEquals(0, p.instances());
    }

    @Test
    void warmCallsSkipTheColdStart() {
        Platform p = platform();
        p.invoke(1);
        p.advance(2);
        p.invoke(1);
        assertEquals(1, p.coldStarts());
        assertEquals(5, p.latency());
        p.advance(10);
        p.invoke(1);
        assertEquals(10, p.latency());
    }

    @Test
    void instanceMemoryIsLostButTheStoreIsNot() {
        Platform p = platform();
        p.invoke(1);
        p.advance(2);
        p.invoke(1);
        assertEquals(2, p.lastInstanceUses());
        p.advance(10);
        p.invoke(1);
        assertEquals(1, p.lastInstanceUses());
        assertEquals(3, p.sharedCount());
    }

    @Test
    void busyFunctionsCostMoreThanAServerAndLongWorkIsStopped() {
        Platform busy = platform();
        for (int i = 0; i < 300; i++) {
            busy.invoke(1);
        }
        assertTrue(busy.bill(1) > new AlwaysOnServer(2).bill(100));
        assertTrue(platform().runWork(15));
        assertFalse(platform().runWork(20));
    }
}
