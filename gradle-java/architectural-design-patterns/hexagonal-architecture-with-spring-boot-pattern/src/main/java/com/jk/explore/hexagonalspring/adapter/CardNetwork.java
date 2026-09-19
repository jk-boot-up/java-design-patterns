package com.jk.explore.hexagonalspring.adapter;

import com.jk.explore.hexagonalspring.core.domain.PaymentRefused;
import com.jk.explore.hexagonalspring.core.port.Payments;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicBoolean;

/** The card network, in memory. It can be told to decline the next charge. */
@Component
public class CardNetwork implements Payments {

    private final AtomicBoolean declineNext = new AtomicBoolean();

    public void declineNextCharge() {
        declineNext.set(true);
    }

    @Override
    public void charge(long pence) {
        if (declineNext.getAndSet(false)) {
            throw new PaymentRefused();
        }
    }
}
