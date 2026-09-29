package com.jk.explore.modularmonolith.payments.internal;

import com.jk.explore.modularmonolith.payments.PaymentsApi;
import java.util.HashMap;
import java.util.Map;

/**
 * Inside payments: its own ledger, which no other module can see.
 */
public final class PaymentsModule implements PaymentsApi {

    private final Map<String, Long> ledger = new HashMap<>();

    @Override
    public String charge(String orderId, long pence) {
        ledger.put(orderId, pence);
        return "pay-" + ledger.size();
    }

    @Override
    public long takenFor(String orderId) {
        return ledger.getOrDefault(orderId, 0L);
    }
}
