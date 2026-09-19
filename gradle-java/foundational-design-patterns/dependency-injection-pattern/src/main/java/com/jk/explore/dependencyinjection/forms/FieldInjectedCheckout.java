package com.jk.explore.dependencyinjection.forms;

import com.jk.explore.dependencyinjection.domain.DiscountPolicy;
import com.jk.explore.dependencyinjection.domain.Notifier;
import com.jk.explore.dependencyinjection.domain.PaymentGateway;

/**
 * <strong>Field injection: discouraged, and this is why.</strong> The fields
 * are private and set from outside by reflection. The object can be built with
 * {@code new} in an invalid state, and it cannot be built validly in a test
 * without a framework, or the same reflection.
 */
public class FieldInjectedCheckout {

    private DiscountPolicy policy;
    private PaymentGateway gateway;
    private Notifier notifier;

    public String place(long price) {
        long discounted = policy.apply(price);
        String receipt = gateway.charge(discounted);
        notifier.send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
