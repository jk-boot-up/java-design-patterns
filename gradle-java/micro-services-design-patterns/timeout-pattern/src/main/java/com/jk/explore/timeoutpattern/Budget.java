package com.jk.explore.timeoutpattern;

import java.util.ArrayList;
import java.util.List;

/** One time budget shared by a series of calls, so the page has a limit and not each call. Numbers, not sleeps. */
public final class Budget {

    public record Outcome(int call, String what, int spentMillis) {
    }

    private Budget() {
    }

    public static List<Outcome> spend(int budget, int... wanted) {
        List<Outcome> outcomes = new ArrayList<>();
        int spent = 0;
        for (int i = 0; i < wanted.length; i++) {
            int allowed = budget - spent;
            if (allowed <= 0) {
                outcomes.add(new Outcome(i + 1, "skipped", 0));
                continue;
            }
            int took = Math.min(wanted[i], allowed);
            spent += took;
            outcomes.add(new Outcome(i + 1, wanted[i] <= allowed ? "answered" : "cut off", took));
        }
        return outcomes;
    }

    public static int total(List<Outcome> outcomes) {
        return outcomes.stream().mapToInt(Outcome::spentMillis).sum();
    }
}
