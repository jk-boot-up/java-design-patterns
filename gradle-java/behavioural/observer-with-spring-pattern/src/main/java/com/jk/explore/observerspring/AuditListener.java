package com.jk.explore.observerspring;

import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.util.concurrent.CountDownLatch;

/** Runs on another thread. The demo holds it at a gate so the ordering is not left to chance. */
@Component
public class AuditListener {

    private final Journal journal;
    private volatile Gate gate = new Gate();
    private volatile CountDownLatch done = new CountDownLatch(1);

    public AuditListener(Journal journal) {
        this.journal = journal;
    }

    /** Holds the next audit until {@link #release()}. */
    void hold() {
        gate = new Gate();
        done = new CountDownLatch(1);
    }

    void release() {
        gate.open();
    }

    CountDownLatch done() {
        return done;
    }

    @Async
    @EventListener(condition = "#event.to() == 'CANCELLED'")
    public void onCancelled(OrderStatusChanged event) {
        gate.await();
        journal.add("audit: recorded " + event.orderId() + " on " + Thread.currentThread().getName());
        done.countDown();
    }
}
