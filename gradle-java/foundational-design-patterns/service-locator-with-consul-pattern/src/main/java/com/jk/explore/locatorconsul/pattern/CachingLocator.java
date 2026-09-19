package com.jk.explore.locatorconsul.pattern;

import com.jk.explore.locatorconsul.consul.Address;
import com.jk.explore.locatorconsul.consul.ConsulClient;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <strong>The same locator, remembering its answers.</strong> It is faster and
 * asks Consul far less, and it goes stale: it keeps returning an address after
 * the instance behind it has gone, until it is told to look again.
 */
public class CachingLocator implements Locator {

    private final ConsulClient consul;
    private final Map<String, List<Address>> cache = new HashMap<>();
    private int asked;

    public CachingLocator(ConsulClient consul) {
        this.consul = consul;
    }

    @Override
    public Address find(String serviceName) {
        List<Address> known = cache.computeIfAbsent(serviceName, name -> {
            asked++;
            return consul.healthy(name);
        });
        if (known.isEmpty()) {
            cache.remove(serviceName);
            throw new NoHealthyInstance(serviceName);
        }
        return known.get(0);
    }

    public void refresh() {
        cache.clear();
    }

    /** How many times Consul was actually asked. */
    public int timesConsulWasAsked() {
        return asked;
    }
}
