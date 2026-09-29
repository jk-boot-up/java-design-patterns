package com.jk.explore.immutable;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ImmutableObjectDemo.run());

    @Test
    void sharedAddressMoves() {
        assertTrue(all.contains("ORD-1 now ships to: 12 High Street, York"));
    }

    @Test
    void halfAppliedSale() {
        assertTrue(all.contains("reads after the first: £62.00"));
        assertTrue(all.contains("basket after the sale: £58.50"));
    }

    @Test
    void lostInSet() {
        assertTrue(all.contains("set contains it: false, although the set's size is 1"));
    }

    @Test
    void immutableVersionsHold() {
        assertTrue(all.contains("ORD-2 still ships to 4 Mill Lane, Leeds"));
        assertTrue(all.contains("checkout still reads £65.00"));
        assertTrue(all.contains("checkout now reads £58.50, never a mix"));
        assertTrue(all.contains("kettle still £30.00"));
        assertTrue(all.contains("set contains 9 Park Road: true"));
    }

    @Test
    void copyCost() {
        assertTrue(all.contains("a new list of 1000 entries"));
    }
}
