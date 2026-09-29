package com.jk.explore.writethrough;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", WriteThroughDemo.run());

    @Test
    void stale() {
        assertTrue(all.contains("product page (cache): £30.00; checkout (database): £27.00"));
    }

    @Test
    void writeThrough() {
        assertTrue(all.contains("product page: £27.00; checkout: £27.00"));
        assertTrue(all.contains("100 page views: 0 database reads"));
        assertTrue(all.contains("still say £27.00"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("1000 prices: 20.0 s spent waiting"));
    }
}
