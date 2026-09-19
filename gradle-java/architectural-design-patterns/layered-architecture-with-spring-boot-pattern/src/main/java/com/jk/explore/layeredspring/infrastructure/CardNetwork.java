package com.jk.explore.layeredspring.infrastructure;

import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;

/** The card network, in memory: it can be told to decline the next charge. */
@Component
public class CardNetwork {

    private final AtomicBoolean declineNext = new AtomicBoolean();

    public void declineNextCharge() {
        declineNext.set(true);
    }

    public void charge(long pence) {
        if (declineNext.getAndSet(false)) {
            throw new PaymentDeclined();
        }
    }
}
