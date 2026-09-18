package com.jk.explore.sidecar;

/**
 * Any of the four services, after the retry code has been taken out of it.
 *
 * <p>One class replaces four here, and that is not a trick of the demo — it is the
 * measurement. The four services differed from each other only in the cross-cutting code
 * they each carried; take that code out and what is left is a name and a request. The
 * business logic that made checkout different from refunds never lived in the part we
 * removed.
 *
 * <p>Read {@link #pay} and notice everything it does not do. It does not know how many
 * times a payment will be attempted. It does not know what the deadline is, what
 * certificate is presented, or what the counters are called. It cannot retry, because
 * there is no retry code in it to go wrong. If the provider changes its mind about any of
 * that next month, this file is not opened, not rebuilt and not redeployed.
 *
 * <p>That is the trade in one sentence: the service gave up knowing, and got to stop
 * caring.
 */
public final class ServiceBehindASidecar implements TakesPayments {

    private final String name;
    private final Sidecar sidecar;

    public ServiceBehindASidecar(String name, Sidecar sidecar) {
        this.name = name;
        this.sidecar = sidecar;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public Receipt pay(Payment payment) {
        return sidecar.send(payment);
    }

    public Sidecar sidecar() {
        return sidecar;
    }
}
