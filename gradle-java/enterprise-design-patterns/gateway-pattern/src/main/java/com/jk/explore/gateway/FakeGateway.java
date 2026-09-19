package com.jk.explore.gateway;

import java.util.ArrayDeque;
import java.util.List;
import java.util.Queue;

/** A gateway that never leaves the process. Tests decide what it answers, and can count what it was asked. */
public class FakeGateway implements PaymentGateway {

    private final Queue<PaymentStatus> script = new ArrayDeque<>();
    private int calls;

    public FakeGateway willAnswer(PaymentStatus... statuses) {
        script.addAll(List.of(statuses));
        return this;
    }

    public int calls() {
        return calls;
    }

    @Override
    public PaymentResult charge(long pence, String card) {
        calls++;
        PaymentStatus status = script.isEmpty() ? PaymentStatus.APPROVED : script.poll();
        return new PaymentResult(status, status == PaymentStatus.APPROVED ? "FAKE-" + calls : null);
    }
}
