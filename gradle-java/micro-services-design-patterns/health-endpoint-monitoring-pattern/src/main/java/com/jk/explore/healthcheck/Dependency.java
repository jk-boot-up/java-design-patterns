package com.jk.explore.healthcheck;

/**
 * Something checkout relies on, such as its database or the payment provider, which can be up or down.
 *
 * <p>A critical dependency is one checkout cannot take an order without. A
 * non-critical one, such as product recommendations, only makes the page
 * poorer when it is missing.
 */
public final class Dependency {

    private final String name;
    private final boolean critical;
    private boolean up = true;
    private int checks;

    public Dependency(String name, boolean critical) {
        this.name = name;
        this.critical = critical;
    }

    public boolean check() {
        checks++;
        return up;
    }

    public void setUp(boolean up) {
        this.up = up;
    }

    public String name() {
        return name;
    }

    public boolean critical() {
        return critical;
    }

    public int checks() {
        return checks;
    }
}
