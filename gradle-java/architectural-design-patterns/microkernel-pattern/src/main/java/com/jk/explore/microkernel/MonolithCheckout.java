package com.jk.explore.microkernel;

import java.util.Set;

/** The version where every feature is inside the checkout. */
public class MonolithCheckout {

    public boolean supports(String feature) {
        return Set.of("member-discount", "shipping-fee").contains(feature);
    }

    public long total(long cents, Set<String> features) {
        long total = cents;
        for (String f : features) {
            switch (f) {
                case "member-discount" -> total = total - total * 10 / 100;
                case "shipping-fee" -> total = total + 500;
                default -> { }
            }
        }
        return total;
    }
}
