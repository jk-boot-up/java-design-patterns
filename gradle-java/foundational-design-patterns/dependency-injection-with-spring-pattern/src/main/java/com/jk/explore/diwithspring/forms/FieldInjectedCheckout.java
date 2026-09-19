package com.jk.explore.diwithspring.forms;

import com.jk.explore.diwithspring.domain.DiscountPolicy;
import com.jk.explore.diwithspring.domain.Notifier;
import com.jk.explore.diwithspring.domain.PaymentGateway;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * <strong>Field injection with Spring: {@code @Autowired} on a private field.</strong>
 * Spring can fill it. Nothing else can: {@code new} gives an invalid object.
 */
public class FieldInjectedCheckout {

    @Autowired
    private DiscountPolicy policy;
    @Autowired
    private PaymentGateway gateway;
    @Autowired
    private Notifier notifier;

    public String place(long price) {
        long discounted = policy.apply(price);
        String receipt = gateway.charge(discounted);
        notifier.send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
