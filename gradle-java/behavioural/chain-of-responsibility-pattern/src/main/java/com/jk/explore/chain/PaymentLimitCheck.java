package com.jk.explore.chain;

import java.util.Optional;

/** Will the card issuer authorise this much in one go? */
public final class PaymentLimitCheck extends ScreeningHandler {

    @Override
    public String name() {
        return "payment-limit";
    }

    @Override
    protected Optional<Decision> check(CheckoutRequest request) {
        int total = request.totalPounds();
        if (total > request.cardLimitPounds()) {
            return Optional.of(Decision.rejected(name(),
                    "£" + total + " is above the £" + request.cardLimitPounds() + " card limit"));
        }
        return Optional.empty();
    }
}
