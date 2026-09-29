package com.jk.explore.queryobject;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", QueryObjectDemo.run());

    @Test
    void strings() {
        assertTrue(all.contains("WHERE  AND price_pence <= 3000"));
        assertTrue(all.contains("name LIKE '%O'Brien%'"));
    }

    @Test
    void queryObject() {
        assertTrue(all.contains("SQL:    SELECT * FROM product WHERE category = ? AND price_pence <= ? AND stock > 0"));
        assertTrue(all.contains("values: [kitchen, 3000]"));
        assertTrue(all.contains("any category under £30: SELECT * FROM product WHERE price_pence <= ?"));
    }

    @Test
    void inMemory() {
        assertTrue(all.contains("found steel kettle, £30.00"));
        assertTrue(all.contains("found tea towel, £6.00"));
        assertTrue(all.contains("found O'Brien's mug, £9.00"));
    }

    @Test
    void safe() {
        assertTrue(all.contains("values: [kitchen, 3000, %O'Brien%]"));
        assertTrue(all.contains("found 1 product"));
        assertTrue(all.contains("still 2 values"));
    }
}
