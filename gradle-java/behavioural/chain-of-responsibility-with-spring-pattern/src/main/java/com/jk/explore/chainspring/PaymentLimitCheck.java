package com.jk.explore.chainspring;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
@Order(40)
public class PaymentLimitCheck implements ScreeningCheck {
    public String name() { return "payment-limit"; }

    public Optional<Outcome> check(CheckoutRequest request, StringBuilder reason) {
        if (request.amountPence() <= 100_000) {
            return Optional.empty();
        }
        reason.append("over the single-payment limit");
        return Optional.of(Outcome.REFERRED);
    }
}
