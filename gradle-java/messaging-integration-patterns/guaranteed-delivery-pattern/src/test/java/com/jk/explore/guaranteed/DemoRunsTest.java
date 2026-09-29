package com.jk.explore.guaranteed;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all;

    DemoRunsTest() throws Exception {
        all = String.join("\n", GuaranteedDeliveryDemo.run());
    }

    @Test
    void memoryLoses() {
        assertTrue(all.contains("queued emails now 0"));
    }

    @Test
    void journalKeeps() {
        assertTrue(all.contains("the journal file has 10 lines"));
        assertTrue(all.contains("reads the file: 10 emails waiting"));
        assertTrue(all.contains("still waiting: [MAIL-7, MAIL-8, MAIL-9, MAIL-10]"));
        assertTrue(all.contains("sent: 10 of 10, each exactly once; waiting now 0"));
    }

    @Test
    void duplicates() {
        assertTrue(all.contains("the customer gets 2 emails; duplicates 1"));
        assertTrue(all.contains("10 emails cost 10 forced disk writes"));
    }
}
