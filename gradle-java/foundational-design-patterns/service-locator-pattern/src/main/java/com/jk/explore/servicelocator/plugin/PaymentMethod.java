package com.jk.explore.servicelocator.plugin;

/** A payment method that a plug-in can add. What is available is not known until run time. */
public interface PaymentMethod {

    String name();
}
