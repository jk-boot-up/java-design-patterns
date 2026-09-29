package com.jk.explore.entity;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", EntityDemo.run());

    @Test
    void records() {
        assertTrue(all.contains("the old record and the new are equal: false"));
        assertTrue(all.contains("looked up by the new record: null"));
        assertTrue(all.contains("mailing list: 2, both of them Priya"));
        assertTrue(all.contains("as records, equal: true"));
    }

    @Test
    void entities() {
        assertTrue(all.contains("C-17 Priya <priya@new.example>; still C-17"));
        assertTrue(all.contains("her orders: ORD-1, ORD-2"));
        assertTrue(all.contains("as entities, C-42 and C-43, equal: false"));
        assertTrue(all.contains("one customer, 80 points"));
    }

    @Test
    void bill() {
        assertTrue(all.contains("the live customer are equal: true"));
        assertTrue(all.contains("the copy says priya@work.example and the live one priya@final.example"));
    }
}
