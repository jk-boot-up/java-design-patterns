package com.jk.explore.chainspring;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
@Order(10)
public class AddressCheck implements ScreeningCheck {
    public String name() { return "address"; }

    public Optional<Outcome> check(CheckoutRequest request, StringBuilder reason) {
        if (request.addressValid()) {
            return Optional.empty();
        }
        reason.append("the address does not exist");
        return Optional.of(Outcome.REJECTED);
    }
}
