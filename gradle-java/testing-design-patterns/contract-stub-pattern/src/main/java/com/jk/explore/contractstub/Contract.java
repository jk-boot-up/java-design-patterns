package com.jk.explore.contractstub;

import java.util.List;
import java.util.Map;

/**
 * The contract between checkout and payments, written once and used on both sides:
 * checkout tests run against a stub made from it, and the payment service is checked against it.
 */
public record Contract(List<Interaction> interactions) {

    public static Contract payments() {
        return new Contract(List.of(
                new Interaction("a normal charge is approved",
                        Map.of("amount", "20.00", "card", "4000000000000001", "currency", "GBP"),
                        Map.of("result", "APPROVED", "reason", "")),
                new Interaction("a card with no funds is declined",
                        Map.of("amount", "20.00", "card", "4000000000000002", "currency", "GBP"),
                        Map.of("result", "DECLINED", "reason", "insufficient funds")),
                new Interaction("a zero amount is rejected",
                        Map.of("amount", "0.00", "card", "4000000000000001", "currency", "GBP"),
                        Map.of("result", "REJECTED", "reason", "amount must be positive"))));
    }
}
