package com.jk.explore.cleanspring.usecases;

import com.jk.explore.cleanspring.entities.Money;

public interface PaymentGateway {

    void charge(String customerId, Money amount) throws PaymentDeclinedException;
}
