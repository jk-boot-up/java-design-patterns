package com.jk.explore.dependencyinjection.forms;

import com.jk.explore.dependencyinjection.domain.DiscountPolicy;
import com.jk.explore.dependencyinjection.domain.Notifier;
import com.jk.explore.dependencyinjection.domain.PaymentGateway;

/**
 * <strong>Setter injection: for genuinely optional things.</strong> The
 * mandatory collaborators come through the constructor. The notifier is
 * optional, so it has a setter and a do-nothing default.
 */
public class SetterInjectedCheckout {

    private final DiscountPolicy policy;
    private final PaymentGateway gateway;
    private Notifier notifier = message -> { };

    public SetterInjectedCheckout(DiscountPolicy policy, PaymentGateway gateway) {
        this.policy = policy;
        this.gateway = gateway;
    }

    public void setNotifier(Notifier notifier) {
        this.notifier = notifier;
    }

    public String place(long price) {
        long discounted = policy.apply(price);
        String receipt = gateway.charge(discounted);
        notifier.send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
