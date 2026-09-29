package com.jk.explore.modularmonolith;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ModularMonolithDemo.run());

    @Test
    void mudOversells() {
        assertTrue(all.contains("kettle stock is now -1"));
    }

    @Test
    void modulesRefuse() {
        assertTrue(all.contains("ORD-1 placed, pay-1"));
        assertTrue(all.contains("ORD-2 refused: only 0 kettle left"));
    }

    @Test
    void boundaryCheck() {
        assertTrue(all.contains("scan of this project's source: 0 modules"));
        assertTrue(all.contains("[OrdersModule.java imports payments.internal]"));
    }

    @Test
    void movedOut() {
        assertTrue(all.contains("ORD-3 placed, pay-1"));
        assertTrue(all.contains("over the network: 1 call"));
    }
}
