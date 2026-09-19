package com.jk.explore.gateway;

/** The one door to taking money. Whatever is behind it is the gateway's business. */
public interface PaymentGateway {
    PaymentResult charge(long pence, String card);
}
