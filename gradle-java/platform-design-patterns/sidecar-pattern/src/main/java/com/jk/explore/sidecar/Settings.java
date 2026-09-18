package com.jk.explore.sidecar;

/**
 * The four cross-cutting decisions every service that calls the payment gateway has to
 * make, gathered into one record so that the demo can print them side by side.
 *
 * <p>Gathering them here is a reporting convenience and nothing more. In the four
 * services these are four separate literals in four separate files in four separate
 * repositories, and that is the whole problem: there is no shared type, no shared build,
 * and no moment at which anybody sees all sixteen values at once. The only reason you get
 * to see them at once in this project is that a demo printed them for you.
 */
public record Settings(int maxAttempts,
                       long firstBackoffMillis,
                       long deadlineMillis,
                       String tlsProfile) {

    /** Four values per service, one per concern the service is carrying itself. */
    public static final int CONCERNS_PER_SERVICE = 4;
}
