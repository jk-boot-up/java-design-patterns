package com.jk.explore.circuitbreaker;

/**
 * Taking the money — the most important thing in the shop.
 *
 * Structurally this is the same as {@link RecommendationsService}: a remote call that
 * sometimes does not answer. What differs is not the failure, it is what the shop is
 * allowed to do about it, and that difference is the second half of this project.
 */
public final class PaymentsService {

    public static final long TIMEOUT_MILLIS = 3_000;
    public static final long HEALTHY_MILLIS = 100;

    private final SimulatedClock clock;
    private final CallLog log;
    private boolean down;
    private int chargesMade;

    public PaymentsService(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    public PaymentsService goDown() {
        this.down = true;
        return this;
    }

    /** Charges the card, or times out. */
    public String charge(String orderId, Money amount) {
        long startedAt = clock.millis();
        if (down) {
            clock.advance(TIMEOUT_MILLIS);
            log.record(startedAt, clock.millis(), "Payments", "TIMEOUT",
                    "no answer in " + TIMEOUT_MILLIS + "ms");
            throw new ServiceUnavailableException("Payments");
        }
        clock.advance(HEALTHY_MILLIS);
        chargesMade++;
        String chargeId = "chg-" + chargesMade;
        log.record(startedAt, clock.millis(), "Payments", "CHARGED",
                chargeId + " " + amount + " for " + orderId);
        return chargeId;
    }

    /** How much money has genuinely moved. */
    public int chargesMade() {
        return chargesMade;
    }
}
