package com.jk.explore.testdouble;

/**
 * A stub: gives a canned answer to every call, so a test can steer checkout down one path.
 */
public final class StubGateway implements PaymentGateway {

    private final Result answer;

    public StubGateway(Result answer) {
        this.answer = answer;
    }

    @Override
    public Result charge(String orderId, long pence) {
        return answer;
    }

    @Override
    public void refund(String receiptId) {
    }
}
