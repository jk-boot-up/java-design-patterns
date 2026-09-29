package com.jk.explore.ecstkafka;

import java.util.HashMap;
import java.util.Map;

/**
 * The owner of customer addresses. It can be taken down, to show who still depends on it.
 */
public final class CustomerService {

    private final Map<String, String> addresses = new HashMap<>();
    private boolean up = true;
    private int lookups;

    public void move(String customer, String address) {
        addresses.put(customer, address);
    }

    public String lookup(String customer) {
        lookups++;
        if (!up) {
            throw new IllegalStateException("customer service is down");
        }
        return addresses.get(customer);
    }

    public void setUp(boolean up) {
        this.up = up;
    }

    public int lookups() {
        return lookups;
    }
}
