package com.jk.explore.testdouble;

/**
 * What checkout needs from a payment provider: take money, and give it back.
 *
 * <p>Every test double in this project implements this one interface, which
 * is what lets a test hand checkout a stand-in instead of the real thing.
 */
public interface PaymentGateway {

    /** The provider's answer to a charge. */
    record Result(boolean approved, String receiptId, String reason) {
        public static Result approved(String receiptId) {
            return new Result(true, receiptId, "");
        }

        public static Result declined(String reason) {
            return new Result(false, "", reason);
        }
    }

    /** Charge a customer's card, in pence. */
    Result charge(String orderId, long pence);

    /** Give a charge back, by its receipt id. */
    void refund(String receiptId);
}
