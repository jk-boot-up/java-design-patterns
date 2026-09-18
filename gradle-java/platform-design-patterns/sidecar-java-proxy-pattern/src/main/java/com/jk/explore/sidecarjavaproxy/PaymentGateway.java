package com.jk.explore.sidecarjavaproxy;

import java.util.HashMap;
import java.util.Map;

/**
 * The payment provider, as the shop experiences it from the outside.
 *
 * <p>It is a company, not a class, and the shop does not get to change it. One behaviour
 * of it drives this entire project: <b>it wobbles</b>. For a few hundred milliseconds at
 * a time it declines everything, and then it is fine again. Nothing is broken and nobody
 * needs to be paged. Here the wobble is exact — every attempt made before
 * {@link #RECOVERS_AT_MILLIS} is declined, and every attempt made at or after it
 * succeeds.
 *
 * <p>That exactness is deliberate, because it turns the project's question into
 * arithmetic. Three attempts inside the first three milliseconds of a three-hundred
 * millisecond wobble all land in the bad window and the payment fails. The same three
 * attempts, spread out, do not. Nothing about the provider changed between those two
 * runs; only the spacing did.
 */
public final class PaymentGateway {

    /** How long a wobble lasts. Attempts at or after this point succeed. */
    public static final long RECOVERS_AT_MILLIS = 300;

    private final CallLog callLog = new CallLog();
    private final Map<String, String> charged = new HashMap<>();
    private long recoversAtMillis;
    private boolean refusing;

    /** Puts the provider into a wobble that ends at {@link #RECOVERS_AT_MILLIS}. */
    public void beginWobble() {
        recoversAtMillis = RECOVERS_AT_MILLIS;
        refusing = false;
        reset();
    }

    /** A healthy provider: everything succeeds on the first attempt. */
    public void behave() {
        recoversAtMillis = 0;
        refusing = false;
        reset();
    }

    /**
     * The merchant account's allowance is spent, and the provider is refusing outright.
     *
     * <p>This is a different animal from a wobble and the difference decides how a proxy
     * should behave. A decline means "not right now"; a refusal means "you personally
     * are asking too often", and asking again is precisely how one service's retries
     * take down every other service's payments. Both proxies in this project stop on a
     * refusal, which is one of the few things they agree about completely.
     */
    public void refuseEverything() {
        refusing = true;
        reset();
    }

    private void reset() {
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
        if (refusing) {
            callLog.record(service, payment.orderRef(), atMillis, "rate-limited");
            throw new PaymentFailed(PaymentFailed.Reason.RATE_LIMITED,
                    "429 refused — the merchant account's allowance is spent");
        }
        if (atMillis < recoversAtMillis) {
            callLog.record(service, payment.orderRef(), atMillis, "declined");
            throw new PaymentFailed(PaymentFailed.Reason.WOBBLE,
                    "503 from the provider: temporarily unable to authorise");
        }
        // The idempotency key is what makes retrying safe: a repeat of a payment the
        // provider has already taken returns the original reference rather than taking
        // the money a second time.
        String reference = charged.computeIfAbsent(payment.idempotencyKey(),
                key -> "pay_" + payment.orderRef());
        callLog.record(service, payment.orderRef(), atMillis, "charged");
        return reference;
    }
}
