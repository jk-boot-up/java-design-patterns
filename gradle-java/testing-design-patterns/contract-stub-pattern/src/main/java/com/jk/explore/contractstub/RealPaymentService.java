package com.jk.explore.contractstub;

import java.util.Map;

/**
 * The payment team's real service. Version 2 renamed the reply field "result" to "outcome".
 */
public final class RealPaymentService implements PaymentProvider {

    private final String resultField;

    public RealPaymentService(int version) {
        this.resultField = version >= 2 ? "outcome" : "result";
    }

    @Override
    public Map<String, String> charge(Map<String, String> request) {
        double amount = Double.parseDouble(request.get("amount"));
        if (amount <= 0) {
            return Map.of(resultField, "REJECTED", "reason", "amount must be positive");
        }
        if (request.get("card").endsWith("0002")) {
            return Map.of(resultField, "DECLINED", "reason", "insufficient funds");
        }
        return Map.of(resultField, "APPROVED", "reason", "");
    }
}
