package com.jk.explore.strategyspring;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * The rule chosen by configuration ({@code shipping.rule}). Resolved once, at startup, so an
 * unknown name stops the application from starting instead of failing on a customer's order.
 */
@Component
public class SelectedShipping {

    private final String name;
    private final ShippingCostRule rule;

    public SelectedShipping(Map<String, ShippingCostRule> rules, @Value("${shipping.rule:flat}") String name) {
        this.name = name;
        this.rule = rules.get(name);
        if (rule == null) {
            throw new IllegalArgumentException("shipping.rule is '" + name + "' but the rules are " + new java.util.TreeSet<>(rules.keySet()));
        }
    }

    public String name() {
        return name;
    }

    public long cost(Shipment shipment) {
        return rule.costFor(shipment);
    }
}
