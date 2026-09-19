package com.jk.explore.aggregate.domain;

/** A rule of the business, broken. It names the rule. */
public class InvariantViolated extends RuntimeException {
    public InvariantViolated(String rule) {
        super(rule);
    }
}
