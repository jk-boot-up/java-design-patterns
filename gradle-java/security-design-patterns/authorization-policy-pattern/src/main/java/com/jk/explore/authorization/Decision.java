package com.jk.explore.authorization;

/**
 * The answer, with the reason, so every decision can be explained and logged.
 */
public record Decision(boolean allowed, String reason) {

    @Override
    public String toString() {
        return (allowed ? "ALLOW" : "DENY") + " (" + reason + ")";
    }
}
