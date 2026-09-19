package com.jk.explore.registryspring.app;

import com.jk.explore.registryspring.domain.DiscountPolicy;
import com.jk.explore.registryspring.domain.Notifier;
import com.jk.explore.registryspring.domain.PaymentGateway;
import org.springframework.stereotype.Component;

/** <strong>The registry used well: it is never called.</strong> The class is given what it needs. */
@Component
public class InjectedCheckout {

    private final DiscountPolicy policy;
    private final PaymentGateway gateway;
    private final Notifier notifier;

    public InjectedCheckout(DiscountPolicy policy, PaymentGateway gateway, Notifier notifier) {
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
