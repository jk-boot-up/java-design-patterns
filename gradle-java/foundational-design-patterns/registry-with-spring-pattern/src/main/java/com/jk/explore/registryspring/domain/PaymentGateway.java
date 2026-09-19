package com.jk.explore.registryspring.domain;

/** Takes the money. The second of the three collaborators. */
public interface PaymentGateway {

    String charge(long pence);
}
