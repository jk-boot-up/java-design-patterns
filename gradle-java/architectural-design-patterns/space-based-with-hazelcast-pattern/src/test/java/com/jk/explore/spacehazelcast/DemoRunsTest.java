package com.jk.explore.spacehazelcast;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo, with three real Hazelcast members started inside the test. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        String all = String.join("\n", HazelcastSpaceBasedDemo.run());
        assertTrue(all.contains("each written to the database: over 1.4 s"), all);
        assertTrue(all.contains("cluster formed: 3 members"), all);
        assertTrue(all.contains("under 1 s; database writes during the orders: 0"), all);
        assertTrue(all.contains("stock read on each unit: [700, 700, 700]"), all);
        assertTrue(all.contains("database stock now 700, after at most 3 writes"), all);
        assertTrue(all.contains("sold 1 of 2; stock 0"), all);
        assertTrue(all.contains("KETTLE-1 on the survivors still 700"), all);
    }
}
