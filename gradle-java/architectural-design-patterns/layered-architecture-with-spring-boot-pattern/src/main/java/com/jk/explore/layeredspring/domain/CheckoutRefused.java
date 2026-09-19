package com.jk.explore.layeredspring.domain;

/** A business refusal. It says why, and nothing about HTTP or about how the reason is shown. */
public class CheckoutRefused extends RuntimeException {

    public enum Reason { OUT_OF_STOCK, PAYMENT_DECLINED }

    private final Reason reason;

    public CheckoutRefused(Reason reason, String message) {
        super(message);
        this.reason = reason;
    }

    public Reason reason() {
        return reason;
    }
}
