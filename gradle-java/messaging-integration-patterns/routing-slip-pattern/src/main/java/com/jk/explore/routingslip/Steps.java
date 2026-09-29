package com.jk.explore.routingslip;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Predicate;

/**
 * The processing steps. Each does its one job and says whether the order may carry on; none knows what comes next.
 */
public final class Steps {

    public static Map<String, Predicate<OrderMessage>> all() {
        Map<String, Predicate<OrderMessage>> s = new LinkedHashMap<>();
        s.put("validate", m -> true);
        s.put("age-check", m -> m.ageVerified());
        s.put("customs", m -> true);
        s.put("fraud-check", m -> true);
        s.put("charge", m -> true);
        s.put("gift-wrap", m -> true);
        s.put("pack", m -> true);
        return s;
    }

    private Steps() {
    }
}
