package com.jk.explore.contextmap.before;

/**
 * Without a shared kernel: sales and shipping each keep their own address, and a converter copies one into the other.
 *
 * <p>Sales added a flat number; shipping's address never had one, and the
 * converter quietly drops it.
 */
public final class Separate {

    public record SalesAddress(String flat, String street, String city) {
    }

    public record ShippingAddress(String street, String city) {
        public String label() {
            return street + ", " + city;
        }
    }

    public static ShippingAddress convert(SalesAddress a) {
        return new ShippingAddress(a.street(), a.city());
    }

    private Separate() {
    }
}
