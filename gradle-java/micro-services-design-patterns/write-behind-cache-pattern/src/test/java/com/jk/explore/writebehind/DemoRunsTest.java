package com.jk.explore.writebehind;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", WriteBehindDemo.run());

    @Test
    void writeThroughCosts() {
        assertTrue(all.contains("10 cart changes each: 30 database writes"));
        assertTrue(all.contains("waited 600 ms in total"));
    }

    @Test
    void writeBehindCoalesces() {
        assertTrue(all.contains("customers waited 0 ms; 3 carts waiting"));
        assertTrue(all.contains("flush after 5 seconds: 3 database writes"));
        assertTrue(all.contains("{mug=10, tea=9}"));
    }

    @Test
    void survivesDatabaseOutage() {
        assertTrue(all.contains("flush: failed, database unavailable; 2 carts still waiting"));
        assertTrue(all.contains("next flush: 2 writes"));
    }

    @Test
    void crashLoses() {
        assertTrue(all.contains("crash: 3 changes lost; priya's teapot is not in the database: true"));
    }

    @Test
    void databaseIsBehind() {
        assertTrue(all.contains("checkout sees 3 kettles; the stock report reading the database sees 1"));
    }
}
