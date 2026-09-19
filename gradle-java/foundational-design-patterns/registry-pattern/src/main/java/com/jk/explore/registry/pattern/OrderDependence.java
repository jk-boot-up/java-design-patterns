package com.jk.explore.registry.pattern;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The symptom teams meet first.</strong> Two tests that share a
 * registry. Each passes on its own. Run in one order both pass; run in the
 * other, one fails. Nothing about either test changed.
 */
public final class OrderDependence {

    private OrderDependence() {
    }

    /** A named test body that throws if it fails. */
    public record NamedTest(String name, Runnable body) {
    }

    /** Runs the tests in the given order, in one shared registry, and reports what happened. Never clears between tests. */
    public static List<String> run(List<NamedTest> tests) {
        Registry.clear();
        List<String> outcomes = new ArrayList<>();
        for (NamedTest t : tests) {
            try {
                t.body().run();
                outcomes.add(t.name() + ": passed");
            } catch (RuntimeException | AssertionError e) {
                outcomes.add(t.name() + ": FAILED (" + e.getMessage() + ")");
            }
        }
        Registry.clear();
        return outcomes;
    }
}
