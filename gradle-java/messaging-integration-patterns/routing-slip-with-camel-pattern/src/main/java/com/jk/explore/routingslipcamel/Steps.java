package com.jk.explore.routingslipcamel;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The processing steps. Each records a visit, and whether it had any work to do for that order.
 */
public final class Steps {

    public static final List<String> ALL = List.of("validate", "age-check", "customs", "charge", "gift-wrap", "pack");

    private final List<String> visits = new CopyOnWriteArrayList<>();
    private int useful;

    public void visit(String step, Order order) {
        visits.add(order.id() + ":" + step);
        if (applies(step, order)) {
            useful++;
        }
        if (step.equals("age-check") && order.ageRestricted() && order.customerAge() < 18) {
            throw new IllegalStateException(order.id() + " failed its age check");
        }
    }

    static boolean applies(String step, Order o) {
        return switch (step) {
            case "age-check" -> o.ageRestricted();
            case "customs" -> o.international();
            case "gift-wrap" -> o.gift();
            case "fraud-check" -> o.pence() > 50000;
            default -> true;
        };
    }

    public List<String> went(String orderId) {
        List<String> out = new ArrayList<>();
        for (String v : visits) {
            if (v.startsWith(orderId + ":")) {
                out.add(v.substring(orderId.length() + 1));
            }
        }
        return out;
    }

    public int visits() {
        return visits.size();
    }

    public int useful() {
        return useful;
    }
}
