package com.jk.explore.boundedcontext.sales;

import com.jk.explore.boundedcontext.shared.CustomerId;
import com.jk.explore.boundedcontext.shared.CustomerRenamed;
import com.jk.explore.boundedcontext.shared.EventBus;

import java.util.HashMap;
import java.util.Map;

public class SalesContext {

    private final Map<CustomerId, Buyer> buyers = new HashMap<>();
    private final EventBus bus;

    public SalesContext(EventBus bus) {
        this.bus = bus;
    }

    public void register(Buyer buyer) {
        buyers.put(buyer.id(), buyer);
    }

    public Buyer buyer(CustomerId id) {
        return buyers.get(id);
    }

    public void rename(CustomerId id, String newName) {
        Buyer old = buyers.get(id);
        buyers.put(id, new Buyer(id, newName, old.creditLimitPence(), old.lastPurchase()));
        bus.publish(new CustomerRenamed(id, newName));
    }
}
