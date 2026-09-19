package com.jk.explore.registry.naive;

import com.jk.explore.registry.domain.DiscountPolicy;
import com.jk.explore.registry.domain.ForwardChain;
import com.jk.explore.registry.domain.Notifier;
import com.jk.explore.registry.domain.PaymentGateway;

/**
 * <strong>Everything passed down, through six constructors.</strong> The
 * gateway is handed through five classes that never use it. This deserves real
 * sympathy: it is friction, and it is honest, because every dependency is
 * visible in a signature.
 */
public class PassedDownCheckout {

    private final ForwardChain.Storefront storefront;
    private final DiscountPolicy policy;
    private final Notifier notifier;

    public PassedDownCheckout(DiscountPolicy policy, PaymentGateway gateway, Notifier notifier) {
        this.storefront = new ForwardChain.Storefront(gateway);
        this.policy = policy;
        this.notifier = notifier;
    }

    public String place(long price) {
        long discounted = policy.apply(price);
        String receipt = storefront.checkout(discounted);
        notifier.send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
