package com.jk.explore.shardingpostgres;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against real PostgreSQL databases; skipped, not failed, without a container runtime. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Shards.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", PostgresShardingDemo.run());
        assertTrue(all.contains("one PostgreSQL holds all 2500 orders"), all);
        assertTrue(all.contains("shard-1 (its own database): 834 orders"), all);
        assertTrue(all.contains("customer 17 lives on shard-2, customer 42 on shard-0"), all);
        assertTrue(all.contains("customer 17's orders: [ORD-17]; shards asked: 1"), all);
        assertTrue(all.contains("orders over £500: 1250, from 3 databases"), all);
        assertTrue(all.contains("customer 17 accepted true, customer 42 accepted true"), all);
        assertTrue(all.contains("1874 of 2500 customers must move"), all);
        assertTrue(all.contains("jump hash) instead: 630 must move"), all);
    }

    @Test
    void jumpHashMovesFewKeys() {
        int moved = 0;
        for (int c = 1; c <= 10_000; c++) {
            if (PostgresShardingDemo.jump(c, 9) != PostgresShardingDemo.jump(c, 10)) {
                moved++;
            }
        }
        assertTrue(moved < 1_500, "moved " + moved);
    }
}
