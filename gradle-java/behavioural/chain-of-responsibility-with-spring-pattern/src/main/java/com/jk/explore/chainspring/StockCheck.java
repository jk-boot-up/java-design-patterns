package com.jk.explore.chainspring;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
@Order(20)
public class StockCheck implements ScreeningCheck {
    public String name() { return "stock"; }

    public Optional<Outcome> check(CheckoutRequest request, StringBuilder reason) {
        if (request.inStock()) {
            return Optional.empty();
        }
        reason.append("an item is out of stock");
        return Optional.of(Outcome.REJECTED);
    }
}
