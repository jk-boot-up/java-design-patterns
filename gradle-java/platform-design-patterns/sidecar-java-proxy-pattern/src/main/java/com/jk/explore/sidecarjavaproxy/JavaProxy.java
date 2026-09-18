package com.jk.explore.sidecarjavaproxy;

import java.util.List;

/**
 * The replacement. A proxy written in Java, in about forty lines, that goes in the same
 * place beside the same service and reads the same policy.
 *
 * <p>Everything {@link NginxProxy} does, this does, plus the one sentence nginx had no
 * words for: it waits between attempts, and it doubles the wait each time. That is four
 * extra lines — a variable, an addition and a multiplication — and those four lines are
 * the entire reason this project exists as a separate project.
 *
 * <p><b>Read what is not different.</b> The service next door is not mentioned anywhere
 * in this file except as a name to report. The policy is not hard-coded; it arrives as
 * a parameter, the same instance the nginx proxy was handed. Nothing here knows what the
 * shop sells or what a refund is. A proxy that knew any of that would be a business rule
 * hidden somewhere no developer will think to look, and the swap you are about to watch
 * would stop being safe.
 *
 * <p><b>And read what this costs.</b> Twenty-two lines of somebody else's configuration
 * became forty lines of your own code. Those forty lines are now yours to test, to
 * review, to keep working on the next JDK and to fix at three in the morning. This
 * version has no TLS termination, no access log format, no connection pooling and no
 * twenty-year record of answering CVEs — every one of which nginx brought for free and
 * this file quietly dropped. The trade is worth it here because the gap was the
 * difference between a payment going through and a payment failing. It is not worth it
 * for a gap you could live with.
 */
public final class JavaProxy implements Proxy {

    /** The same hop. Swapping the proxy does not move the service any closer. */
    public static final long HOP_MILLIS = NginxProxy.HOP_MILLIS;

    /** The source of {@link #forward}, its fields and its constructor. */
    public static final int LINES = 40;

    private final String besideService;
    private final PaymentGateway provider;
    private final ProxyPolicy policy;
    private final Clock clock = new Clock();

    public JavaProxy(String besideService, PaymentGateway provider, ProxyPolicy policy) {
        this.besideService = besideService;
        this.provider = provider;
        this.policy = policy;
    }

    @Override
    public String name() {
        return "java-proxy";
    }

    @Override
    public String language() {
        return "Java";
    }

    @Override
    public int lines() {
        return LINES;
    }

    @Override
    public List<String> cannotExpress() {
        // Nothing. Which is the advantage of a general-purpose language, and also the
        // danger of one: there is no longer anything stopping the next person putting
        // the shop's refund rules in here.
        return List.of();
    }

    /**
     * The same loop as {@link NginxProxy#forward}, with the waiting put back in.
     *
     * <p>Three attempts is still three attempts — the provider's allowance is untouched
     * and this proxy is no greedier than the last one. What changed is when the third
     * one arrives. A provider that is unwell for three hundred milliseconds is well
     * again by the time this loop asks for the third time, and unwell for all three of
     * nginx's.
     */
    @Override
    public Receipt forward(Payment payment) {
        clock.reset();
        long backoff = policy.firstBackoffMillis();
        PaymentFailed lastFailure = null;
        for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
            if (clock.now() > policy.deadlineMillis()) {
                break;
            }
            clock.waitFor(HOP_MILLIS);
            try {
                String reference = provider.charge(besideService, payment, clock.now());
                return new Receipt(payment.orderRef(), reference, attempt, clock.now());
            } catch (PaymentFailed failure) {
                lastFailure = failure;
                if (failure.reason() == PaymentFailed.Reason.RATE_LIMITED) {
                    break;
                }
                if (attempt < policy.maxAttempts()) {
                    clock.waitFor(backoff);
                    backoff *= 2;
                }
            }
        }
        throw lastFailure;
    }
}
