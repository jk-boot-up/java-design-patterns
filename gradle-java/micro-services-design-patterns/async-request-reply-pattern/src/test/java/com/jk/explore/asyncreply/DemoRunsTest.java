package com.jk.explore.asyncreply;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", AsyncRequestReplyDemo.run());

    @Test
    void syncTimesOutTwice() {
        assertTrue(all.contains("first try: 504, Gateway Timeout"));
        assertTrue(all.contains("built 2 times; the seller received it 0 times"));
    }

    @Test
    void acceptedAtOnce() {
        assertTrue(all.contains("POST /reports: 202 -> /reports/status/R-1, retry after 2 s, Accepted"));
    }

    @Test
    void pollsThenFetches() {
        assertTrue(all.contains("t=2.0s  status: 200, retry after 2 s, running, 33%"));
        assertTrue(all.contains("t=6.0s  status: 303 -> /reports/R-1, See Other"));
        assertTrue(all.contains("fetch:  200, 412 orders, £18240.50"));
    }

    @Test
    void doubleClickBuildsOnce() {
        assertTrue(all.contains("the report was built 1 time"));
    }

    @Test
    void requestCounts() {
        assertTrue(all.contains("as told: 5 requests instead of 1"));
        assertTrue(all.contains("every 0.1 s: 62 requests"));
    }
}
