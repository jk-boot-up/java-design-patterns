package com.jk.explore.locatorconsul.pattern;

import com.jk.explore.locatorconsul.consul.Address;
import com.jk.explore.locatorconsul.consul.ConsulClient;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <strong>The service locator, over real service discovery.</strong> It asks
 * Consul for the healthy instances of a service and rotates through them. What
 * is available is a genuine run-time fact here, which is why this is a
 * legitimate use of the pattern.
 */
public class ConsulLocator implements Locator {

    private final ConsulClient consul;
    private final Map<String, Integer> next = new HashMap<>();

    public ConsulLocator(ConsulClient consul) {
        this.consul = consul;
    }

    @Override
    public Address find(String serviceName) {
        List<Address> healthy = consul.healthy(serviceName);
        if (healthy.isEmpty()) {
            throw new NoHealthyInstance(serviceName);
        }
        int index = next.merge(serviceName, 1, Integer::sum) - 1;
        return healthy.get(index % healthy.size());
    }
}
