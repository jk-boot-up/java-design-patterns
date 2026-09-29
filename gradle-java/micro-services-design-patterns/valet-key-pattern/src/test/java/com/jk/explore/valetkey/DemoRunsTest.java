package com.jk.explore.valetkey;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", ValetKeyDemo.run());
    }

    @Test
    void throughApp() {
        assertTrue(all.contains("the app server carried 40.0 MB"));
    }

    @Test
    void valetKey() {
        assertTrue(all.contains("201 stored /reviews/R-11/photo.jpg (2000000 bytes)"));
        assertTrue(all.contains("under 200 bytes: just the key"));
        assertTrue(all.contains("403 key does not allow GET"));
        assertTrue(all.contains("413 file too large"));
        assertTrue(all.contains("401 no key"));
        assertTrue(all.contains("403 key expired"));
        assertTrue(all.contains("a stranger uses it: 201"));
    }
}
