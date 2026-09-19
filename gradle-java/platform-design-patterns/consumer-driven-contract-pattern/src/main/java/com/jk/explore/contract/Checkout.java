package com.jk.explore.contract;

import java.util.Map;

/** A consumer. It reads sku and priceCents, so those are what its contract lists. */
public class Checkout {

    public static final Contract CONTRACT = new Contract("checkout", Map.of("sku", Type.STRING, "priceCents", Type.INTEGER));

    /** Returns the total in cents, or -1 if the answer was not what checkout needs. */
    public long total(PriceProvider provider, String sku, int quantity) {
        Object price = provider.price(sku).get("priceCents");
        if (!(price instanceof Integer cents)) {
            return -1;
        }
        return (long) cents * quantity;
    }
}
