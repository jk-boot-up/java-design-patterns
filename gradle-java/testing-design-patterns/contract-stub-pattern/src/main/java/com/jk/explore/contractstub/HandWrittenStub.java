package com.jk.explore.contractstub;

import java.util.Map;

/**
 * Before: the checkout team's own stub, written once from the payment docs and never checked again.
 * It approves anything.
 */
public final class HandWrittenStub implements PaymentProvider {

    @Override
    public Map<String, String> charge(Map<String, String> request) {
        return Map.of("result", "APPROVED", "reason", "");
    }
}
