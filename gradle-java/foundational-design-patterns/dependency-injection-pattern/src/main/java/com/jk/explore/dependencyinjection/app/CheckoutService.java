package com.jk.explore.dependencyinjection.app;

import com.jk.explore.dependencyinjection.domain.DiscountPolicy;
import com.jk.explore.dependencyinjection.domain.Notifier;
import com.jk.explore.dependencyinjection.domain.PaymentGateway;

/**
 * <strong>Constructor injection: the signature is the dependency list.</strong>
 * Complete, checked by the compiler, and the object is valid the moment it
 * exists. It never looks anything up.
 */
public class CheckoutService {

    private final DiscountPolicy policy;
    private final PaymentGateway gateway;
    private final Notifier notifier;

    public CheckoutService(DiscountPolicy policy, PaymentGateway gateway, Notifier notifier) {
        this.policy = policy;
        this.gateway = gateway;
        this.notifier = notifier;
    }

    public String place(long price) {
        long discounted = policy.apply(price);
        String receipt = gateway.charge(discounted);
        notifier.send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
