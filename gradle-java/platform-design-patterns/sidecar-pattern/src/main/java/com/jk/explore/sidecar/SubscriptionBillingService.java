package com.jk.explore.sidecar;

/**
 * Charges the saved cards of everyone on a coffee subscription, at two in the morning.
 *
 * <p>Copy four of four, and the one that was missed.
 *
 * <p>Compare this class with the other three and the only difference you will find is an
 * absence: there is no {@code applyPolicyReview()} method here. That absence is the whole
 * point of this project. When the provider asked the shop to cap attempts at three, the
 * change was made in checkout, in refunds and in payouts by the people in the room. This
 * service runs overnight, is owned by the billing team, lives in its own repository, and
 * had no open work that sprint. Nobody was careless. Nobody was even wrong. The change
 * was simply made in three of the four places it existed, because there was no fourth
 * place to look unless you already knew to look there.
 *
 * <p>So this service still retries six times, starting ten milliseconds apart — which is
 * what everybody agreed was reasonable before the review, and is now the behaviour that
 * spends the merchant account's entire attempt allowance before the other three services
 * have finished their first payment.
 */
public final class SubscriptionBillingService implements TakesPayments {

    public static final String NAME = "subscription-billing";

    private final PaymentGateway gateway;
    private final Clock clock = new Clock();
    private final Metrics metrics = new Metrics("billing.payments");

    // --- the four copied concerns, copy 4 of 4 -------------------------------------
    // These two are the pre-review values. There is no method below that changes them.
    private final int maxAttempts = 6;
    private final long firstBackoffMillis = 10;
    private final long deadlineMillis = 2_000;
    private final String tlsProfile = "TLS1.3";
    // -------------------------------------------------------------------------------

    public SubscriptionBillingService(PaymentGateway gateway) {
        this.gateway = gateway;
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
