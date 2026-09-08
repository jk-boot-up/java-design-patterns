package com.jk.explore.strategy;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

/**
 * Turns a campaign name into the rule it selects.
 *
 * <p>This class is worth being careful about, because at a glance it looks
 * like the {@code switch} the pattern was supposed to remove — and a reader
 * who has met the Simple Factory project will recognise the shape immediately.
 * The difference is what it does and how often it changes:
 *
 * <ul>
 *   <li>The naive version branched on the method <em>every time a shipment was
 *       priced</em>, inside the pricing logic, so the decision and the
 *       arithmetic were tangled together and neither could be tested alone.
 *   <li>This branches once, at the edge, to answer a different question:
 *       "which rule is configured today?" Nothing downstream branches again.
 * </ul>
 *
 * <p>Something always has to map configuration onto an object; Strategy does
 * not make that go away, it confines it. In a real store this lookup would be
 * a database table or a feature flag, which is the honest version of the same
 * point — the mapping is data, and the pricing code never sees it.
 */
public final class ShippingRules {

    private static final Map<String, ShippingCostRule> BY_NAME = new LinkedHashMap<>();

    static {
        BY_NAME.put("flat", new FlatRateRule(Money.pounds(4.99)));
        BY_NAME.put("weight", WeightBandedRule.standard());
        BY_NAME.put("distance", DistanceBasedRule.standard());
        BY_NAME.put("campaign", FreeOverThresholdRule.standard());
    }

    private ShippingRules() {
    }

    /**
     * The rule registered under {@code key}.
     *
     * @throws IllegalArgumentException if nothing is registered under it —
     *         quietly falling back to a default would silently charge the
     *         customer the wrong amount for delivery
     */
    public static ShippingCostRule byName(String key) {
        ShippingCostRule rule = BY_NAME.get(key);
        if (rule == null) {
            throw new IllegalArgumentException(
                    "no shipping rule called \"" + key + "\"; known rules are " + BY_NAME.keySet());
        }
        return rule;
    }

    /**
     * Every registered key, in registration order.
     *
     * <p>Wrapped rather than returned directly: a bare {@code keySet()} is a
     * live view, and a caller could {@code remove} from it and delete a rule
     * from the registry.
     */
    public static Set<String> names() {
        return Collections.unmodifiableSet(BY_NAME.keySet());
    }
}
