package com.jk.explore.sidecar;

/**
 * The one statement of how the shop talks to the payment gateway.
 *
 * <p>This is the artefact the pattern actually produces. In this project it is a Java
 * record because everything here runs in one JVM; in the deployed version it is a small
 * configuration file that the proxy beside each service reads at start-up. Either way the
 * important property is the same and it is a counting property: there is one of it. Four
 * services, four sidecars, one set of numbers. A change to the retry policy is a change
 * to this record, and no service is rebuilt, retested or redeployed for it.
 *
 * <p>Notice what is <em>not</em> here: anything about checkout, refunds, subscriptions or
 * payouts. That is the test for whether a decision belongs in a sidecar. How many times
 * to retry a failed connection is a fact about the network and the provider's contract,
 * and it is true no matter which service is making the call. Whether a refund is allowed
 * after ninety days is a fact about the shop, and it must never move out here.
 */
public record SidecarConfig(int maxAttempts,
                            long firstBackoffMillis,
                            long deadlineMillis,
                            String tlsProfile) {

    /** What the provider asked everyone for in March: at most three, properly spaced. */
    public static SidecarConfig agreedWithTheProvider() {
        return new SidecarConfig(3, 200, 2_000, "TLS1.3");
    }

    /** What the shop used before that review, kept so the demo can show the change. */
    public static SidecarConfig beforeTheReview() {
        return new SidecarConfig(6, 10, 2_000, "TLS1.3");
    }

    public String line() {
        return "maxAttempts=" + maxAttempts
                + " firstBackoff=" + firstBackoffMillis + "ms"
                + " deadline=" + deadlineMillis + "ms"
                + " tls=" + tlsProfile;
    }
}
