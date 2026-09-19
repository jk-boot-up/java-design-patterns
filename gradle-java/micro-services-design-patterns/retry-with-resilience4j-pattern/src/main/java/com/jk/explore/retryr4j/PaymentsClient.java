package com.jk.explore.retryr4j;

import io.github.resilience4j.retry.annotation.Retry;
import org.springframework.stereotype.Service;

@Service
public class PaymentsClient {

    private final PaymentGateway gateway;

    public PaymentsClient(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    @Retry(name = "payments")
    public String charge(String idempotencyKey, long pence) {
        return gateway.charge(idempotencyKey, pence);
    }

    @Retry(name = "everything")
    public String chargeRetryingEverything(String idempotencyKey, long pence) {
        return gateway.charge(idempotencyKey, pence);
    }
}
