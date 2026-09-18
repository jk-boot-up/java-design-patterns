package com.jk.explore.sidecar;

/**
 * Gives the money back when a customer returns the coffee maker.
 *
 * <p>Copy two of four. Different team, different repository, different release day — and
 * a retry loop that is, line for line, the one in {@link CheckoutService}. Nobody copied
 * it dishonestly. Two competent people reading the same provider documentation write
 * almost the same twenty lines, and once both versions exist there is no mechanism
 * anywhere in the shop that will ever bring them back together.
 */
public final class RefundsService implements TakesPayments {

    public static final String NAME = "refunds";

    private final PaymentGateway gateway;
    private final Clock clock = new Clock();
    private final Metrics metrics = new Metrics("refunds.payments");

    // --- the four copied concerns, copy 2 of 4 -------------------------------------
    private int maxAttempts = 6;
    private long firstBackoffMillis = 10;
    private long deadlineMillis = 2_000;
    private final String tlsProfile = "TLS1.3";
    // -------------------------------------------------------------------------------

    public RefundsService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

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
