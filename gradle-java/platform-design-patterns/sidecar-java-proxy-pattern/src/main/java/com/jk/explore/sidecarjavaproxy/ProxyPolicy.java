package com.jk.explore.sidecarjavaproxy;

/**
 * The one statement of how the shop talks to the payment provider.
 *
 * <p>This is the artefact §41 produced, and this project changes nothing about it. Both
 * proxies here read this same record; neither of them was written with the other in
 * mind; and the service next door has never heard of it. That is what makes a proxy
 * swappable at all — the policy is an input to the proxy rather than something baked
 * into whichever one happens to be installed.
 *
 * <p>The field worth staring at is {@link #firstBackoffMillis}. The provider asked for
 * it in writing: at most three attempts, <em>and wait properly between them</em>. One of
 * the two proxies in this project can honour that sentence and the other one cannot, and
 * both of them are handed this identical record. A policy is only as real as the thing
 * reading it.
 */
public record ProxyPolicy(int maxAttempts,
                          long firstBackoffMillis,
                          long deadlineMillis,
                          String tlsProfile) {

    /** What the provider asked every merchant for: at most three, properly spaced. */
    public static ProxyPolicy agreedWithTheProvider() {
        return new ProxyPolicy(3, 200, 2_000, "TLS1.3");
    }

    public String line() {
        return "maxAttempts=" + maxAttempts
                + " firstBackoff=" + firstBackoffMillis + "ms"
                + " deadline=" + deadlineMillis + "ms"
                + " tls=" + tlsProfile;
    }
}
