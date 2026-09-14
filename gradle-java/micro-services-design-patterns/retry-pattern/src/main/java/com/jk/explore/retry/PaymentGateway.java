package com.jk.explore.retry;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The payment gateway: a well-behaved remote service on a bad network.
 *
 * It is worth being clear that nothing in this class is broken. It honours
 * idempotency keys correctly, it declines cards when the bank declines them, and it
 * charges each key exactly once. Every double charge you will see in this project is
 * the caller's doing, not the gateway's.
 *
 * <p>Three kinds of trouble can be scripted onto it:
 * <ul>
 *   <li>{@link #timeOutNext} — the request never arrives. No charge is made.</li>
 *   <li>{@link #loseReplyAfterCharging} — the request arrives, the card <em>is</em>
 *       charged, and the reply is lost on the way home. From the caller's side this
 *       is indistinguishable from the case above, and that is the whole problem.</li>
 *   <li>{@link #declineAlways} — the bank says no. Trying again will not help.</li>
 * </ul>
 */
public final class PaymentGateway {

    /** How long one attempt at the gateway takes, whether it works or not. */
    public static final long GATEWAY_LATENCY_MILLIS = 50;

    private final SimulatedClock clock;
    private final CallLog log;

    private final Map<String, Receipt> chargesByKey = new LinkedHashMap<>();
    private final List<Receipt> charges = new ArrayList<>();

    private int timeoutsRemaining;
    private int lostRepliesRemaining;
    private boolean declineAlways;
    private int attempts;
    private int nextChargeNumber = 1;

    public PaymentGateway(SimulatedClock clock, CallLog log) {
        this.clock = clock;
        this.log = log;
    }

    /** The next {@code count} requests are lost on the way out. Nothing is charged. */
    public PaymentGateway timeOutNext(int count) {
        this.timeoutsRemaining = count;
        return this;
    }

    /**
     * The next {@code count} requests are charged and then the reply is lost.
     *
     * This is the dangerous failure, and the realistic one.
     */
    public PaymentGateway loseReplyAfterCharging(int count) {
        this.lostRepliesRemaining = count;
        return this;
    }

    /**
     * The bank declines this card, now and every time it is asked.
     *
     * There is no "decline once" here on purpose. A refused card is refused for a
     * reason — no funds, wrong expiry, a block on the account — and that reason is
     * still true a hundred milliseconds later. Modelling it as a one-off would
     * quietly reward a retrier for being wrong.
     */
    public PaymentGateway declineAlways() {
        this.declineAlways = true;
        return this;
    }

    /** Takes the money, unless something has been scripted to go wrong. */
    public Receipt charge(PaymentRequest request) {
        attempts++;
        long startedAt = clock.millis();
        clock.advance(GATEWAY_LATENCY_MILLIS);

        if (timeoutsRemaining > 0) {
            timeoutsRemaining--;
            log.record(startedAt, clock.millis(), "Payments", "TIMEOUT", "request never arrived");
            throw new GatewayTimeoutException("Payments did not answer");
        }

        if (declineAlways) {
            log.record(startedAt, clock.millis(), "Payments", "DECLINED", "the bank said no");
            throw new CardDeclinedException("card declined for " + request.orderId());
        }

        // The key check happens before the charge, which is the entire mechanism.
        Receipt existing = chargesByKey.get(request.idempotencyKey());
        if (existing != null) {
            log.record(startedAt, clock.millis(), "Payments", "REPLAYED",
                    "key already charged, returning " + existing.chargeId());
            return existing;
        }

        Receipt receipt = new Receipt("chg-" + nextChargeNumber++, request.orderId(),
                request.amount());
        chargesByKey.put(request.idempotencyKey(), receipt);
        charges.add(receipt);

        if (lostRepliesRemaining > 0) {
            lostRepliesRemaining--;
            log.record(startedAt, clock.millis(), "Payments", "CHARGED-THEN-LOST",
                    receipt.chargeId() + " taken, reply lost");
            throw new GatewayTimeoutException("Payments did not answer");
        }

        log.record(startedAt, clock.millis(), "Payments", "CHARGED", receipt.toString());
        return receipt;
    }

    /** Every charge the gateway has actually made. The number the customer cares about. */
    public List<Receipt> charges() {
        return List.copyOf(charges);
    }

    /** How much money has left the customer's account in total. */
    public Money totalCharged() {
        return new Money(charges.stream().mapToLong(r -> r.amount().pence()).sum());
    }

    /** How many requests reached the gateway, successful or not. */
    public int attempts() {
        return attempts;
    }
}
