package com.jk.explore.dependencyinjection.app;

import com.jk.explore.dependencyinjection.domain.DiscountPolicy;
import com.jk.explore.dependencyinjection.domain.Notifier;
import com.jk.explore.dependencyinjection.domain.PaymentGateway;

/**
 * <strong>A class that needs seven collaborators has a design problem.</strong>
 * No injection style fixes it. The long constructor is telling you the class
 * does too much.
 */
public class OverloadedService {

    public OverloadedService(DiscountPolicy a, PaymentGateway b, Notifier c, Object d, Object e, Object f, Object g) {
    }
}
