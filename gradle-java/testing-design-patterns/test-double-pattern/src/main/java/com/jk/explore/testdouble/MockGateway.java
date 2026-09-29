package com.jk.explore.testdouble;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * A mock: told in advance exactly which calls to expect, it fails at once on anything else.
 *
 * <p>A spy is checked after the fact; a mock checks as the calls happen, and
 * verify() fails if an expected call never came.
 */
public final class MockGateway implements PaymentGateway {

    private final Deque<String> expected = new ArrayDeque<>();
    private final List<String> unexpected = new ArrayList<>();

    public MockGateway expectCharge(String orderId, long pence) {
        expected.add("charge(" + orderId + ", " + pence + ")");
        return this;
    }

    @Override
    public Result charge(String orderId, long pence) {
        String call = "charge(" + orderId + ", " + pence + ")";
        if (!call.equals(expected.peek())) {
            unexpected.add(call);
            throw new AssertionError("unexpected call: " + call + ", "
                    + (expected.isEmpty() ? "no more charges were expected" : "expected " + expected.peek()));
        }
        expected.poll();
        return Result.approved("mock-1");
    }

    @Override
    public void refund(String receiptId) {
        String call = "refund(" + receiptId + ")";
        unexpected.add(call);
        throw new AssertionError("unexpected call: " + call);
    }

    /** Fails if any expected call never happened. */
    public void verify() {
        if (!expected.isEmpty()) {
            throw new AssertionError("expected but never called: " + expected);
        }
    }
}
