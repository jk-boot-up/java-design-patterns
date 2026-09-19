package com.jk.explore.chainspring;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.Optional;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/** The expensive link: it stands in for a call to a paid scoring service, and counts its calls. */
@Component
@Order(30)
@ConditionalOnProperty(name = "screening.fraud.enabled", havingValue = "true", matchIfMissing = true)
public class FraudScoreCheck implements ScreeningCheck {

    static final AtomicInteger CALLS = new AtomicInteger();
    private final AtomicBoolean serviceDown = new AtomicBoolean();

    public void serviceDown(boolean down) {
        serviceDown.set(down);
    }

    public String name() { return "fraud"; }

    public Optional<Outcome> check(CheckoutRequest request, StringBuilder reason) {
        CALLS.incrementAndGet();
        if (serviceDown.get()) {
            throw new IllegalStateException("fraud service unavailable");
        }
        if (request.fraudScore() > 80) {
            reason.append("fraud score ").append(request.fraudScore());
            return Optional.of(Outcome.REJECTED);
        }
        if (request.fraudScore() >= 55) {
            reason.append("fraud score ").append(request.fraudScore()).append(", a person should look");
            return Optional.of(Outcome.REFERRED);
        }
        return Optional.empty();
    }
}
