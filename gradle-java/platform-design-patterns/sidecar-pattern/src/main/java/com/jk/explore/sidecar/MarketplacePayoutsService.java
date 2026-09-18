package com.jk.explore.sidecar;

/**
 * Pays the independent sellers who list on the shop, every Friday.
 *
 * <p>Copy three of four, and the service to keep an eye on. It is the last of the four to
 * reach the gateway during the incident in {@code PaymentsDemo}, and it is the one that
 * gets refused — not for anything it did, but because by the time its turn came the
 * merchant account's attempt allowance had already been spent by a service it has never
 * heard of.
 *
 * <p>That is the shape of the problem worth remembering: the code that misbehaves and the
 * code that suffers are in different repositories owned by different teams.
 */
public final class MarketplacePayoutsService implements TakesPayments {

    public static final String NAME = "marketplace-payouts";

    private final PaymentGateway gateway;
    private final Clock clock = new Clock();
    private final Metrics metrics = new Metrics("payouts.payments");

    // --- the four copied concerns, copy 3 of 4 -------------------------------------
    private int maxAttempts = 6;
    private long firstBackoffMillis = 10;
    private long deadlineMillis = 2_000;
    private final String tlsProfile = "TLS1.3";
    // -------------------------------------------------------------------------------

    public MarketplacePayoutsService(PaymentGateway gateway) {
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
