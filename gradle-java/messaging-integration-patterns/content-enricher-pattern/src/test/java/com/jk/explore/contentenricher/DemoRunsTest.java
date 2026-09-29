package com.jk.explore.contentenricher;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ContentEnricherDemo.run());

    @Test
    void everyReceiverLooksUpWithoutEnricher() {
        assertTrue(all.contains("3 orders, 2 receivers: 6 calls"));
    }

    @Test
    void enricherWithCacheCallsTwice() {
        assertTrue(all.contains("with a cache: 2 calls"));
    }

    @Test
    void problemListHoldsTheLostOrder() {
        assertTrue(all.contains("[ORD-4: no customer C-99]"));
    }

    @Test
    void copyKeepsOldAddress() {
        assertTrue(all.contains("the message still says: 4 Mill Lane, Leeds"));
    }
}
