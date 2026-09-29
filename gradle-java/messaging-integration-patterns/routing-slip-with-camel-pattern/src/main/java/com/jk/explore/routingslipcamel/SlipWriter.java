package com.jk.explore.routingslipcamel;

import java.util.ArrayList;
import java.util.List;

/**
 * Writes each order's slip once, when it sets off. The only place that knows which steps an order needs.
 */
public final class SlipWriter {

    private boolean fraudCheck;

    public List<String> steps(Order o) {
        List<String> s = new ArrayList<>(List.of("validate"));
        if (o.ageRestricted()) {
            s.add("age-check");
        }
        if (o.international()) {
            s.add("customs");
        }
        if (fraudCheck && o.pence() > 50000) {
            s.add("fraud-check");
        }
        s.add("charge");
        if (o.gift()) {
            s.add("gift-wrap");
        }
        s.add("pack");
        return s;
    }

    /** The slip as Camel reads it: endpoint addresses separated by commas. */
    public String slip(Order o) {
        return String.join(",", steps(o).stream().map(n -> "direct:" + n).toList());
    }

    public void addFraudCheck() {
        fraudCheck = true;
    }
}
