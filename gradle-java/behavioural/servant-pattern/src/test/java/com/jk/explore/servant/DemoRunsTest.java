package com.jk.explore.servant;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ServantDemo.run());

    @Test
    void copiesDisagree() {
        assertTrue(all.contains("parcel, 2300 g: £6.00 (copy updated)"));
        assertTrue(all.contains("letter, 80 g: £2.50 (copy missed, should be £2.80)"));
    }

    @Test
    void servantIsConsistent() {
        assertTrue(all.contains("LETTER-1 | 80 g | to Bath | £2.80"));
        assertTrue(all.contains("GIFTCARD-1 | 20 g | to York | £2.80"));
    }

    @Test
    void newItem() {
        assertTrue(all.contains("PALLET-1 | 180000 g | to Hull | £289.20"));
    }

    @Test
    void aloneTest() {
        assertTrue(all.contains("1001 g: £4.40, two started kilos"));
    }
}
