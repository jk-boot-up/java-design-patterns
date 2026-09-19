package com.jk.explore.servicelocator.pattern;

import com.jk.explore.servicelocator.domain.DiscountPolicy;
import com.jk.explore.servicelocator.domain.Notifier;
import com.jk.explore.servicelocator.domain.PaymentGateway;

/**
 * <strong>The checkout asks the locator for each collaborator, when it needs it.</strong>
 * Its constructor takes nothing, so {@code new LocatorCheckout()} always
 * compiles. Whether it works depends on how the locator was configured.
 */
public class LocatorCheckout {

    public String place(long price) {
        long discounted = ServiceLocator.find(DiscountPolicy.class).apply(price);
        String receipt = ServiceLocator.find(PaymentGateway.class).charge(discounted);
        ServiceLocator.find(Notifier.class).send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
