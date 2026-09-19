package com.jk.explore.contract;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Runs a provider's real answer against every consumer's contract, before the provider is released. */
public class Verifier {

    public static List<String> verify(PriceProvider provider, String sku, Contract... contracts) {
        Map<String, Object> answer = provider.price(sku);
        List<String> problems = new ArrayList<>();
        for (Contract c : contracts) {
            for (Map.Entry<String, Type> e : c.expects().entrySet()) {
                Object value = answer.get(e.getKey());
                if (value == null) {
                    problems.add(c.consumer() + " expects " + e.getKey() + " (" + e.getValue().name().toLowerCase() + "): missing");
                } else if (!e.getValue().matches(value)) {
                    problems.add(c.consumer() + " expects " + e.getKey() + " (" + e.getValue().name().toLowerCase() + "): got " + value.getClass().getSimpleName());
                }
            }
        }
        return problems;
    }
}
