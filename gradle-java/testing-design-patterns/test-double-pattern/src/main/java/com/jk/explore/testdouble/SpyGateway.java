package com.jk.explore.testdouble;

import java.util.ArrayList;
import java.util.List;

/**
 * A spy: answers like a stub, and also writes down every call so the test can check them afterwards.
 */
public final class SpyGateway implements PaymentGateway {

    private final List<String> calls = new ArrayList<>();
    private int next = 1;

    @Override
    public Result charge(String orderId, long pence) {
        calls.add("charge(" + orderId + ", " + pence + ")");
        return Result.approved("spy-" + next++);
    }

    @Override
    public void refund(String receiptId) {
        calls.add("refund(" + receiptId + ")");
    }

    public List<String> calls() {
        return List.copyOf(calls);
    }
}
