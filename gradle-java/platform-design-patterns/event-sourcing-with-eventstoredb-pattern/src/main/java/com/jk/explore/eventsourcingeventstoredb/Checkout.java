package com.jk.explore.eventsourcingeventstoredb;

import java.time.LocalDate;

/**
 * One place a customer can pay with points — the website, or the phone app. Each checkout has its
 * own connection to KurrentDB, as two separate programs would.
 *
 * <p>Paying with points is two steps, and the gap between them is the whole problem. First the
 * checkout <em>looks</em>: it reads the customer's stream and adds it up. Then it <em>decides</em>:
 * if the customer has enough points, it appends a redemption. Anything another checkout writes in
 * the gap is invisible to the decision.
 */
public final class Checkout implements AutoCloseable {

    /** What a checkout saw when it looked: the balance, and the revision it was worked out at. */
    public record Look(int balance, long revision) {
    }

    private final String name;
    private final LoyaltyLog log;

    public Checkout(String name, LoyaltyLog log) {
        this.name = name;
        this.log = log;
    }

    public String name() {
        return name;
    }

    public Look look(String customerId) {
        LoyaltyLog.History history = log.read(customerId);
        return new Look(history.balance(), history.revision());
    }

    /**
     * Step two, with or without the check. Without it the append says "any": the server adds the
     * event whatever has happened since. With it the append says "only if the stream is still at
     * the revision I looked at", and the server refuses if it is not.
     *
     * @return the revision the redemption was written at
     * @throws LoyaltyLog.StreamMovedOn when the check is on and another write got there first
     */
    public long redeem(String customerId, Look seen, int points, String orderId, LocalDate on,
                       LoyaltyLog.Check check) {
        if (points > seen.balance()) {
            throw new IllegalStateException(name + " declines: " + points + " is more than " + seen.balance());
        }
        PointsRedeemed spend = new PointsRedeemed(customerId, points, orderId, on);
        return check == LoyaltyLog.Check.EXPECTED_REVISION
                ? log.appendExpecting(customerId, seen.revision(), EventJson.toEventData(spend))
                : log.append(customerId, EventJson.toEventData(spend));
    }

    @Override
    public void close() {
        log.close();
    }
}
