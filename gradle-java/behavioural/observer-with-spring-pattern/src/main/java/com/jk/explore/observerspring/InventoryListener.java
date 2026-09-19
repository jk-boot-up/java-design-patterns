package com.jk.explore.observerspring;

import org.springframework.context.event.EventListener;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
public class InventoryListener {

    private final Journal journal;

    public InventoryListener(Journal journal) {
        this.journal = journal;
    }

    @EventListener
    @Order(1)
    public void onChanged(OrderStatusChanged event) {
        journal.add("inventory: released stock for " + event.orderId() + " on " + Thread.currentThread().getName());
    }
}
