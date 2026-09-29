package com.jk.explore.contractstub;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class DemoRunsTest {

    private final String all = String.join("\n", ContractStubDemo.run());

    @Test
    void acts() {
        assertTrue(all.contains("against the hand-written stub: order confirmed"));
        assertTrue(all.contains("payment service version 2: order stuck: no result in the reply"));
        assertTrue(all.contains("card, no funds: card declined: insufficient funds"));
        assertTrue(all.contains("zero amount:    payment rejected: amount must be positive"));
        assertTrue(all.contains("version 1: 3 of 3 interactions match"));
        assertTrue(all.contains("version 2: 0 of 3 match"));
        assertTrue(all.contains("hand-written stub, charge in USD: order confirmed"));
        assertTrue(all.contains("contract stub, charge in USD: no interaction in the contract"));
    }
}
