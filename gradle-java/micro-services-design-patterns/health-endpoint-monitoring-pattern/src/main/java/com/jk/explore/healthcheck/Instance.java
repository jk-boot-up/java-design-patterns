package com.jk.explore.healthcheck;

import java.util.List;

/**
 * One running copy of the checkout service. Its port can be open while it is stuck and cannot take orders.
 */
public final class Instance {

    private final String name;
    private final List<Dependency> dependencies;
    private boolean stuck;
    private int restarts;

    public Instance(String name, List<Dependency> dependencies) {
        this.name = name;
        this.dependencies = dependencies;
    }

    /** Takes an order, or fails if the instance is stuck or a critical dependency is down. */
    public boolean placeOrder() {
        if (stuck) {
            return false;
        }
        return dependencies.stream().filter(Dependency::critical).allMatch(d -> d.check());
    }

    public boolean portOpen() {
        return true;
    }

    public void restart() {
        restarts++;
        stuck = false;
    }

    public void setStuck(boolean stuck) {
        this.stuck = stuck;
    }

    public boolean stuck() {
        return stuck;
    }

    public String name() {
        return name;
    }

    public List<Dependency> dependencies() {
        return dependencies;
    }

    public int restarts() {
        return restarts;
    }
}
