package com.jk.explore.observer;

/**
 * The observer: something that wants to know when an order moves.
 *
 * <p>Two methods, and the second one only exists so that failures can be
 * reported against a readable name. The interface deliberately does not offer
 * a priority, an ordering hint, or a "should I run?" predicate. Every one of
 * those would be a way for a listener to make claims about the other listeners,
 * and the point of the pattern is that no listener knows there are any others.
 *
 * <p>It is a functional interface in spirit but not in law -- {@link #name()}
 * has no default, so a lambda will not do. That is a trade made on purpose: an
 * anonymous lambda in a listener list is untraceable in a stack trace, and this
 * is exactly the kind of code where a stack trace is all you get.
 */
public interface OrderListener {

    /** How this listener is identified in logs and failure reports. */
    String name();

    /**
     * React to a status change.
     *
     * <p>Implementations must not assume they are called first, last, or at
     * all in relation to any other listener.
     */
    void onStatusChanged(OrderEvent event);
}
