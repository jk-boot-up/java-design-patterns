package com.jk.explore.sidecarjavaproxy;

import java.util.List;

/**
 * The proxy §41 actually deployed, behaving here the way the real one behaves there.
 *
 * <p>Twenty lines of nginx configuration, mounted into a container that somebody else
 * wrote, tested, hardened and has been patching for twenty years. It terminates TLS,
 * writes a structured access log, presents the right certificate and retries a failed
 * payment up to three times, and the shop maintains none of it. On almost every count
 * this is the better answer, and this project would rather you kept it.
 *
 * <p><b>It has one gap, and the gap is not a bug.</b> nginx retries by moving to the
 * next server in the upstream group, which is why §41's configuration lists the same
 * address three times. Moving to the next server happens immediately. There is no
 * directive anywhere in the http proxy module that says "wait two hundred milliseconds
 * first", because nginx's retry was designed for a pool of machines where the next
 * machine is a different machine and is probably fine. When every entry in the pool is
 * the one address that is currently unwell, three immediate attempts are three attempts
 * at exactly the same unwell thing, inside the same three milliseconds.
 *
 * <p>So the provider's March letter — <em>at most three attempts, and wait properly
 * between them</em> — is a sentence nginx can honour half of. The half it honours is the
 * half that limits the shop. The half it drops is the half that would have helped.
 *
 * @see JavaProxy the forty lines that close the gap, and everything that costs
 */
public final class NginxProxy implements Proxy {

    /** The cost of crossing to a neighbouring process and back, per attempt. */
    public static final long HOP_MILLIS = 1;

    /** The configuration file, without its comments. */
    public static final int LINES = 22;

    private final String besideService;
    private final PaymentGateway provider;
    private final ProxyPolicy policy;
    private final Clock clock = new Clock();

    public NginxProxy(String besideService, PaymentGateway provider, ProxyPolicy policy) {
        this.besideService = besideService;
        this.provider = provider;
        this.policy = policy;
    }

    @Override
    public String name() {
        return "nginx";
    }

    @Override
    public String language() {
        return "nginx configuration";
    }

    @Override
    public int lines() {
        return LINES;
    }

    @Override
    public List<String> cannotExpress() {
        // One entry, and it is the one the provider asked for by name.
        return List.of("wait " + policy.firstBackoffMillis()
                + "ms between attempts, doubling");
    }

    /**
     * Up to three attempts, back to back, exactly as {@code proxy_next_upstream_tries 3}
     * does it against an upstream group of three identical entries.
     *
     * <p>Compare this loop with {@link JavaProxy#forward}. They are the same loop with
     * one statement missing, and that statement is not missing because whoever wrote
     * this forgot it. It is missing because there is nothing to write it with.
     */
    @Override
    public Receipt forward(Payment payment) {
        clock.reset();
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
                    // `proxy_next_upstream error timeout http_503` and nothing else: a
                    // 429 is the account's allowance being spent, and retrying a refusal
                    // is how one service's stale policy takes down everybody's payments.
                    break;
                }
                // And here is where the waiting would go, if it could be said at all.
            }
        }
        throw lastFailure;
    }
}
