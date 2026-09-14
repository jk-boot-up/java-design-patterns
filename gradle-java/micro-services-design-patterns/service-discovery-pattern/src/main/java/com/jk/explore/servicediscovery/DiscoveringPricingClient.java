package com.jk.explore.servicediscovery;

import java.util.List;
import java.util.NoSuchElementException;

/**
 * The pattern. A caller that asks the registry where Pricing is, every time,
 * instead of having an address written into it.
 *
 * Two behaviours matter and they are easy to conflate. The first is discovery:
 * look the service up, call whatever you were given. The second is what to do
 * when the answer turns out to be wrong — and it will, because a registry cannot
 * know that a process crashed a second ago. So the client tries the next instance
 * on the list, and gives up only when it has run out.
 *
 * <p>That second behaviour is what makes discovery usable in practice rather than
 * merely correct in theory. A client that trusts the first address it is given
 * fails every time an instance dies, which is precisely the thing discovery was
 * supposed to fix.
 */
public final class DiscoveringPricingClient {

    private final ServiceRegistry registry;
    private final PricingCluster cluster;
    private final CallLog log;

    private int lookups;

    public DiscoveringPricingClient(ServiceRegistry registry, PricingCluster cluster,
                                    CallLog log) {
        this.registry = registry;
        this.cluster = cluster;
        this.log = log;
    }

    /**
     * The price of something, from whichever Pricing instance is up.
     *
     * @throws ServiceUnavailableException if every instance the registry offered
     *         failed, or it offered none at all
     */
    public Money price(String sku) {
        List<ServiceInstance> candidates = registry.instances("Pricing");
        lookups++;
        log.note("Client", "LOOKUP", candidates.size() + " Pricing instance(s) offered");

        if (candidates.isEmpty()) {
            throw new ServiceUnavailableException("Pricing (nothing registered)");
        }

        ServiceUnavailableException lastFailure = null;
        for (ServiceInstance instance : candidates) {
            try {
                return cluster.endpoint(instance).invoke(sku);
            } catch (ServiceUnavailableException e) {
                // A stale entry: the registry believed this one was alive. Note
                // it and move down the list.
                log.note("Client", "STALE", instance.instanceId()
                        + " was on the list but is not answering");
                lastFailure = e;
            }
        }
        throw lastFailure;
    }

    /** How many times the registry has been consulted. */
    public int lookups() {
        return lookups;
    }

    /** The first instance the registry would currently offer. */
    public ServiceInstance anyInstance() {
        return registry.instances("Pricing").stream().findFirst()
                .orElseThrow(() -> new NoSuchElementException("no Pricing registered"));
    }
}
