package com.jk.explore.contentenricher;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * The customer service, in memory: counts every lookup, and can be switched off to show an outage.
 */
public final class CustomerDirectory {

    private final Map<String, Customer> customers = new HashMap<>();
    private int lookups;
    private boolean up = true;

    public CustomerDirectory add(Customer c) {
        customers.put(c.id(), c);
        return this;
    }

    public Optional<Customer> find(String customerId) {
        if (!up) {
            throw new IllegalStateException("customer service unavailable");
        }
        lookups++;
        return Optional.ofNullable(customers.get(customerId));
    }

    public void moveHouse(String customerId, String newAddress) {
        Customer c = customers.get(customerId);
        customers.put(customerId, new Customer(c.id(), c.name(), newAddress, c.tier()));
    }

    public void setUp(boolean up) {
        this.up = up;
    }

    public int lookups() {
        return lookups;
    }
}
