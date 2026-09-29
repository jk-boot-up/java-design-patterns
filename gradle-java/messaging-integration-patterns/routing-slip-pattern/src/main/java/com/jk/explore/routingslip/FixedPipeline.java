package com.jk.explore.routingslip;

import java.util.List;

/**
 * Without the pattern: every order passes through every step, and each step must check whether it applies.
 */
public final class FixedPipeline {

    static final List<String> EVERY_STEP = List.of("validate", "age-check", "customs", "charge", "gift-wrap", "pack");

    private int visits;
    private int useful;

    public void process(OrderMessage m) {
        for (String step : EVERY_STEP) {
            visits++;
            boolean applies = switch (step) {
                case "age-check" -> m.ageRestricted();
                case "customs" -> !m.country().equals("UK");
                case "gift-wrap" -> m.gift();
                default -> true;
            };
            if (applies) {
                useful++;
                m.visited(step);
            }
        }
    }

    public int visits() {
        return visits;
    }

    public int useful() {
        return useful;
    }
}
