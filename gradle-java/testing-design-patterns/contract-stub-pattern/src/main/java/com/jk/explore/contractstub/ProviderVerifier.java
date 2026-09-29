package com.jk.explore.contractstub;

import java.util.ArrayList;
import java.util.List;

/**
 * The other half: replays every interaction in the contract against the real provider,
 * in the provider's own build, and reports each reply that differs.
 */
public final class ProviderVerifier {

    public static List<String> mismatches(Contract contract, PaymentProvider provider) {
        List<String> problems = new ArrayList<>();
        for (Interaction i : contract.interactions()) {
            if (!provider.charge(i.request()).equals(i.reply())) {
                problems.add(i.description());
            }
        }
        return problems;
    }

    private ProviderVerifier() {
    }
}
