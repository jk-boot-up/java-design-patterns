package com.jk.explore.servant;

/**
 * The things the shop sends. They share no parent class; each only promises to be Shippable.
 */
public final class Items {

    public record Parcel(String name, int grams, String city) implements Shippable {
    }

    public record Letter(String name, int grams, String city) implements Shippable {
    }

    /** A gift card is also a Voucher: it belongs to two unrelated families, which a shared parent class could not express. */
    public record GiftCard(String name, int grams, String city, long valuePence) implements Shippable, Voucher {
    }

    /** Added in act three: shipped by the same servant with no new shipping code. */
    public record Pallet(String name, int grams, String city) implements Shippable {
    }

    /** Something with a cash value. Unrelated to shipping. */
    public interface Voucher {
        long valuePence();
    }

    private Items() {
    }
}
