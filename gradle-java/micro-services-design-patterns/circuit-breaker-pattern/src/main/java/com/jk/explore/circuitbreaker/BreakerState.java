package com.jk.explore.circuitbreaker;

/**
 * The three states, named after the fuse box the pattern is named after.
 *
 * The vocabulary is the one thing worth learning here, because it reads backwards
 * to most people: <strong>closed is the healthy state</strong>. A closed circuit is
 * one where current flows, so calls go through. An <em>open</em> circuit is broken,
 * so calls do not.
 */
public enum BreakerState {

    /** Healthy. Calls go through, failures are counted. */
    CLOSED,

    /** Tripped. Calls are refused instantly, without touching the service. */
    OPEN,

    /**
     * Testing the water. Exactly one call is let through to see whether the service
     * has recovered — if it works the breaker closes, if it fails the breaker opens
     * again for another full wait.
     */
    HALF_OPEN
}
