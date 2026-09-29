package com.jk.explore.testdouble;

/**
 * A dummy: passed in only because the constructor needs something, and never meant to be used.
 *
 * <p>If it is used, it fails loudly, which turns "I think this path never pays" into a checked fact.
 */
public final class DummyGateway implements PaymentGateway {

    @Override
    public Result charge(String orderId, long pence) {
        throw new AssertionError("the dummy was used: charge(" + orderId + ", " + pence + ")");
    }

    @Override
    public void refund(String receiptId) {
        throw new AssertionError("the dummy was used: refund(" + receiptId + ")");
    }
}
