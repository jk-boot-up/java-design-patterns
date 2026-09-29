package com.jk.explore.routingslip;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 * The pattern: decide an order's route once, attach it to the message as a slip, and let each step pass the order to the next address on it.
 */
public final class RoutingSlip {

    private final List<Function<OrderMessage, List<String>>> extraRules = new ArrayList<>();
    private final Map<String, Predicate<OrderMessage>> steps = Steps.all();
    private int visits;

    /** Works out the slip from what the order is, once, at the start. */
    public List<String> slipFor(OrderMessage m) {
        List<String> slip = new ArrayList<>(List.of("validate"));
        if (m.ageRestricted()) {
            slip.add("age-check");
        }
        if (!m.country().equals("UK")) {
            slip.add("customs");
        }
        extraRules.forEach(r -> slip.addAll(r.apply(m)));
        slip.add("charge");
        if (m.gift()) {
            slip.add("gift-wrap");
        }
        slip.add("pack");
        return slip;
    }

    public RoutingSlip addRule(Function<OrderMessage, List<String>> rule) {
        extraRules.add(rule);
        return this;
    }

    /** Each step does its job and hands on to whatever the slip says is next. */
    public String route(OrderMessage m) {
        m.slip(slipFor(m));
        String step;
        while ((step = m.nextStep()) != null) {
            visits++;
            m.visited(step);
            if (!steps.get(step).test(m)) {
                return "stopped at " + step + "; still on the slip: " + m.slip();
            }
        }
        return "done";
    }

    public int visits() {
        return visits;
    }
}
