package com.jk.explore.registry.pattern;

import com.jk.explore.registry.domain.DiscountPolicy;
import com.jk.explore.registry.domain.Notifier;
import com.jk.explore.registry.domain.PaymentGateway;

/**
 * <strong>The six constructors collapse: this one takes nothing.</strong>
 * That is the friction gone, and it is also the bill. Nothing in the
 * signature says that three things must be registered before this can run.
 */
public class RegistryCheckout {

    public String place(long price) {
        long discounted = Registry.get(DiscountPolicy.class).apply(price);
        String receipt = Registry.get(PaymentGateway.class).charge(discounted);
        Registry.get(Notifier.class).send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
