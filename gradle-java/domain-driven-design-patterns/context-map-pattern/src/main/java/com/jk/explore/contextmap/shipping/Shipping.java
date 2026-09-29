package com.jk.explore.contextmap.shipping;

import com.jk.explore.contextmap.kernel.Address;
import com.jk.explore.contextmap.kernel.Money;

/**
 * The shipping context: prints labels. It knows the kernel's Address and Money, and nothing about sales' orders.
 */
public final class Shipping {

    public static String label(String parcelId, Address to, Money insuredFor) {
        return parcelId + " to " + to.label() + ", insured for " + insuredFor;
    }

    private Shipping() {
    }
}
