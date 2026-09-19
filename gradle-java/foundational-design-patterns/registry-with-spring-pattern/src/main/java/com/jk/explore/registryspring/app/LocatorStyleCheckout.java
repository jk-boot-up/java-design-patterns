package com.jk.explore.registryspring.app;

import com.jk.explore.registryspring.domain.DiscountPolicy;
import com.jk.explore.registryspring.domain.Notifier;
import com.jk.explore.registryspring.domain.PaymentGateway;
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

/**
 * <strong>The registry used badly: the class calls {@code getBean}.</strong>
 * It compiles with a constructor that takes nothing, and only works once Spring
 * has handed it the context. This is the hand-built Registry, inside Spring.
 */
@Component
public class LocatorStyleCheckout implements ApplicationContextAware {

    private ApplicationContext context;

    @Override
    public void setApplicationContext(ApplicationContext context) throws BeansException {
        this.context = context;
    }

    public String place(long price) {
        long discounted = context.getBean(DiscountPolicy.class).apply(price);
        String receipt = context.getBean(PaymentGateway.class).charge(discounted);
        context.getBean(Notifier.class).send("paid " + discounted + " pence, " + receipt);
        return receipt;
    }
}
