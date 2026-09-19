package com.jk.explore.retryr4j;

import io.github.resilience4j.retry.annotation.Retry;
import org.springframework.stereotype.Service;

/** A second layer that also retries: three attempts here, each making three attempts below. */
@Service
public class CheckoutService {

    private final PaymentsClient payments;

    public CheckoutService(PaymentsClient payments) {
        this.payments = payments;
    }

    @Retry(name = "payments")
    public String pay(String idempotencyKey, long pence) {
        return payments.charge(idempotencyKey, pence);
    }
}
