package com.jk.explore.diwithspring.app;

import com.jk.explore.diwithspring.domain.DiscountPolicy;
import com.jk.explore.diwithspring.domain.Notifier;
import com.jk.explore.diwithspring.domain.PaymentGateway;

/**
 * <strong>A class that needs seven collaborators has a design problem.</strong>
 * No injection style fixes it. The long constructor is telling you the class
 * does too much.
 */
public class OverloadedService {

    public OverloadedService(DiscountPolicy a, PaymentGateway b, Notifier c, Object d, Object e, Object f, Object g) {
    }
}
