package com.jk.explore.observer;

import java.util.Objects;

/**
 * One listener that threw, reported rather than swallowed.
 *
 * <p>The alternative designs are both worse. Letting the exception escape means
 * the first broken listener stops the rest, so a bug in the analytics client
 * silently prevents the warehouse feed from being written. Catching it and
 * doing nothing means the same bug is invisible until someone notices the
 * missing rows weeks later. Returning it lets the caller decide, and lets a
 * test assert on it.
 */
public record ListenerFailure(String listenerName, String message) {

    public ListenerFailure {
        Objects.requireNonNull(listenerName, "listenerName");
        Objects.requireNonNull(message, "message");
    }

    static ListenerFailure of(OrderListener listener, RuntimeException cause) {
        String message = cause.getMessage() == null
                ? cause.getClass().getSimpleName()
                : cause.getMessage();
        return new ListenerFailure(listener.name(), message);
    }

    @Override
    public String toString() {
        return listenerName + " failed: " + message;
    }
}
