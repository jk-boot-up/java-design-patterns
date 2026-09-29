package com.jk.explore.testdouble;

/**
 * The code under test: turns a basket total into a paid order, or explains why not.
 */
public final class Checkout {

    private final PaymentGateway gateway;
    private final boolean chargeInPounds;   // the bug act six plants

    public Checkout(PaymentGateway gateway) {
        this(gateway, false);
    }

    /** A checkout with a planted bug: it sends pounds where the provider expects pence. */
    public static Checkout withPenceBug(PaymentGateway gateway) {
        return new Checkout(gateway, true);
    }

    private Checkout(PaymentGateway gateway, boolean chargeInPounds) {
        this.gateway = gateway;
        this.chargeInPounds = chargeInPounds;
    }

    /** Place an order. An empty basket is refused without ever calling the provider. */
    public String placeOrder(String orderId, long totalPence) {
        if (totalPence <= 0) {
            return "refused: the basket is empty";
        }
        long amount = chargeInPounds ? totalPence / 100 : totalPence;
        PaymentGateway.Result r = gateway.charge(orderId, amount);
        return r.approved() ? "paid, receipt " + r.receiptId() : "not paid: " + r.reason();
    }

    /** Cancel a paid order by refunding its receipt. */
    public void cancel(String receiptId) {
        gateway.refund(receiptId);
    }
}
