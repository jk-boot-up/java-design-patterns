package com.jk.explore.hexagonal.core.port;

import com.jk.explore.hexagonal.core.domain.Money;

/**
 * Taking money from a customer, in words the core chose. Nothing here
 * mentions a card, a network, or a provider — an adapter is free to be any
 * of those, or none.
 */
public interface PaymentGateway {

    void charge(String customerId, Money amount) throws PaymentDeclinedException;
}
