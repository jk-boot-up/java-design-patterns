package com.jk.explore.circuitbreaker;

/**
 * Checkout with a fallback that lies. The worst thing in this project.
 *
 * It is built exactly like {@link CheckoutService} and differs in one respect: when
 * Payments cannot be reached it returns a made-up receipt instead of an error. Every
 * dashboard goes green. The shopper sees "thank you for your order". No exception is
 * thrown, no alert fires, and the warehouse ships an espresso machine that nobody
 * paid for.
 *
 * <p>This exists because "add a fallback" is the advice that comes attached to this
 * pattern, and it is only good advice when there is something true to fall back to.
 * An empty list of suggestions is true — the shop really has no suggestions to show.
 * A receipt for money that never moved is not true, and a fallback that hides a real
 * failure is worse than the error it replaced: the error would have been noticed in
 * seconds, and this will be noticed at the end of the month.
 */
public final class PretendItWorkedCheckoutService {

    private final PaymentsService payments;
    private final CircuitBreaker breaker;
    private final CallLog log;

    public PretendItWorkedCheckoutService(PaymentsService payments, CircuitBreaker breaker,
                                          CallLog log) {
        this.payments = payments;
        this.breaker = breaker;
        this.log = log;
    }

    /** Always succeeds. That is the bug. */
    public String pay(String orderId, Money amount) {
        try {
            return breaker.call(() -> payments.charge(orderId, amount));
        } catch (RuntimeException anything) {
            log.note("Checkout", "PRETENDED", "returned a receipt for money that never moved");
            return "chg-assumed-ok";
        }
    }
}
