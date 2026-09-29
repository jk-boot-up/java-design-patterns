package com.jk.explore.memoization;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", MemoizationDemo.run());

    @Test
    void plainRepeatsItself() {
        assertTrue(all.contains("best price for 25: £75.00, after 9,749,473 calls"));
    }

    @Test
    void memoizedIsFast() {
        assertTrue(all.contains("best price for 25: £75.00, after 26 calls"));
    }

    @Test
    void shippingQuotes() {
        assertTrue(all.contains("slow carrier calls: 12, 2,400 ms instead of 200,000 ms"));
    }

    @Test
    void stale() {
        assertTrue(all.contains("the memo still says €116.00, the real price is €112.00"));
    }

    @Test
    void grows() {
        assertTrue(all.contains("100,000 answers kept in memory"));
    }
}
