package com.jk.explore.strategyspring;

import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.TreeSet;

/**
 * The context. Spring collects every {@link ShippingCostRule} bean into a map keyed by bean
 * name, and this class looks one up. It has no branch that depends on which rule it finds.
 */
@Service
public class CheckoutService {

    private final Map<String, ShippingCostRule> rules;

    public CheckoutService(Map<String, ShippingCostRule> rules) {
        this.rules = rules;
    }

    public java.util.Set<String> ruleNames() {
        return new TreeSet<>(rules.keySet());
    }

    public long quote(String ruleName, Shipment shipment) {
        ShippingCostRule rule = rules.get(ruleName);
        if (rule == null) {
            throw new IllegalArgumentException("unknown shipping rule '" + ruleName + "'; known: " + ruleNames());
        }
        return rule.costFor(shipment);
    }
}
