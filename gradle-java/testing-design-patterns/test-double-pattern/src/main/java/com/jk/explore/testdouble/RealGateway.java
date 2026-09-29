package com.jk.explore.testdouble;

/**
 * A stand-in for the real provider as a test would meet it: slow, needs the network, and charges real money.
 *
 * <p>It keeps a simulated clock (800 ms per call) and a count of real pounds
 * taken, so the demo can show what testing against it costs without waiting.
 */
public final class RealGateway implements PaymentGateway {

    private long elapsedMillis;
    private long realPenceCharged;
    private boolean online = true;
    private int next = 1;

    public void goOffline() {
        online = false;
    }

    @Override
    public Result charge(String orderId, long pence) {
        elapsedMillis += 800;
        if (!online) {
            throw new IllegalStateException("network unreachable");
        }
        realPenceCharged += pence;
        return Result.approved("real-" + next++);
    }

    @Override
    public void refund(String receiptId) {
        elapsedMillis += 800;
    }

    public long elapsedMillis() {
        return elapsedMillis;
    }

    public long realPenceCharged() {
        return realPenceCharged;
    }
}
