package com.jk.explore.servicelocator.plugin;

/** A second provider. */
public class BankTransferPayment implements PaymentMethod {

    @Override
    public String name() {
        return "bank transfer";
    }
}
