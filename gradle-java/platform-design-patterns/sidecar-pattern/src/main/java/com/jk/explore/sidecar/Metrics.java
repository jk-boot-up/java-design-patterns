package com.jk.explore.sidecar;

/**
 * The counters one service keeps about its own calls to the payment gateway.
 *
 * <p>Every service needs these and every service has written them itself, which is the
 * fourth of the four copied concerns. They are also the reason a duplicated concern is
 * hard to spot: each of these counters is correct, and each dashboard built on one of
 * them looks healthy, because a service can only ever show you its own quarter of the
 * picture.
 */
public final class Metrics {

    private final String prefix;
    private int attempted;
    private int succeeded;
    private int failed;

    public Metrics(String prefix) {
        this.prefix = prefix;
    }

    public void attempted() {
        attempted++;
    }

    public void succeeded() {
        succeeded++;
    }

    public void failed() {
        failed++;
    }

    public int attempts() {
        return attempted;
    }

    public int successes() {
        return succeeded;
    }

    public int failures() {
        return failed;
    }

    public String prefix() {
        return prefix;
    }

    public String line() {
        return prefix + ".attempts=" + attempted
                + " " + prefix + ".ok=" + succeeded
                + " " + prefix + ".failed=" + failed;
    }
}
