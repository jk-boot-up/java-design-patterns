package com.jk.explore.observerspring;

import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

/** Wants only shipped orders, and says so in a condition on the annotation. */
@Component
public class ShippedOnlyListener {

    private final Journal journal;

    public ShippedOnlyListener(Journal journal) {
        this.journal = journal;
    }

    @EventListener(condition = "#event.to() == 'SHIPPED'")
    public void onShipped(OrderStatusChanged event) {
        journal.add("warehouse feed: pick line for " + event.orderId());
    }
}
