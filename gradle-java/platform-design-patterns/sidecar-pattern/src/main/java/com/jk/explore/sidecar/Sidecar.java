package com.jk.explore.sidecar;

/**
 * The proxy that stands between one service and the payment gateway.
 *
 * <p>In the deployed version of this pattern a sidecar is a second process running beside
 * the service — its own container, on the same machine, sharing the same network address.
 * The service is configured to send its payment requests to {@code localhost} instead of
 * to the provider, and the sidecar is the thing that actually goes out to the internet.
 * Retrying, giving up, presenting the right certificate and counting what happened are
 * all done out here, where the service cannot see them and does not have to.
 *
 * <p><b>This class is honest about what it is.</b> In one JVM, a proxy that a service
 * talks through is an object wrapping another object, and an object wrapping another
 * object is the Decorator pattern from §11. Nothing in this file would surprise anybody
 * who has read that project. What makes Sidecar a different pattern is not the code —
 * it is where the code runs. A decorator ships inside your service's jar, in your
 * service's language, and changes when your service is rebuilt. A sidecar ships as its
 * own process, may be written in a language nobody on your team knows, and changes when
 * somebody restarts it. The structure is borrowed; the decision is about deployment.
 *
 * <p>Two things here exist only so the demo can show what this costs. {@link #stop()}
 * turns the sidecar off, which is what makes the point that you have added a second thing
 * that can be down to every call you were trying to make more reliable. And
 * {@link #HOP_MILLIS} is the millisecond each attempt spends crossing from the service to
 * the proxy and back — small, real, and paid on every call for the life of the service.
 */
public final class Sidecar {

    /** The cost of going through a neighbouring process instead of straight out. */
    public static final long HOP_MILLIS = 1;

    private final String besideService;
    private final PaymentGateway gateway;
    private final SidecarConfig config;
    private final Clock clock = new Clock();
    private final Metrics metrics;
    private boolean running = true;

    public Sidecar(String besideService, PaymentGateway gateway, SidecarConfig config) {
        this.besideService = besideService;
        this.gateway = gateway;
        this.config = config;
        // The counters are named the same way for every service, because one proxy
        // produces them all. Nobody had to agree on that; nobody could have disagreed.
        this.metrics = new Metrics("sidecar.payments");
    }

    /**
     * Takes the payment on behalf of the service next door, retrying as the one shared
     * configuration says to, and stopping when it says to stop.
     */
    public Receipt send(Payment payment) {
        if (!running) {
            throw new PaymentFailed(PaymentFailed.Reason.NOTHING_LISTENING,
                    "connection refused to localhost — no sidecar beside "
                            + besideService);
        }
        clock.reset();
        long backoff = config.firstBackoffMillis();
        PaymentFailed lastFailure = null;
        for (int attempt = 1; attempt <= config.maxAttempts(); attempt++) {
            if (clock.now() > config.deadlineMillis()) {
                break;
            }
            clock.waitFor(HOP_MILLIS);
            metrics.attempted();
            try {
                String reference = gateway.charge(besideService, payment, clock.now());
                metrics.succeeded();
                return new Receipt(payment.orderRef(), reference, attempt, clock.now());
            } catch (PaymentFailed failure) {
                lastFailure = failure;
                if (failure.reason() == PaymentFailed.Reason.RATE_LIMITED) {
                    break;
                }
                if (attempt < config.maxAttempts()) {
                    clock.waitFor(backoff);
                    backoff *= 2;
                }
            }
        }
        metrics.failed();
        throw lastFailure;
    }

    /** Kills the proxy. Everything the service sends now fails before leaving the box. */
    public void stop() {
        running = false;
    }

    public void start() {
        running = true;
    }

    public boolean running() {
        return running;
    }

    public SidecarConfig config() {
        return config;
    }

    public Metrics metrics() {
        return metrics;
    }

    public String besideService() {
        return besideService;
    }
}
