package com.jk.explore.observerspring;

import org.springframework.context.event.EventListener;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;

@Component
public class EmailListener {

    private final Journal journal;
    private final AtomicBoolean mailServerDown = new AtomicBoolean();

    public EmailListener(Journal journal) {
        this.journal = journal;
    }

    public void mailServerDown(boolean down) {
        mailServerDown.set(down);
    }

    @EventListener
    @Order(2)
    public void onChanged(OrderStatusChanged event) {
        if (mailServerDown.get()) {
            throw new IllegalStateException("mail server timed out");
        }
        journal.add("email: told the customer about " + event.orderId());
    }
}
