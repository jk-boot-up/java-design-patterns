package com.jk.explore.observerspring;

import org.springframework.context.event.EventListener;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
public class AnalyticsListener {

    private final Journal journal;

    public AnalyticsListener(Journal journal) {
        this.journal = journal;
    }

    @EventListener
    @Order(3)
    public void onChanged(OrderStatusChanged event) {
        journal.add("analytics: counted " + event.orderId() + " as " + event.to());
    }
}
