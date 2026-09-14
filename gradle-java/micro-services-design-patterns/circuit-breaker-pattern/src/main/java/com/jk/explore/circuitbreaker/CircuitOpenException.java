package com.jk.explore.circuitbreaker;

/**
 * Thrown instead of making a call, because the breaker is open.
 *
 * This is a refusal, not a failure — nothing was attempted. It arrives in
 * microseconds rather than after a three-second timeout, and that speed is the
 * entire benefit of the pattern.
 */
public class CircuitOpenException extends RuntimeException {

    private final String serviceName;

    public CircuitOpenException(String serviceName) {
        super(serviceName + " is not being called: the circuit is open");
        this.serviceName = serviceName;
    }

    public String serviceName() {
        return serviceName;
    }
}
