package com.jk.explore.saga;

import java.util.ArrayList;
import java.util.List;

/**
 * The confirmation email: the step with no undo at all.
 *
 * There is no {@code unsend}. Once it is in somebody's inbox it has been read, forwarded,
 * and printed out and stuck on a fridge. The only thing a saga can do about an email it
 * should not have sent is send a second email apologising, which is a new fact and not a
 * compensation.
 *
 * <p>The practical consequence shapes how sagas are ordered: put the steps that cannot be
 * undone at the very end, after everything that might fail.
 */
public final class EmailService {

    public static final long LATENCY_MILLIS = 40;

    private final List<String> sent = new ArrayList<>();
    private final RemoteCall<SagaContext, String> send;

    public EmailService(SimulatedClock clock, CallLog log) {
        this.send = new RemoteCall<>("Email", LATENCY_MILLIS, this::doSend, clock, log);
    }

    public String send(SagaContext context) {
        return send.invoke(context);
    }

    public void failNextSend(int count) {
        send.failNext(count);
    }

    public List<String> sent() {
        return List.copyOf(sent);
    }

    private String doSend(SagaContext context) {
        sent.add("your order " + context.orderId() + " is confirmed");
        return "emailed " + context.customerId();
    }
}
