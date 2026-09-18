package com.jk.explore.sidecar;

/**
 * Counts the two things that are easy to confuse when arguing about this pattern: how
 * many <em>processes</em> you are running, and how many <em>places a decision lives</em>.
 *
 * <p>A sidecar does not reduce the first number. Four services with a proxy each is eight
 * processes where there were four, and every one of those proxies wants memory, a version,
 * a restart when it is patched and a line in somebody's on-call runbook. Anybody who tells
 * you this pattern simplifies your deployment has not counted.
 *
 * <p>What it reduces is the second number, and the second number is the one that caused
 * the incident. Four copies of a retry policy is four chances to update three of them.
 */
public final class Concerns {

    /** Retry, deadline, transport security, counters. */
    public static final int CROSS_CUTTING_CONCERNS = Settings.CONCERNS_PER_SERVICE;

    private Concerns() {
    }

    /** Four concerns written out once inside each service. */
    public static int copiesInsideTheServices(int services) {
        return services * CROSS_CUTTING_CONCERNS;
    }

    /**
     * How many files an engineer has to find and edit to change one policy.
     *
     * <p>They also have to know that all four exist, which is the part no tool checks.
     */
    public static int placesToEditAPolicy(int services) {
        return services;
    }

    /**
     * Four concerns, stated once, beside every service.
     *
     * <p>This method takes no argument, and the missing argument is the answer. The number
     * of concerns does not grow with the number of services, because the services are no
     * longer where the concerns are written down.
     */
    public static int copiesBesideTheServices() {
        return CROSS_CUTTING_CONCERNS;
    }

    /** One {@link SidecarConfig}, however many services read it. */
    public static int placesToEditAPolicyWithSidecars() {
        return 1;
    }

    /** The honest half: a proxy process for every service instance, plus the services. */
    public static int processesToRun(int services, boolean withSidecars) {
        return withSidecars ? services * 2 : services;
    }
}
