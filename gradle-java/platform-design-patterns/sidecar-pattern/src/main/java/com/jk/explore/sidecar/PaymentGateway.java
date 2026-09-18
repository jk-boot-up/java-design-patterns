package com.jk.explore.sidecar;

import java.util.HashMap;
import java.util.Map;

/**
 * The payment provider, as the shop experiences it from the outside.
 *
 * <p>It is a company, not a class, and the shop does not get to change it. Two of its
 * behaviours drive this entire project.
 *
 * <p><b>It wobbles.</b> For a few hundred milliseconds at a time it declines everything,
 * and then it is fine again. Nothing is broken and nobody needs to be paged; the right
 * response is to wait a moment and ask again. Here the wobble is exact: every attempt
 * made before {@link #recoversAtMillis} is declined, and every attempt made at or after
 * it succeeds.
 *
 * <p><b>It counts.</b> The contract says at most three attempts per payment, and the shop
 * has four services that take payments, so a single wobble may cost the shop at most
 * twelve attempts. The thirteenth is not declined — it is refused, and so is everything
 * after it, for the whole merchant account. That last clause is the one that hurts,
 * because it means one service can spend a quota that a different service needed.
 */
public final class PaymentGateway {

    /** The contract: three attempts per payment, four services that take payments. */
    public static final int ATTEMPTS_ALLOWED_PER_WOBBLE = 12;

    /** How long a wobble lasts. Attempts at or after this point succeed. */
    public static final long RECOVERS_AT_MILLIS = 300;

    private final CallLog callLog = new CallLog();
    private final Map<String, String> charged = new HashMap<>();
    private long recoversAtMillis;
    private boolean enforcingQuota = true;

    /** Puts the gateway into a wobble that ends at {@link #RECOVERS_AT_MILLIS}. */
    public void beginWobble() {
        recoversAtMillis = RECOVERS_AT_MILLIS;
        callLog.clear();
        charged.clear();
    }

    /** A healthy gateway: everything succeeds on the first attempt. */
    public void behave() {
        recoversAtMillis = 0;
        callLog.clear();
        charged.clear();
    }

    public long recoversAtMillis() {
        return recoversAtMillis;
    }

    public CallLog callLog() {
        return callLog;
    }

    /**
     * One attempt to take the money, from one service, at one moment.
     *
     * @param atMillis milliseconds since the wobble began — see {@link Clock}
     */
    public String charge(String service, Payment payment, long atMillis) {
        if (enforcingQuota && callLog.total() >= ATTEMPTS_ALLOWED_PER_WOBBLE) {
            callLog.record(service, payment.orderRef(), atMillis, "rate-limited");
            throw new PaymentFailed(PaymentFailed.Reason.RATE_LIMITED,
                    "429 refused — the account's " + ATTEMPTS_ALLOWED_PER_WOBBLE
                            + "-attempt allowance is spent");
        }
        if (atMillis < recoversAtMillis) {
            callLog.record(service, payment.orderRef(), atMillis, "declined");
            throw new PaymentFailed(PaymentFailed.Reason.WOBBLE,
                    "503 from the gateway: temporarily unable to authorise");
        }
        // The idempotency key is what makes retrying a payment safe at all: a repeat of a
        // payment the gateway has already taken returns the original reference and does
        // not take the money twice.
        String reference = charged.computeIfAbsent(payment.idempotencyKey(),
                key -> "pay_" + payment.orderRef());
        callLog.record(service, payment.orderRef(), atMillis, "charged");
        return reference;
    }

    /**
     * Turns the account-wide quota off, so that a demonstration can show what the retry
     * attempts alone would have been if the gateway had tolerated all of them.
     */
    public void stopEnforcingQuota() {
        enforcingQuota = false;
    }

    public void startEnforcingQuota() {
        enforcingQuota = true;
    }
}
