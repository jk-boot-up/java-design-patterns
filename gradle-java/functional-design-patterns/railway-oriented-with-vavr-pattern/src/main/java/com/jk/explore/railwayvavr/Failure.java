package com.jk.explore.railwayvavr;

/**
 * Why checkout failed, and at which step.
 */
public record Failure(String step, String reason) {

    @Override
    public String toString() {
        return reason + " (at " + step + ")";
    }
}
