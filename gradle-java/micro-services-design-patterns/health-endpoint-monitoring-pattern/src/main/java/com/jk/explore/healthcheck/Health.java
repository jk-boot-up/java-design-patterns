package com.jk.explore.healthcheck;

/**
 * A health answer: the HTTP code a checker sees, a one-word status, and what was found.
 */
public record Health(int code, String status, String detail) {

    @Override
    public String toString() {
        return code + " " + status + (detail.isEmpty() ? "" : " (" + detail + ")");
    }
}
