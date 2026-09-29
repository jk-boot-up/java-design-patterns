package com.jk.explore.stijpa;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo, with Hibernate and an in-memory H2 database. */
class DemoRunsTest {

    @Test
    void acts() {
        String all = String.join("\n", JpaSingleTableDemo.run());
        assertTrue(all.contains("one query that UNIONs 3 tables together"), all);
        assertTrue(all.contains("one plain select from the product table"), all);
        assertTrue(all.contains("KETTLE-1 -> Electronics: 2-year warranty card"), all);
        assertTrue(all.contains("the type column holds: [BOOK, ELECTRONICS, FOOD]"), all);
        assertTrue(all.contains("GIFT-1 -> GiftCard: activate £50 on dispatch"), all);
        assertTrue(all.contains("15 of 20 type-specific cells are empty (NULL)"), all);
        assertTrue(all.contains("make isbn NOT NULL, as every book needs one: refused"), all);
        assertTrue(all.contains("BOOK-2 stored"), all);
    }
}
