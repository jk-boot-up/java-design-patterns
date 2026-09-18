package com.jk.explore.sidecar;

/**
 * Takes the money while a customer is watching a spinner.
 *
 * <p>This is the first of four services that talk to the payment gateway, and it is the
 * one everybody looks at. Read it and it is unremarkable: it asks the gateway for the
 * money, and if the gateway is having a moment it waits and asks again. Perfectly
 * sensible code, written by a careful person.
 *
 * <p>The trouble is that the next three classes in this package say the same thing in
 * their own words. Four copies of a retry loop, four deadlines, four TLS profiles, four
 * sets of counters — sixteen decisions, none of which is about checkout, refunds, billing
 * or payouts, and all of which live inside them.
 *
 * <p>The values below start at what the shop used before the provider's review, and
 * {@link #applyPolicyReview()} is what an engineer did to this file the week the provider
 * asked everyone to cap attempts at three. In a real shop that method is not a method: it
 * is an edit to these two lines, a pull request, and a release.
 */
public final class CheckoutService implements TakesPayments {

    public static final String NAME = "checkout";

    private final PaymentGateway gateway;
    private final Clock clock = new Clock();
    private final Metrics metrics = new Metrics("checkout.payments");

    // --- the four copied concerns, copy 1 of 4 -------------------------------------
    private int maxAttempts = 6;              // retry
    private long firstBackoffMillis = 10;     // retry
    private long deadlineMillis = 2_000;      // timeout
    private final String tlsProfile = "TLS1.3";  // transport security
    // metrics is the fourth: the Metrics field above
    // -------------------------------------------------------------------------------

    public CheckoutService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    /** The provider's review: at most three attempts, and wait properly between them. */
    public void applyPolicyReview() {
        maxAttempts = 3;
        firstBackoffMillis = 200;
    }

    @Override
    public String name() {
        return NAME;
    }

    @Override
    public Receipt pay(Payment payment) {
        clock.reset();
        long backoff = firstBackoffMillis;
        PaymentFailed lastFailure = null;
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            if (clock.now() > deadlineMillis) {
                break;
            }
            metrics.attempted();
            try {
                String reference = gateway.charge(NAME, payment, clock.now());
                metrics.succeeded();
                return new Receipt(payment.orderRef(), reference, attempt, clock.now());
            } catch (PaymentFailed failure) {
                lastFailure = failure;
                // Being refused for asking too often is not a reason to ask again.
                if (failure.reason() == PaymentFailed.Reason.RATE_LIMITED) {
                    break;
                }
                if (attempt < maxAttempts) {
                    clock.waitFor(backoff);
                    backoff *= 2;
                }
            }
        }
        metrics.failed();
        throw lastFailure;
    }

    public Settings settings() {
        return new Settings(maxAttempts, firstBackoffMillis, deadlineMillis, tlsProfile);
    }

    public Metrics metrics() {
        return metrics;
    }
}
