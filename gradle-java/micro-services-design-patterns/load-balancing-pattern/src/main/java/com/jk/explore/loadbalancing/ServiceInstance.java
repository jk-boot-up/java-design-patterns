package com.jk.explore.loadbalancing;

/**
 * One running copy of the Catalog service.
 *
 * The three instances answer identically, so a caller is free to use any of them.
 * They are not equally fast, though, and that is what makes the choice
 * interesting: {@code latencyMillis} is how long this particular box takes, and
 * one of the three in the demo is on older hardware.
 */
public record ServiceInstance(String instanceId, long latencyMillis) {

    @Override
    public String toString() {
        return instanceId;
    }
}
