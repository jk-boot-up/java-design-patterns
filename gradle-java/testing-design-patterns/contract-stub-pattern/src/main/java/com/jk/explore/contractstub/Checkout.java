package com.jk.explore.contractstub;

import java.util.Map;

/**
 * The consumer: checkout charges the card and reads the payment service's reply.
 */
public final class Checkout {

    private final PaymentProvider payments;

    public Checkout(PaymentProvider payments) {
        this.payments = payments;
    }

    public String pay(String amount, String card, String currency) {
        Map<String, String> reply = payments.charge(Map.of("amount", amount, "card", card, "currency", currency));
        String result = reply.get("result");
        if (result == null) {
            return "order stuck: no result in the reply";
        }
        return switch (result) {
            case "APPROVED" -> "order confirmed";
            case "DECLINED" -> "card declined: " + reply.get("reason");
            default -> "payment rejected: " + reply.get("reason");
        };
    }
}
