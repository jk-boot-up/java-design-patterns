package com.jk.explore.gateway;

/** The shop's checkout. It knows the gateway's interface and nothing about who is behind it. */
public class Checkout {

    private final PaymentGateway payments;

    public Checkout(PaymentGateway payments) {
        this.payments = payments;
    }

    public String pay(long pence) {
        PaymentResult result = payments.charge(pence, "tok_ada");
        return switch (result.status()) {
            case APPROVED -> "paid, receipt " + result.receipt();
            case DECLINED -> "card declined";
            case UNAVAILABLE -> "payment provider unavailable, try again";
        };
    }
}
