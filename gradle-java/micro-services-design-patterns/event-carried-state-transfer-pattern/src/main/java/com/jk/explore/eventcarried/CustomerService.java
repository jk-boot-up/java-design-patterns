package com.jk.explore.eventcarried;

import java.util.HashMap;
import java.util.Map;

/**
 * The owner of customer data. It can be taken down to show who still depends on it.
 */
public final class CustomerService {

    private final Map<String, Address> addresses = new HashMap<>();
    private final Map<String, Integer> versions = new HashMap<>();
    private boolean up = true;
    private int lookups;

    public Events.AddressChanged move(String customerId, Address address) {
        addresses.put(customerId, address);
        int version = versions.merge(customerId, 1, Integer::sum);
        return new Events.AddressChanged(customerId, address, version);
    }

    public Address lookup(String customerId) {
        lookups++;
        if (!up) {
            throw new IllegalStateException("customer service is down");
        }
        return addresses.get(customerId);
    }

    public void setUp(boolean up) {
        this.up = up;
    }

    public int lookups() {
        return lookups;
    }
}
