package com.jk.explore.servicestub;

/**
 * The part of checkout that fills in the delivery address from a postcode, and copes when it cannot.
 */
public final class Checkout {

    public static String address(AddressGateway gateway, String postcode) {
        try {
            return gateway.lookup(postcode).map(a -> "deliver to " + a)
                    .orElse("postcode not found: please type your address");
        } catch (IllegalStateException e) {
            return "lookup unavailable: please type your address";
        }
    }

    private Checkout() {
    }
}
