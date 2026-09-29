package com.jk.explore.sharding;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ShardingDemo.run());

    @Test
    void oneDatabase() {
        assertTrue(all.contains("orders left waiting every minute: 1500"));
    }

    @Test
    void shards() {
        assertTrue(all.contains("shard-1: 834 orders this minute (within its limit)"));
        assertTrue(all.contains("customer 17 lives on shard-2"));
        assertTrue(all.contains("shards asked: 1"));
        assertTrue(all.contains("25 found, shards asked: 3"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("1874 of 2500 customers"));
    }
}
