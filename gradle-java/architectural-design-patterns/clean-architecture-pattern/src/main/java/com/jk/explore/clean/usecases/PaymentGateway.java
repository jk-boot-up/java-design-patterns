package com.jk.explore.clean.usecases;

import com.jk.explore.clean.entities.Money;

public interface PaymentGateway {

    void charge(String customerId, Money amount) throws PaymentDeclinedException;
}
