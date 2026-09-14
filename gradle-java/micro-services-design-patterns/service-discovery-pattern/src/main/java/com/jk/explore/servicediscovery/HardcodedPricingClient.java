package com.jk.explore.servicediscovery;

/**
 * The version with the address written into it, and the reason a registry
 * exists.
 *
 * This is what every system starts with, and it is right to start there: one
 * instance, one address, one constant. It works perfectly until the day the set
 * of instances changes — which is every deployment, every autoscaling event and
 * every crash.
 *
 * <p>What makes it worse than it looks is that the failure is not a wrong answer.
 * It is an outage. There is no fallback, because there is nothing to fall back
 * to: the class has been told about exactly one machine and it has no way of
 * finding out about any other.
 */
public final class HardcodedPricingClient {

    /** The address somebody pasted in when there was one instance. */
    private static final String PRICING_INSTANCE = "pricing-1";

    private final PricingCluster cluster;
    private final ServiceInstance pinned;

    public HardcodedPricingClient(PricingCluster cluster, ServiceInstance pinned) {
        this.cluster = cluster;
        this.pinned = pinned;
        if (!PRICING_INSTANCE.equals(pinned.instanceId())) {
            throw new IllegalArgumentException(
                    "this client only knows about " + PRICING_INSTANCE);
        }
    }

    public Money price(String sku) {
        return cluster.endpoint(pinned).invoke(sku);
    }
}
