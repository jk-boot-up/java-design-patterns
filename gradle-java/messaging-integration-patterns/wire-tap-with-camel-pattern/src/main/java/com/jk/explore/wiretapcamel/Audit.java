package com.jk.explore.wiretapcamel;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The audit log fed by the wire tap. It masks card numbers, and can be made slow.
 */
public final class Audit {

    private final List<String> lines = new CopyOnWriteArrayList<>();
    private volatile long delayMillis;

    public void record(PaymentMessage m) throws InterruptedException {
        if (delayMillis > 0) {
            Thread.sleep(delayMillis);   // an audit store that answers slowly
        }
        m.setCard("**** " + m.getCard().substring(m.getCard().length() - 4));
        lines.add("audit: " + m);
    }

    public List<String> lines() {
        return lines;
    }

    public void setDelayMillis(long delayMillis) {
        this.delayMillis = delayMillis;
    }

    /** Waits, up to a limit, until the tap has delivered {@code expected} copies. */
    public boolean awaitLines(int expected, long timeoutMillis) throws InterruptedException {
        long deadline = System.currentTimeMillis() + timeoutMillis;
        while (lines.size() < expected && System.currentTimeMillis() < deadline) {
            Thread.sleep(5);
        }
        return lines.size() >= expected;
    }
}
