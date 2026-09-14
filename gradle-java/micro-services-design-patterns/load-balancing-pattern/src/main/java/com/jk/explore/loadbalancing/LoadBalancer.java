package com.jk.explore.loadbalancing;

import java.util.List;

/**
 * How a caller picks which instance to ask.
 *
 * This interface is the pattern, and it is worth saying plainly what it is: this
 * is Strategy. Not "like" Strategy, not "an application of" Strategy — the same
 * structure, with one method, several interchangeable implementations, and a
 * caller that holds one and does not ask which. If you have done
 * {@code behavioural/strategy-pattern}, you have already written this interface
 * once under a different name.
 *
 * <p>What is new is not the shape. It is the context: the choice is now being made
 * about machines rather than about business rules, it is made afresh on every
 * single request, and the caller has information — how slow each instance has been
 * <em>for it</em> — that nothing in the middle of the network can see.
 */
public interface LoadBalancer {

    /**
     * Picks one instance to send this request to.
     *
     * @param candidates every instance currently believed to be running, never
     *        empty
     * @return the one to call
     */
    ServiceInstance choose(List<ServiceInstance> candidates);

    /**
     * Told what actually happened, so a balancer that learns can learn.
     *
     * Most implementations ignore this. That is the point of it being on the
     * interface: round-robin does not care how fast an instance was, and it should
     * not have to pretend to.
     */
    default void observed(ServiceInstance instance, long tookMillis) {
    }

    /** A name for the timeline. */
    String name();
}
