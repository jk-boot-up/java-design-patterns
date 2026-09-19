package com.jk.explore.servicelocator.plugin;

/** One provider, registered in META-INF/services. Java's own {@code ServiceLoader} finds it. */
public class CardPayment implements PaymentMethod {

    @Override
    public String name() {
        return "card";
    }
}
